from UI import UI
import Schedule
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QCalendarWidget,
)
import sys
def main():
    app = QApplication(sys.argv)
    # UI.Instance() 是类方法，返回全局唯一的窗口对象
    window = UI.Instance()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
