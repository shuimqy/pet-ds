import requests
import json
class QA:
    url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
    header = {
        "Authorization": "Bearer KvokgkEtSRJqBBwizGdQ:CQGfPKeiYmokbpzZyzzQ" # 注意此处替换自己的APIPassword
    }
    data = {
            "model": "lite", # 指定请求的模型
            "messages": [
                {
                    "role": "user",
                    "content": "你是谁"
                }
            ],
            "stream": True
        }
    # 流式响应解析示例
    def Answer(self,Q):
        self.data["messages"][0]["content"]=Q
        response = requests.post(self.url, headers=self.header, json=self.data, stream=True)
        response.encoding = "utf-8"
        str_all=""
        for line in response.iter_lines(decode_unicode="utf-8"):
            # rint(line)
            if 'content' in line:
                # print(json.loads(line[6:])["choices"][0]["delta"]["content"])
                str_all+=json.loads(line[6:])["choices"][0]["delta"]["content"]
        # print(str)
        return str_all
# Tmp=QA()
# print(Tmp.Answer("hello"))
