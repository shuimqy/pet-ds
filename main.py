from PySide6.QtWidgets import QWidget,QApplication,QLabel,QGraphicsOpacityEffect,QHBoxLayout,QPushButton
from PySide6.QtCore import Qt,QPoint
from PySide6.QtGui import QIcon,QPixmap,QMouseEvent,QPaintEvent,QPainter
class Pet(QWidget):
  def __init__(self):
    super().__init__()
    self.init_ui()
  def init_ui(self):
      # 设置窗口标志，去掉标题栏
      self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
      # 设置窗口背景透明
      self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
      self.setGeometry(300, 300, 300, 200)
      self.layout_main=QHBoxLayout()
      self.img_label=MyLabel()
      self.layout_main.addWidget(self.img_label)
      self.setLayout(self.layout_main)

class MyLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.img_main = QPixmap('img/shime1.png')
        self.update()
        self.pressedpos=QPoint()
    def mousePressEvent(self, ev: QMouseEvent):
        if ev.buttons() & Qt.MouseButton.LeftButton:
          self.img_main.load('img/shime2.png')
          self.update()
          self.pressedpos.setX(ev.x())
          self.pressedpos.setY(ev.y())
    def paintEvent(self,ev:QPaintEvent):
      with QPainter(self) as self.p:
        self.p.drawPixmap(self.rect(), self.img_main)
    def mouseMoveEvent(self, ev: QMouseEvent):
      self.move(self.pos()+ev.pos()-self.pressedpos)

if __name__ =='__main__':
  app=QApplication([])
  pet=Pet()
  pet.show()
  app.exec()