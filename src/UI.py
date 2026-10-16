from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QCalendarWidget,
    QDialog, QDialogButtonBox, QFormLayout, QLineEdit,
    QMessageBox, QTextEdit, QTimeEdit,
)
from datetime import date, datetime, time
import sys

from Schedule import Schedule         
from Backend import Backend


class UI(QWidget):
    

    _instance = None
    selectedSchedule = None

    
    @classmethod
    def Instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        
        super().__init__()

        self.setWindowTitle("日程管理系统")
        self.resize(760, 540)

        self.selectedSchedule = None
        main_layout = QHBoxLayout(self)

        self.calendar = self.CreateCalendar()


        right_panel = self.CreateRightPanel()

        main_layout.addWidget(self.calendar)
        main_layout.addWidget(right_panel)

        today = date.today()
        self.calendar.setSelectedDate(QDate(today.year, today.month, today.day))
        self.SelectDate(today)
        self.DisplayScheduleInfoOfDay()

    def CreateCalendar(self):
        """创建日历控件（含年月切换、星期/天数显示、当天标注）。"""
        calendar = QCalendarWidget()
        calendar.setGridVisible(True)
        calendar.setStyleSheet("font-size:14px;")
        calendar.setMinimumWidth(380)
        calendar.selectionChanged.connect(self.on_date_selected)
        return calendar

    def CreateRightPanel(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title_label = QLabel("📋 日程列表")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size:16px; font-weight:bold; padding:10px;")
        layout.addWidget(title_label)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("font-size:14px;")
        self.list_widget.itemClicked.connect(self.on_list_item_clicked)
        layout.addWidget(self.list_widget)

        # 选中日程的详细信息
        self.detail_label = QLabel("")
        self.detail_label.setWordWrap(True)
        self.detail_label.setStyleSheet("font-size:13px; color:#374151; padding:6px;")
        layout.addWidget(self.detail_label)

        layout.addWidget(self.CreateButtons())
        return widget

    def CreateButtons(self):
        """创建底部按钮（含样式与信号接线）。"""
        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)

        self.btn_add = QPushButton("添加")
        self.btn_view = QPushButton("查看")
        #self.btn_edit = QPushButton("修改")
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
        for btn in (self.btn_add, self.btn_view):#,self.btn_edit
            btn.setStyleSheet(btn_style)
        self.btn_del.setStyleSheet(
            btn_style.replace("#3b82f6", "#ef4444").replace("#2563eb", "#dc2626")
        )

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_view)
        #btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_del)
        btn_layout.setSpacing(10)

        # ========== 按钮信号绑定（接线）==========
        self.btn_add.clicked.connect(self.on_add_click)
        self.btn_view.clicked.connect(self.on_view_click)
        #self.btn_edit.clicked.connect(self.on_edit_click)
        self.btn_del.clicked.connect(self.on_delete_click)

        return btn_widget

    # ==================== 日期 / 日程 选择 ====================
    def on_date_selected(self):
        """日历上选日期 -> 写入 Backend -> 刷新当天日程列表。"""
        qdate = self.calendar.selectedDate()
        target = date(qdate.year(), qdate.month(), qdate.day())
        print(f"选中日期：{target.isoformat()}")
        self.SelectDate(target)
        self.DisplayScheduleInfoOfDay()

    def SelectDate(self, target_date):
        """点击日历某日后，选择日期"""
        if target_date is not None:
            Backend.Instance.targetDate = target_date

    def on_list_item_clicked(self, item):
        """列表项被点击 -> 取出绑定的日程对象。"""
        self.SelectSchedule(item.data(Qt.UserRole))

    def SelectSchedule(self, schedule):
        """点击日程列表上的某个日程后，选择日程。出于对pyqt界面自身考虑，移除取消选择功能"""
        if schedule is None:
            return
        if self.selectedSchedule is not schedule:
            self.selectedSchedule = schedule
            if schedule not in Backend.Instance.selectedScheduleList:
                Backend.Instance.selectedScheduleList.append(schedule)
        """else:
            self.selectedSchedule = None
            if schedule in Backend.Instance.selectedScheduleList:
                Backend.Instance.selectedScheduleList.remove(schedule)"""
        self.DisplayScheduleInfo()

    # ==================== 信息显示 ====================
    def DisplayScheduleInfo(self):
        """显示当前选中日程的详细信息"""
        if self.selectedSchedule is not None:
            info = self.selectedSchedule.GetInfo()
            self.detail_label.setText("  ".join(str(i) for i in info))
            print("选中日程：", info)
        else:
            self.detail_label.setText("")

    def DisplayScheduleInfoOfDay(self, target_date=None):
        """显示指定日期（默认 Backend.targetDate）的日程列表。"""
        if target_date is None:
            target_date = Backend.Instance.targetDate

        self.list_widget.clear()
        for schedule in Backend.Instance.scheduleList:
            if not self._is_schedule_on_date(schedule, target_date):
                continue
            item = QListWidgetItem(self._schedule_text(schedule))
            item.setData(Qt.UserRole, schedule)   # 把日程对象挂在列表项上
            self.list_widget.addItem(item)

        # 选中的日程可能已不在当前列表中，同步一下详情显示
        self.DisplayScheduleInfo()

    # -------- 适配 Schedule 对象的辅助方法（按实际结构微调即可） --------
    @staticmethod
    def _schedule_date(schedule):
        """尽量从日程对象中取出日期，取不到返回 None。"""
        for attr in ("date", "targetDate", "Date"):
            if hasattr(schedule, attr):
                value = getattr(schedule, attr)
                return value() if callable(value) else value
        for method in ("GetDate", "getDate"):
            if hasattr(schedule, method):
                return getattr(schedule, method)()
        return None

    @classmethod
    def _is_schedule_on_date(cls, schedule, target_date):
        """判断日程是否属于目标日期。"""
        s_date = cls._schedule_date(schedule)
        if s_date is None or target_date is None:
            return True                    # 判断不了就不过滤，避免漏显示
        if isinstance(s_date, datetime):
            s_date = s_date.date()
        if isinstance(s_date, str):
            return s_date.startswith(str(target_date))
        return s_date == target_date

    @staticmethod
    def _schedule_text(schedule):
        """列表项显示文本：优先取标题。

        注意 Schedule 类没有 GetTitle()，只有 title 属性和 GetInfo()，
        所以这里要额外兜底取 title，否则列表会显示成 <Schedule object at 0x...>。
        """
        for method in ("GetTitle", "GetName", "getTitle"):
            if hasattr(schedule, method):
                return str(getattr(schedule, method)())
        title = getattr(schedule, "title", None)
        if title:
            return str(title)
        return str(schedule)

    # ==================== 按钮点击槽函数 ====================
    def on_add_click(self):
        print("【添加】按钮被点击")
        self.ScheduleCreateWindow()

    def on_view_click(self):
        print("【查看】按钮被点击")
        if self.selectedSchedule is None:
            print("请先在列表中选择一个日程")
            return
        self.ScheduleCreateWindow(self.selectedSchedule)

    """def on_edit_click(self): 与查看功能重复，移除
        print("【修改】按钮被点击")
        if self.selectedSchedule is None:
            print("请先在列表中选择一个日程")
            return
        # TODO: 打开修改对话框，改完调用 self.DisplayScheduleInfoOfDay()"""

    def on_delete_click(self):
        print("【删除】按钮被点击")
        if self.selectedSchedule is None:
            print("请先在列表中选择一个日程")
            return
        
        Backend.Instance.scheduleList.remove(self.selectedSchedule)
        self.selectedSchedule = None
        self.DisplayScheduleInfoOfDay()

    def ScheduleCreateWindow(self,schedule = None):
        """添加日程弹窗：输入标题 / 时间 / 备注，确定后写入 Backend.Instance。

        - 日期取自日历当前选中日（Backend.Instance.targetDate），弹窗里只展示不可改；
        - 时间用 QTimeEdit 输入，再转成 datetime.time 存进 Schedule.hms；
        - 返回新建的 Schedule 对象；用户取消或标题为空时返回 None。
        """
        targetDate = Backend.Instance.targetDate

        dialog = QDialog(self)
        dialog.setWindowTitle("添加日程")
        dialog.setMinimumWidth(360)

        form = QFormLayout(dialog)

        title_edit = QLineEdit(dialog)
        title_edit.setPlaceholderText("必填，例如：小组会议")
        title_edit.setText(schedule.title if schedule else "")
        form.addRow("标题：", title_edit)

        now = QTime.currentTime()
        time_edit = QTimeEdit(dialog)
        time_edit.setDisplayFormat("HH:mm")                     # 24 小时制
        time_edit.setTime(schedule.hms if schedule else QTime(now.hour(), now.minute()))      # 秒归零，存的就是看到的
        
        form.addRow("时间：", time_edit)

        note_edit = QTextEdit(dialog)
        note_edit.setPlaceholderText("可留空")
        note_edit.setFixedHeight(70)
        note_edit.setText(schedule.note if schedule else "")
        form.addRow("备注：", note_edit)

        form.addRow("日期：", QLabel(str(targetDate), dialog))

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog
        )
        buttons.button(QDialogButtonBox.Ok).setText("确定")
        buttons.button(QDialogButtonBox.Cancel).setText("取消")
        form.addRow(buttons)

        def on_ok():
            """标题为空就留在弹窗里提示，先别关。"""
            if not title_edit.text().strip():
                QMessageBox.warning(dialog, "提示", "标题不能为空")
                return
            dialog.accept()

        buttons.accepted.connect(on_ok)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec_() != QDialog.Accepted:
            print("已取消添加日程")
            return None

        # ---------- 收集输入 ----------
        title = title_edit.text().strip()
        qt_time = time_edit.time()
        # QTime -> datetime.time
        hms = time(qt_time.hour(), qt_time.minute(), qt_time.second())
        note = note_edit.toPlainText().strip()

        newSchedule = Schedule(title, targetDate, hms, note)
        if schedule is not None:
            # 如果是查看/修改模式，先删除旧日程再添加新日程
            if schedule in Backend.Instance.scheduleList:
                Backend.Instance.scheduleList.remove(schedule)
        Backend.Instance.AddSchedule(newSchedule)

        self.DisplayScheduleInfoOfDay()          # 刷新右侧当天的日程列表
        
        return newSchedule

    # ==================== 兼容旧接口 ====================
    def CreateWindow(self):
        """兼容第一个类的旧接口：显示窗口（QApplication 需已创建）。"""
        self.show()
        return self

    def closeEvent(self, event):
        UI._instance = None
        super().closeEvent(event)

    
    
