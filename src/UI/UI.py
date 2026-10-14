from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout


class UI:
    def __init__(self):
        app = QApplication([])

        # 创建主窗口
        window = QWidget()
        window.setWindowTitle("日程管理系统")
        window.setGeometry(100, 100, 500, 300)  # 稍微加宽窗口放下4个按钮
        window.setAttribute(Qt.WA_DeleteOnClose, True) # 销毁

        # ========= 布局 =========
        main_layout = QHBoxLayout(window)
        btn_container = self.CreateButtons()
        main_layout.addWidget(btn_container)

        # 显示窗口
        window.show()
        # 运行应用
        app.exec_()

    def CreateButtons(self):
        # 按钮容器
        container = QWidget()
        layout = QHBoxLayout(container)

        # 创建4个按钮
        self.btn_add = QPushButton("添加")
        self.btn_view = QPushButton("查看")
        self.btn_edit = QPushButton("修改")
        self.btn_del = QPushButton("删除")

        # ========= 按钮样式【这次放在按钮实例后面，保证生效】=========
        base_style = """
        QPushButton {
            min-width:70px;
            min-height:30px;
            font-size:14px;
            border: none;
            border-radius: 6px;
            background-color:#2196F3;
            color:white;
        }
        QPushButton:hover {
            background-color:#1976D2;
        }
        QPushButton:pressed {
            background-color:#0D47A1;
        }
        """
        del_style = """
        QPushButton {
            min-width:70px;
            min-height:30px;
            font-size:14px;
            border: none;
            border-radius: 6px;
            background-color:#f44336;
            color:white;
        }
        QPushButton:hover {
            background-color:#d32f2f;
        }
        QPushButton:pressed {
            background-color:#b71c1c;
        }
        """

        # 应用样式
        self.btn_add.setStyleSheet(base_style)
        self.btn_view.setStyleSheet(base_style)
        self.btn_edit.setStyleSheet(base_style)
        self.btn_del.setStyleSheet(del_style)

        # 添加到布局
        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_view)
        layout.addWidget(self.btn_edit)
        layout.addWidget(self.btn_del)
        layout.setSpacing(12)

        # 绑定信号，槽函数空壳，留给别人接线
        self.btn_add.clicked.connect(self.on_add)
        self.btn_view.clicked.connect(self.on_view)
        self.btn_edit.clicked.connect(self.on_edit)
        self.btn_del.clicked.connect(self.on_del)

        return container

    # 空槽函数，后续业务实现
    def on_add(self):
        pass
    def on_view(self):
        pass
    def on_edit(self):
        pass
    def on_del(self):
        pass

    def CreatCalendar():


if __name__ == "__main__":
    ui = UI()
