from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
class UI:
    def __init__(self):
        app = QApplication([])

        # 创建主窗口
        window = QWidget()
        window.setWindowTitle("日程管理系统")
        window.setGeometry(100, 100, 400, 300)  # (x, y, width, height)
        window.setAttribute(Qt.WA_DeleteOnClose, True) # 销毁
        # 显示窗口
        window.show()

        # 运行应用
        app.exec_()
    def CreateButtons(): #按钮创建，按钮功能可以先留空等别人接线

    def CreateCalendar():  #日历创建1：包括切换年月；显示星期、天数；标注当天
