from pydantic import BaseModel


class Config(BaseModel):
    # LLM 密钥
    api_key: str = (
        "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"
    )
    # LLM url
    llm_url: str = "https://openrouter.ai/api/v1/chat/completions"
    # 模型
    model: str = "deepseek/deepseek-chat-v3-0324:free"
    # mcp server 路径
    mcp_server_path: str = "D:/junior-work/junior/pet-ds/pet_ds/mcp/server/weather.py"
    # 代理
    proxy: str = "http://127.0.0.1:7890"


conf = Config()
