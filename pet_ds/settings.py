# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QSizePolicy,
    QStackedWidget, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.gridStackedWidget = QStackedWidget(Form)
        self.gridStackedWidget.setObjectName(u"gridStackedWidget")
        self.gridStackedWidget.setGeometry(QRect(0, 0, 401, 301))
        self.WidgetPage1 = QWidget()
        self.WidgetPage1.setObjectName(u"WidgetPage1")
        self.gridLayout = QGridLayout(self.WidgetPage1)
        self.gridLayout.setObjectName(u"gridLayout")
        self.checkBox_2 = QCheckBox(self.WidgetPage1)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.gridLayout.addWidget(self.checkBox_2, 1, 0, 1, 1)

        self.on_top_checkBox = QCheckBox(self.WidgetPage1)
        self.on_top_checkBox.setObjectName(u"on_top_checkBox")

        self.gridLayout.addWidget(self.on_top_checkBox, 0, 0, 1, 1)

        self.checkBox_3 = QCheckBox(self.WidgetPage1)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.gridLayout.addWidget(self.checkBox_3, 0, 1, 1, 1)

        self.checkBox_4 = QCheckBox(self.WidgetPage1)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.gridLayout.addWidget(self.checkBox_4, 1, 1, 1, 1)

        self.gridStackedWidget.addWidget(self.WidgetPage1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.checkBox_2.setText(QCoreApplication.translate("Form", u"CheckBox", None))
        self.on_top_checkBox.setText(QCoreApplication.translate("Form", u"\u5728\u6240\u6709\u754c\u9762\u7f6e\u9876", None))
        self.checkBox_3.setText(QCoreApplication.translate("Form", u"CheckBox", None))
        self.checkBox_4.setText(QCoreApplication.translate("Form", u"CheckBox", None))
    # retranslateUi

