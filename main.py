from PySide6.QtWidgets import (
    QWidget, QApplication, QLabel,
    QMenu, QGraphicsOpacityEffect, QHBoxLayout, QPushButton
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QIcon, QPixmap,QContextMenuEvent, QMouseEvent, QPaintEvent, QPainter, QAction

class Pet(QWidget):
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
        self.img_label = MyLabel(self)
        self.img_label.show()

class MyLabel(QLabel):
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
        
        # 绑定槽函数
        action_quit.triggered.connect(self.on_quit)
        action_change_face.triggered.connect(self.on_change_face)
        action_info.triggered.connect(self.on_show_info)
        
        # 将选项添加到菜单
        menu.addAction(action_quit)
        menu.addAction(action_change_face)
        menu.addAction(action_info)
        
        # 在形象旁显示菜单
        menu.exec(QPoint(self.pos().x()*0.92,self.pos().y())*1.05)

    def on_quit(self):
        """ 退出程序 """
        QApplication.quit()

    def on_change_face(self):
        """ 切换表情 """
        # 示例：切换图片
        self.img_main.load('img/shime3.png')  # 假设存在 shime3.png
        self.update()

    def on_show_info(self):
        """ 显示关于信息 """
        print("这是一个桌面宠物程序")

    # ==================== 原有逻辑 ====================
    def mousePressEvent(self, ev: QMouseEvent):
        if ev.button() == Qt.MouseButton.LeftButton:
            self.img_main.load('img/shime2.png')
            self.update()
            self.pressedpos = ev.position().toPoint()

    def mouseMoveEvent(self, ev: QMouseEvent):
        new_pos = self.pos() + ev.position().toPoint() - self.pressedpos
        self.move(new_pos)

    def mouseReleaseEvent(self, ev: QMouseEvent):
        self.img_main.load('img/shime1.png')
        self.update()

    def paintEvent(self, ev: QPaintEvent):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.img_main)

if __name__ == '__main__':
    app = QApplication([])
    pet = Pet()
    pet.show()
    app.exec()