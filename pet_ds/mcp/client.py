import json
import platform
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import api
from log import logger


class MCPClient:
    def __init__(self):
        self.sessions: dict[str, ClientSession] = {}
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_script_path: str, name: str = None):
        """Connect to an MCP server with a unique name"""
        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command, args=[server_script_path]
        )

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        stdio, write = stdio_transport
        session = await self.exit_stack.enter_async_context(ClientSession(stdio, write))
        await session.initialize()

        if not name:
            name = server_script_path.split("/")[-1].split(".")[0]
        self.sessions[name] = session

        response = await session.list_tools()
        tools = response.tools
        logger.info(f"连接到 {name} 服务，工具：{[tool.name for tool in tools]}")

    async def get_tools_prompt(self) -> str:
        all_tools = []
        for name, session in self.sessions.items():
            response = await session.list_tools()
            for tool in response.tools:
                all_tools.append(
                    {
                        "server": name,
                        "name": tool.name,
                        "description": tool.description,
                        "input_schema": tool.inputSchema,
                    }
                )

        os_name = platform.system()
        return (
            f"用户的操作系统：{os_name}\n"
            + "当前可用工具列表：\n"
            + json.dumps(all_tools, indent=2)
            + """\n每个工具包含 server 字段标识其所属服务。
请你分析哪些工具对当前回答有帮助，如果要调用工具，请在 **最后一行** 用json格式写出：
{"server":"server_name","name":"tool_name","args":{"arg_name":"value"}}
若无需调用工具，请写"not"
"""
        )

    async def process_query(self, query: str):
        tools_prompt = await self.get_tools_prompt()
        messages = [{"role": "user", "content": tools_prompt + query}]
        first_response = api.completions(messages=messages, stream=False)
        first_response.encoding = "utf-8"

        def extract_answer(raw_text: str) -> tuple[str, str]:
            data = json.loads(raw_text.strip())
            content = data["choices"][0]["message"]["content"]
            tool_call_line = content.strip().split("\n")[-1]
            final_answer = content[: -len(tool_call_line)]
            return final_answer, tool_call_line

        final_answer, tool_call_line = extract_answer(first_response.text)
        logger.info(f"{final_answer = }")
        logger.info(f"{tool_call_line = }")
        segment_length = 9
        for i in range(len(final_answer) // segment_length + 1):
            segment = final_answer[i * segment_length : (i + 1) * segment_length]
            yield segment

        if tool_call_line == "not":
            return

        tool_call = json.loads(tool_call_line)
        server_name = tool_call["server"]
        if server_name not in self.sessions:
            raise ValueError(f"未找到指定的服务：{server_name}")
        session = self.sessions[server_name]

        tool_call_note = f"\n调用工具（服务：{server_name}）：{tool_call['name']}，参数：{tool_call['args']}\n"
        yield tool_call_note

        tool_call_result = await session.call_tool(tool_call["name"], tool_call["args"])
        logger.info(f"Tool call result: {tool_call_result}")

        messages.append({"role": "assistant", "content": first_response.text})
        messages.append(
            {
                "role": "user",
                "content": str(tool_call_result.content)
                + "\n上面是工具调用的结果，请你分析并生成最终回答。",
            }
        )

        second_response = api.completions(messages=messages, stream=True)
        second_response.encoding = "utf-8"
        for line in second_response.iter_lines(decode_unicode="utf-8"):
            if "content" in line:
                yield json.loads(line[6:])["choices"][0]["delta"]["content"]

    async def cleanup(self):
        await self.exit_stack.aclose()
