from PySide6.QtWidgets import (
    QWidget,
    QApplication,
    QLabel,
    QMenu,
    QGraphicsOpacityEffect,
    QPushButton,
    QDialog,
    QVBoxLayout,
    QLineEdit,
)
from PySide6.QtCore import (
    QSettings,
    QThreadPool,
    QRunnable,
    Slot,
    Qt,
    QPoint,
    Signal,
    QTimer,
    QPropertyAnimation,
    QEasingCurve,
)
from PySide6.QtGui import (
    QPixmap,
    QContextMenuEvent,
    QMouseEvent,
    QPaintEvent,
    QPainter,
    QAction,
)
from AI import QA
from transitions import State, Machine

# 导入设置界面
from Ui_untitled import Ui_Form


def AccPetPos(pet_pos: QPoint, Q: QWidget):
    if pet_pos:
        screen = QApplication.primaryScreen().availableGeometry()

        # 水平定位：优先左侧显示
        left = pet_pos.x() - Q.width()
        right = pet_pos.x() + 100

        if left > 20:  # 左侧空间足够
            x = left
        elif screen.width() - right > 20:  # 右侧空间足够
            x = right
        else:  # 两侧都不够时居中
            x = (screen.width() - Q.width()) // 2

        # 垂直定位：居中于桌宠形象
        y = pet_pos.y() - Q.height() // 2

        # 垂直边界保护
        y = max(20, min(y, screen.height() - Q.height() - 20))

        return QPoint(x, y)


# 回答显示气泡类
class ChatBubble(QLabel):
    def __init__(self, text: str, parent=None, pet_pos: QPoint = None):
        super().__init__(parent)
        self.pet_pos = pet_pos
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 美化
        self.setStyleSheet("""
            QLabel {
                /* 背景颜色 (0.95透明度) */
                background: rgba(23, 32, 56, 0.95);
                
                /* 现代渐变边框 */
                border: 2px solid qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(82, 130, 164, 1),
                    stop:1 rgba(122, 180, 220, 1)
                );
                
                /* 圆角效果 */
                border-radius: 12px;
                
                /* 内部填充 */
                padding: 12px 16px;
                
                /* 字体样式 */
                color: #e0f0ff;
                font-family: "微软雅黑";
                font-size: 14px;
                font-weight: 500;
                
                /* 控件阴影 */
                margin: 8px;
            }
            
            /* 伪元素实现发光效果 */
            QLabel::before {
                content: "";
                position: absolute;
                top: -6px;
                left: 20px;
                width: 12px;
                height: 12px;
                background: rgba(82, 130, 164, 0.8);
                transform: rotate(45deg);
                z-index: -1;
            }
        """)

        self.setText(text)
        self.setWordWrap(True)  # 启用自动换行
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # 根据内容调整尺寸 (最大宽度300px)
        self.setMaximumWidth(300)
        self.adjustSize()
        # 定位
        self.move(AccPetPos(self.pet_pos, self))

        # 淡入动画
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_anim.setDuration(300)
        self.opacity_anim.setStartValue(0.0)
        self.opacity_anim.setEndValue(1.0)
        self.opacity_anim.start()

        # 淡出定时器（3秒后开始淡出）
        self.timer = QTimer(self)
        self.timer.singleShot(5000, self.fade_out)

    def move_bubble(self, new_pos: QPoint):
        self.move(AccPetPos(new_pos, self))

    # 追加文本信息
    def text_append(self, new_text: str):
        # 计时器暂停，重新开始计时
        self.timer.stop()
        tmp = self.text() + new_text
        self.setText(tmp)
        print("调用文本追加")
        self.adjustSize()
        self.move(AccPetPos(self.pet_pos, self))
        self.timer.start(5000)

    def fade_out(self):
        """优雅的淡出动画"""
        self.opacity_anim.setDuration(800)
        self.opacity_anim.setStartValue(1.0)
        self.opacity_anim.setEndValue(0.0)
        self.opacity_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.opacity_anim.finished.connect(self.close)
        self.opacity_anim.start()


# 定义全局Qsettings实例
# 初始化相关(Qsettings)

Q_set = QSettings("config.ini", QSettings.IniFormat)
img_dir = "D:/junior-work/junior/pet-ds/img"


# Q_set.setValue("a",100)
# Q_set.setValue("MainWindow/is_on_top",True)
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置窗口属性（无边框、透明、置顶）
        if Q_set.value("MainWindow/is_on_top", type=bool):
            self.setWindowFlags(
                Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
            )
        else:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.showFullScreen()
        # 创建桌宠标签
        self.pat = Pet(self)
        self.pat.show()
        #

    def show_set_ui(self):
        self.set_ui = SetUi()
        self.set_ui.show()


