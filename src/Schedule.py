from datetime import datetime,time,date
class Schedule: #别直接访问属性
    title = ""
    date = date(1971,1,1)
    hms = time(8,0,0)
    note = ""
    
    # 构造方法
    def __init__(self, title,date,hms,note=""):
        self.title = title
        self.date = date
        self.hms = hms
        self.note = note

    def ChangeDate(self,newDate):
        self.date = newDate
    def ChangeTime(self,newTime):
        self.hms = newTime
    def ChangeTitle(self,newTitle):
        self.title = newTitle
    def ChangeNote(self,newNote):
        self.note = newNote
    def GetInfo(self): #0：标题 1：日期 2：时间 3：备注
        return (self.title,self.date,self.hms,self.note)
