import subprocess

from mcp.server.fastmcp import FastMCP


# Initialize FastMCP server
mcp = FastMCP("cmd")


@mcp.tool()
async def cmd(cmd_line: str) -> str:
    """在用户的系统上执行命令行指令。

    Args:
        cmd_line: 要执行的命令行指令。
    """
    res = subprocess.run(
        cmd_line,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return res.stdout.strip()


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
