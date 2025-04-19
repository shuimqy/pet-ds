from pydantic import BaseModel


class Config(BaseModel):
    # LLM 密钥
    api_key: str = ""
    # LLM url
    llm_url: str = "https://api.siliconflow.cn/v1/chat/completions"
    # 模型
    model: str = "THUDM/GLM-4-9B-0414"
    # mcp server 路径
    mcp_server_path: str = "mcp/server/weather.py"
    # 代理
    proxy: str = "http://127.0.0.1:7890"


conf = Config()
