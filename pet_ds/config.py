from pydantic import BaseModel


class Config(BaseModel):
    # LLM 密钥
    api_key: str = "sk-qmuzdsgridawrpjevnfwghbtckfegbhwmimcmopyrjvvffyu"
    # LLM url
    llm_url: str = "https://api.siliconflow.cn/v1/chat/completions"
    # 模型
    model: str = "THUDM/GLM-4-9B-0414"
    # mcp server 路径
    mcp_server_path: str = "D:/junior-work/junior/pet-ds/pet_ds/mcp/server/weather.py"
    # 代理
    proxy: str = "http://127.0.0.1:7890"


conf = Config()

# url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
#     header = {
#         "Authorization": "Bearer KvokgkEtSRJqBBwizGdQ:CQGfPKeiYmokbpzZyzzQ" # 注意此处替换自己的APIPassword
#     }
#     data = {
#             "model": "lite", # 指定请求的模型
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": "你是谁"
#                 }
#             ],
#             "stream": True
#         }
