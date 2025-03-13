import requests
import json
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
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
    def __init__(self):
        self.msg_signal=Msg_signal()
    # 流式响应解析示例
    def Answer(self,Q):
        self.data["messages"][0]["content"]=Q
        response = requests.post(self.url, headers=self.header, json=self.data, stream=True)
        response.encoding = "utf-8"
        str_all=""
        for line in response.iter_lines(decode_unicode="utf-8"):
            if 'content' in line:
                self.msg_signal.new_msg.emit(json.loads(line[6:])["choices"][0]["delta"]["content"])
        self.msg_signal.finished_msg.emit()

class Msg_signal(QWidget):
    # 消息气泡更新相关信号
    new_msg=Signal(str)
    finished_msg=Signal()