class SetUi(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.on_top_checkBox.toggled.connect(self.on_top_checkBox_changed)

        self.on_top_checkBox.setChecked(Q_set.value("MainWindow/is_on_top", type=bool))

    def on_top_checkBox_changed(self):
        if self.on_top_checkBox.isChecked():
            Q_set.setValue("MainWindow/is_on_top", True)
        else:
            Q_set.setValue("MainWindow/is_on_top", False)


class Pet(QLabel):
    def __init__(self, parent: MainWindow = None):
        super().__init__(parent)
        self.father = parent
        # 初始化状态机
        self.machine_init()

        self.img_main = QPixmap(f"{img_dir}/shime1.png")
        self.setFixedSize(self.img_main.width(), self.img_main.height())
        self.pressedpos = QPoint()
        # 初始位置：右下角
        self.move(
            self.parentWidget().width() * 0.85, self.parentWidget().height() * 0.75
        )
        # 对话实例
        self.dialog = None
        # 添加定时器
        # 状态控制相关
        self.idle_timer = QTimer(self)
        self.idle_timer.timeout.connect(self._on_idle)
        self.reset_state_timer()
        # 调用ai异步处理初始化函数
        self._init_async_ai()

    def _init_async_ai(self):
        """初始化异步 AI 处理"""
        self.thread_pool = QThreadPool.globalInstance()  # 获取全局线程池
        self.thread_pool.setMaxThreadCount(2)  # 最多同时处理2个请求

        # 初始化加载气泡
        self.loading_bubble = None
        self.bubble = None

    def _handle_message(self, msg: str):
        """非阻塞处理消息"""
        self.reset_state_timer()
        print(f"收到消息: {msg}")

        # 显示加载动画
        self._show_loading()

        # 创建并启动工作线程
        worker = AIWorker(msg, self)
        # worker.signals.finished.connect(self._on_ai_reply)
        # worker.signals.error.connect(self._on_ai_error)
        worker.ai.msg_signal.ready_send.connect(self._on_ai_reply)
        worker.ai.msg_signal.new_msg.connect(self.bubble_text_append)
        self.thread_pool.start(worker)

    def bubble_text_append(self, text: str):
        self.bubble.text_append(text)

    def _show_loading(self):
        """显示加载中的气泡"""
        if self.loading_bubble is None:
            self.loading_bubble = ChatBubble(
                "思考中...", self.parentWidget(), self.pos()
            )
            self.loading_bubble.show()

    def _hide_loading(self):
        """隐藏加载动画"""
        if self.loading_bubble:
            self.loading_bubble.close()
            self.loading_bubble = None

    def _on_ai_reply(self, result: str = ""):
        """成功收到 AI 回复"""
        self._hide_loading()
        self.show_bubble(result)

    def _on_ai_error(self, error_msg: str):
        """处理 AI 错误"""
        self._hide_loading()
        self.show_bubble(f"❌ {error_msg}")

    # ==================== 状态机相关 ====================
    def reset_state_timer(self):
        """重置无操作计时器"""
        self.idle_timer.stop()
        if self.state != "busy":
            self.to_busy()  # 切换到忙碌状态
        self.idle_timer.start(5000)  # 10秒无操作触发

    def _on_idle(self):
        """无操作超时处理"""
        self.to_free()  # 切换回空闲状态
        self.idle_timer.stop()

    def machine_init(self):
        # 定义状态
        states = [
            State(name="busy", on_enter=self._on_enter_busy),
            State(name="free", on_enter=self._on_enter_free),
        ]

        self.machine = Machine(model=self, states=states, initial=states[1])
        self.machine.add_transition(trigger="to_free", source="busy", dest="free")
        self.machine.add_transition(trigger="to_busy", source="free", dest="busy")

    def _on_enter_busy(self):
        print("进入忙碌状态")
        # 可以在这里停止空闲动画

    def _on_enter_free(self):
        print("进入空闲状态")
        # 可以在这里启动自动行为

    # ==================== 右键菜单逻辑 ====================
    def contextMenuEvent(self, event: QContextMenuEvent):
        """右键点击时弹出菜单"""
        # 创建菜单对象
        menu = QMenu(self)
        # 样式表美化
        menu.setStyleSheet(
            "QMenu {background-color:rgba(17,24,47,1);border:1px solid rgba(82,130,164,1);}\
 QMenu::item {min-width:50px;font-size: 12px;color: rgb(225,225,225);background:rgba(75,120,154,0.5);border:1px solid rgba(82,130,164,1);padding:1px 1px;margin:1px 1px;}\
 QMenu::item:selected {background:rgba(82,130,164,1);border:1px solid rgba(82,130,164,1);}  /*选中或者说鼠标滑过状态*/\
 QMenu::item:pressed {background:rgba(82,130,164,0.4);border:1px solid rgba(82,130,164,1);/*摁下状态*/}"
        )
        # 添加菜单选项
        action_quit = QAction("退出", self)
        action_change_face = QAction("切换表情", self)
        action_info = QAction("关于", self)
        action_dialog = QAction("对话", self)
        # action_mcp=QAction("",self)
        action_set = QAction("设置", self)
        # 绑定槽函数
        action_quit.triggered.connect(self.on_quit)
        action_change_face.triggered.connect(self.on_change_face)
        action_info.triggered.connect(self.on_show_info)
        action_dialog.triggered.connect(self.on_dialog)
        action_set.triggered.connect(self.on_set)
        # 将选项添加到菜单
        menu.addAction(action_quit)
        menu.addAction(action_change_face)
        menu.addAction(action_info)
        menu.addAction(action_dialog)
        menu.addAction(action_set)
        # 在形象旁显示菜单
        point_tem = AccPetPos(self.pos(), self)
        menu.exec(QPoint(point_tem.x() + 50, point_tem.y() + 80))

    def on_quit(self):
        """退出程序"""
        QApplication.quit()

    def on_change_face(self):
        """切换表情"""
        # 示例：切换图片
        self.img_main.load(f"{img_dir}/shime3.png")
        self.reset_state_timer()
        self.update()

    def on_show_info(self):
        """显示关于信息"""
        self.reset_state_timer()
        print("这是一个桌面宠物程序")

    def on_set(self):
        self.father.show_set_ui()

    def mousePressEvent(self, ev: QMouseEvent):
        self.reset_state_timer()
        if ev.button() == Qt.MouseButton.LeftButton:
            self.img_main.load(f"{img_dir}/shime2.png")
            self.update()
            self.pressedpos = ev.position().toPoint()
        if self.dialog != None:
            self.dialog.close()

    def mouseMoveEvent(self, ev: QMouseEvent):
        self.reset_state_timer()
        new_pos = self.pos() + ev.position().toPoint() - self.pressedpos
        self.move(new_pos)
        if self.bubble != None:
            self.bubble.move_bubble(new_pos)

    def mouseReleaseEvent(self, ev: QMouseEvent):
        self.reset_state_timer()
        self.img_main.load(f"{img_dir}/shime1.png")
        self.update()

    def paintEvent(self, ev: QPaintEvent):
        self.reset_state_timer()
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.img_main)

    def mouseDoubleClickEvent(self, event):
        self.reset_state_timer()
        if self.dialog != None:
            self.dialog.close()

    def on_dialog(self):
        """弹出对话输入框"""
        self.dialog = ChatDialog(self.parentWidget(), self.pos())
        self.dialog.message_sent.connect(self._handle_message)
        self.dialog.show()

    def show_bubble(self, text: str):
        self.reset_state_timer()
        """ 显示消息气泡 """
        # 关闭旧气泡（如果存在）
        if self.bubble:
            self.bubble.close()
            self.bubble = None
        # 创建新气泡
        self.bubble = ChatBubble(text, self.parentWidget(), self.pos())
        self.bubble.show()


