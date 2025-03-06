from PySide6.QtWidgets import QWidget,QApplication,QLabel,QGraphicsOpacityEffect
from PySide6.QtCore import Qt
class Pet(QWidget):
  def __init__(self):
    super().__init__()
    self.init_ui() 

  def init_ui(self):
      """初始化界面"""
      self.setWindowTitle("Desktop Pet")
      self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                          Qt.WindowType.WindowStaysOnTopHint |
                          Qt.WindowType.Tool)
      self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
      self.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
       # 设置初始大小和位置
      self.resize(128, 128)
      screen_geo = QApplication.primaryScreen().geometry()
      self.move(screen_geo.width()-150, screen_geo.height()-150)
      
      # 创建显示标签
      self.label = QLabel(self)
      self.label.setGeometry(0, 0, 128, 128)
      self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
      self.label.setText("111111")
      # 添加半透明效果
      opacity_effect = QGraphicsOpacityEffect(self)
      opacity_effect.setOpacity(0.9)
      self.label.setGraphicsEffect(opacity_effect)

if __name__ =='__main__':
  app=QApplication([])
  pet=Pet()
  pet.show()
  app.exec()