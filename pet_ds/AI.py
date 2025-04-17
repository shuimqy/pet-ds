import json
import time
import asyncio

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

import api
from pet_ds.config import conf
from pet_ds.mcp.client import MCPClient


class Msg_signal(QWidget):
    # 消息气泡更新相关信号
    ready_send = Signal()
    new_msg = Signal(str)
    finished_msg = Signal()


class QA:
    def __init__(self):
        self.msg_signal = Msg_signal()

    async def mcp_answer(self, query: str):
        client = MCPClient()
        try:
            await client.connect_to_server(conf.mcp_server_path)
            agenerator = client.process_query(query)
            self.msg_signal.ready_send.emit()
            async for chunk in agenerator:
                self.msg_signal.new_msg.emit(chunk)
                await asyncio.sleep(0.1)
            self.msg_signal.finished_msg.emit()
        except Exception as e:
            print(e)
            raise
        finally:
            await client.cleanup()

    # 流式响应解析示例
    def answer(self, query, mcp_isChecked: bool):
        print(f"位于AI.py QA类 Answer方法中的mcp_isChecked变量的值为: {mcp_isChecked}")
        if mcp_isChecked:
            asyncio.run(self.mcp_answer(query))
            # self.msg_signal.ready_send.emit()
            # self.msg_signal.new_msg.emit(result)
            # self.msg_signal.finished_msg.emit()
        else:
            response = api.simplechat(query)
            response.encoding = "utf-8"
            self.msg_signal.ready_send.emit()
            for line in response.iter_lines(decode_unicode="utf-8"):
                if "content" in line:
                    self.msg_signal.new_msg.emit(
                        json.loads(line[6:])["choices"][0]["delta"]["content"]
                    )
                    time.sleep(0.1)
            self.msg_signal.finished_msg.emit()
