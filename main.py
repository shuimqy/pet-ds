from PySide6.QtWidgets import (
    QWidget, QApplication, QLabel,
    QMenu, QGraphicsOpacityEffect, QHBoxLayout, QPushButton,QDialog,QVBoxLayout,QLineEdit
)
from PySide6.QtCore import Qt, QPoint,Signal,QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QIcon, QPixmap,QContextMenuEvent, QMouseEvent, QPaintEvent, QPainter, QAction

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置窗口属性（无边框、透明、置顶）
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.showFullScreen()

        # 创建桌宠标签
        self.img_label = Pet(self)
        self.img_label.show()

class Pet(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.img_main = QPixmap('img/shime1.png')
        self.setFixedSize(self.img_main.width(), self.img_main.height())
        self.pressedpos = QPoint()
        # 初始位置：右下角
        self.move(
            self.parentWidget().width() * 0.85,
            self.parentWidget().height() * 0.75
        )
        #对话实例
        self.dialog=None
    # ==================== 右键菜单逻辑 ====================
    def contextMenuEvent(self, event: QContextMenuEvent):
        """ 右键点击时弹出菜单 """
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
        action_dialog=QAction("对话",self)        
        # 绑定槽函数
        action_quit.triggered.connect(self.on_quit)
        action_change_face.triggered.connect(self.on_change_face)
        action_info.triggered.connect(self.on_show_info)
        action_dialog.triggered.connect(self.on_dialog)
        # 将选项添加到菜单
        menu.addAction(action_quit)
        menu.addAction(action_change_face)
        menu.addAction(action_info)
        menu.addAction(action_dialog)
        # 在形象旁显示菜单
        menu.exec(QPoint(self.pos().x()*0.92,self.pos().y())*1.05)

    def on_quit(self):
        """ 退出程序 """
        QApplication.quit()

    def on_change_face(self):
        """ 切换表情 """
        # 示例：切换图片
        self.img_main.load('img/shime3.png') 
        self.update()

    def on_show_info(self):
        """ 显示关于信息 """
        print("这是一个桌面宠物程序")
    def on_dialog(self):
        pass

    def mousePressEvent(self, ev: QMouseEvent):
        if ev.button() == Qt.MouseButton.LeftButton:
            self.img_main.load('img/shime2.png')
            self.update()
            self.pressedpos = ev.position().toPoint()
        if self.dialog != None:
            self.dialog.close()
    def mouseMoveEvent(self, ev: QMouseEvent):
        new_pos = self.pos() + ev.position().toPoint() - self.pressedpos
        self.move(new_pos)

    def mouseReleaseEvent(self, ev: QMouseEvent):
        self.img_main.load('img/shime1.png')
        self.update()

    def paintEvent(self, ev: QPaintEvent):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.img_main)
    
    def mouseDoubleClickEvent(self, event):
        if self.dialog != None:
            self.dialog.close()

    def on_dialog(self):
        """ 弹出对话输入框 """
        self.dialog = ChatDialog(self.parentWidget(), self.pos())
        self.dialog.message_sent.connect(self._handle_message)
        self.dialog.show()


    def _handle_message(self, msg: str):
        """ 处理用户输入的消息 """
        print(f"收到消息: {msg}")
        reply=msg
        # 显示气泡
        self.show_bubble(reply)

    def show_bubble(self, text: str):
        """ 显示消息气泡 """
        # 关闭旧气泡（如果存在）
        if hasattr(self, 'bubble') and self.bubble:
            self.bubble.close()
        
        # 创建新气泡
        self.bubble = ChatBubble(text, self.parentWidget(), self.pos())
        self.bubble.show()

class ChatDialog(QDialog):
# 定义信号用于传递输入内容
    message_sent = Signal(str)

    def __init__(self, parent=None, pet_pos:QPoint=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(200, 120)
        
        # 根据桌宠位置定位
        if pet_pos:
            self.move(
            pet_pos.x() - 200,
            pet_pos.y()
        )
        
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

# 回答显示气泡类
class ChatBubble(QLabel):
    def __init__(self, text: str, parent=None, pet_pos: QPoint = None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        #美化
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
        if pet_pos:
            screen = QApplication.primaryScreen().availableGeometry()
            
            # 水平定位：优先左侧显示
            bubble_left = pet_pos.x() - self.width() - 30
            bubble_right = pet_pos.x() + 100
            
            if bubble_left > 20:  # 左侧空间足够
                x = bubble_left
            elif screen.width() - bubble_right > 20:  # 右侧空间足够
                x = bubble_right
            else:  # 两侧都不够时居中
                x = (screen.width() - self.width()) // 2
                
            # 垂直定位：居中于桌宠形象
            y = pet_pos.y() - self.height() // 2
            
            # 垂直边界保护
            y = max(20, min(y, screen.height() - self.height() - 20))
            
            self.move(int(x), int(y))

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
        self.timer.singleShot(2000, self.fade_out)

    def fade_out(self):
        """ 优雅的淡出动画 """
        self.opacity_anim.setDuration(800)
        self.opacity_anim.setStartValue(1.0)
        self.opacity_anim.setEndValue(0.0)
        self.opacity_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.opacity_anim.finished.connect(self.close)
        self.opacity_anim.start()

if __name__ == '__main__':
    app = QApplication([])
    pet = MainWindow()
    pet.show()
    app.exec()