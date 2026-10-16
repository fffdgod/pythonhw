from datetime import date


class Backend:
    """日程数据后端（全局唯一实例，见文件末尾）。"""

    scheduleList = []          # 日程列表
    targetDate = date.today()  # 当前选中日期
    selectedScheduleList = []  # 选中日程列表

    def DeleteSchedules(self):
        for i in range(len(self.selectedScheduleList)):
            if self.selectedScheduleList[i] in self.scheduleList:
                self.scheduleList.remove(self.selectedScheduleList[i])
    def AddSchedule(self, schedule):
        self.scheduleList.append(schedule)

# ---------------- 单例 ----------------
# 原来写的是 @staticmethod 套 @property，这个组合在 Python 里无效：
# 类属性取到的是装饰器对象本身，而不是实例，所以会报
#   AttributeError: module 'Backend' has no attribute 'Instance'
# 改成模块导入时直接建好唯一实例，两种导入写法都能用：
#   from Backend import Backend  ->  Backend.Instance   （UI.py 现在用的这种）
#   import Backend               ->  Backend.Instance   （另一种写法）
# 注意：这里 Instance 是“对象”不是“方法”，使用时不加括号。
Instance = Backend()
Backend.Instance = Instance
