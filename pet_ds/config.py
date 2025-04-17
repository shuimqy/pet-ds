from pydantic import BaseModel


class Config(BaseModel):
    # LLM 密钥
    api_key: str = ""
    # LLM url
    llm_url: str = "https://openrouter.ai/api/v1/chat/completions"
    # 模型
    model: str = "deepseek/deepseek-chat-v3-0324:free"
    # mcp server 路径
    mcp_server_path: str = "E:\\work\\vscode\\pet-ds\\pet_ds\\mcp\\server\\weather.py"
    # 代理
    proxy: str = None


conf = Config()
