from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QCalendarWidget, QListWidget, QPushButton, QLabel
)
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("日程管理系统")
        self.resize(760, 540)

        # 主布局
        main_layout = QHBoxLayout()

        # 左侧日历
        self.calendar = self.CreateCalendar()
        # 右侧面板
        right_panel = self.create_right_panel()

        main_layout.addWidget(self.calendar)
        main_layout.addWidget(right_panel)
        self.setLayout(main_layout)

        # ========== 按钮信号绑定（接线）==========
        self.btn_add.clicked.connect(self.on_add_click)
        self.btn_view.clicked.connect(self.on_view_click)
        self.btn_edit.clicked.connect(self.on_edit_click)
        self.btn_del.clicked.connect(self.on_delete_click)
        self.calendar.selectionChanged.connect(self.on_date_selected)


    def CreateCalendar(self):
        """创建日历控件"""
        calendar = QCalendarWidget()
        calendar.setGridVisible(True)
        calendar.setStyleSheet("font-size:14px;")
        calendar.setMinimumWidth(380)
        return calendar


    def create_right_panel(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title_label = QLabel("📋 日程列表")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size:16px; font-weight:bold; padding:10px;")
        layout.addWidget(title_label)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("font-size:14px;")
        layout.addWidget(self.list_widget)

        # ===================== 【Buttons代码在这里，已经完成】=====================
        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)

        self.btn_add = QPushButton("添加")
        self.btn_view = QPushButton("查看")
        self.btn_edit = QPushButton("修改")
        self.btn_del = QPushButton("删除")

        btn_style = """
        QPushButton{
            padding:7px 12px;
            font-size:13px;
            border: none;
            border-radius:5px;
            background-color:#3b82f6;
            color:white;
        }
        QPushButton:hover{
            background-color:#2563eb;
        }
        """
        self.btn_add.setStyleSheet(btn_style)
        self.btn_view.setStyleSheet(btn_style)
        self.btn_edit.setStyleSheet(btn_style)
        self.btn_del.setStyleSheet(btn_style.replace("#3b82f6","#ef4444").replace("#2563eb","#dc2626"))

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_view)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_del)
        btn_layout.setSpacing(10)
        # ========================================================================

        layout.addWidget(btn_widget)
        return widget

    # ========== 按钮点击槽函数 ==========
    def on_add_click(self):
        print("【添加】按钮被点击")

    def on_view_click(self):
        print("【查看】按钮被点击")

    def on_edit_click(self):
        print("【修改】按钮被点击")

    def on_delete_click(self):
        print("【删除】按钮被点击")

    def on_date_selected(self):
        date = self.calendar.selectedDate()
        print(f"选中日期：{date.toString('yyyy-MM-dd')}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    print("✅ 窗口打开，按钮已就绪！点击按钮看cmd输出")
    sys.exit(app.exec_())