# ai处理异步线程相关
# # 仅继承Qobject类定义信号
# class AIWorkerSignals(QObject):
#     finished = Signal(str)  # 成功信号
#     error = Signal(str)     # 错误信号


class AIWorker(QRunnable):
    def __init__(self, message: str, pet: Pet):
        super().__init__()
        self.message = message
        # self.signals=AIWorkerSignals()
        self.ai = QA()

    @Slot()
    def run(self):
        try:
            self.ai.Answer(self.message)
            # self.signals.finished.emit(result)
        except Exception as e:
            self.signals.error.emit(f"AI 处理失败: {str(e)}")


class ChatDialog(QDialog):
    # 定义信号用于传递输入内容
    message_sent = Signal(str)

    def __init__(self, parent=None, pet_pos: QPoint = None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(200, 120)

        # 根据桌宠位置定位
        self.move(AccPetPos(pet_pos, self))
        # 样式表
        self.setStyleSheet("""
            QDialog {
                background: rgba(17, 24, 47, 0.9);
                border: 1px solid rgba(82, 130, 164, 1);
                border-radius: 8px;
            }
            QLineEdit {
                background: rgba(75, 120, 154, 0.5);
                border: 1px solid rgba(82, 130, 164, 1);
                color: white;
                padding: 5px;
                border-radius: 4px;
            }
            QPushButton {
                background: rgba(82, 130, 164, 0.7);
                border: 1px solid rgba(82, 130, 164, 1);
                color: white;
                padding: 5px;
                border-radius: 4px;
                min-width: 60px;
            }
            QPushButton:hover {
                background: rgba(82, 130, 164, 1);
            }
        """)

        # 布局和控件
        layout = QVBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("输入消息...")
        self.btn_send = QPushButton("发送")

        layout.addWidget(self.input_box)
        layout.addWidget(self.btn_send)
        self.setLayout(layout)

        # 连接信号
        self.btn_send.clicked.connect(self._on_send)

    def _on_send(self):
        text = self.input_box.text()
        if text:
            # 发出信号
            self.message_sent.emit(text)
            self.close()


if __name__ == "__main__":
    app = QApplication([])
    pet = MainWindow()
    pet.show()
    app.exec()
