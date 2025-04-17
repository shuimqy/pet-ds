import asyncio
import json
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from anthropic import Anthropic

from pet_ds import api

# load_dotenv()  # load environment variables from .env
from traceback import print_stack


class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command, args=[server_script_path], env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def get_tools_prompt(self) -> str:
        response = await self.session.list_tools()
        available_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            }
            for tool in response.tools
        ]
        return (
            json.dumps(available_tools)
            + """上面是一个工具列表，可以被调用，其中name表示工具名称，description是工具的功能描述，input_schema是调用工具需要传递的参数。
请你分析哪些工具对当前回答有帮助，如果要调用工具，请先分析解决问题的步骤，最后在 **最后一行** 用json格式写出工具名称和传递参数，示例如下：
(回答内容)
{"name":"tool_name","args":{"arg_name1":"arg_value1","arg_name12":"arg_value2"}}
如果你认为不需要调用工具或者没有工具能帮助到当前对话，请在 **最后一行** 写出"not"，如下：
(回答内容)
not
请遵循以上要求，回答用户问题：
"""
        )

    async def process_query(self, query: str):
        """Process a query using Claude and available tools"""
        # 1. 第一次调用
        tools_prompt = await self.get_tools_prompt()
        messages = [
            {
                "role": "user",
                "content": tools_prompt + query,
            }
        ]
        first_response = api.completions(messages=messages, stream=False)
        first_response.encoding = "utf-8"

        def extract_answer(raw_text: str) -> tuple[str, str]:
            data = json.loads(raw_text.strip())
            print(data)
            content = data["choices"][0]["message"]["content"]
            tool_call_line = content.strip().split("\n")[-1]  # 最后一行
            final_answer = content[: -len(tool_call_line)]  # 去除最后一行
            return final_answer, tool_call_line

        final_answer, tool_call_line = extract_answer(first_response.text)
        yield final_answer
        if tool_call_line == "not":  # 不调用工具，直接返回
            return
        # 2. 调用工具
        tool_call = json.loads(tool_call_line)
        # 调用工具
        tool_call_note = f"调用工具：{tool_call['name']}，参数：{tool_call['args']}"
        yield tool_call_note
        # final_answer += tool_call_note
        tool_call_result = await self.session.call_tool(
            tool_call["name"], tool_call["args"]
        )
        # 3. 提供上下文给llm，生成二次回答
        messages.append({"role": "assistant", "content": first_response.text})
        messages.append(
            {
                "role": "user",
                "content": str(tool_call_result.content)
                + "上面是工具调用的结果，请你分析并生成回答",
            }
        )
        second_response = api.completions(messages=messages, stream=True)
        second_response.encoding = "utf-8"
        content = ""
        for line in second_response.iter_lines(decode_unicode="utf-8"):
            if "content" in line:
                content = json.loads(line[6:])["choices"][0]["delta"]["content"]
                yield content
        # data = json.loads(second_response.text.strip())
        # content = data["choices"][0]["message"]["content"]
        # final_answer += content

        # return final_answer

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == "quit":
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")
                raise

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


async def main():
    client = MCPClient()
    try:
        server_path = (
            sys.argv[1]
            if len(sys.argv) >= 2
            else "E:\\work\\vscode\\pet-ds\\pet_ds\\mcp\\server\\weather.py"
        )
        await client.connect_to_server(server_path)
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    import sys

    asyncio.run(main())
