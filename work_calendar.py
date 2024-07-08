import chinese_calendar as c_calendar
import calendar
import datetime


class Calendar:
    def __init__(self, year, month):
        self.year = int(year)
        self.month = int(month)
        self.days_num = calendar.monthrange(self.year, self.month)[1]
        self.workdays_num = 0
        self.dayoff_num = 0
        self.workdays_list = []
        self.dayoff_list = []

    def days_analyse(self):
        for day in range(1, self.days_num + 1):
            # 判断是否是法定工作日
            d = datetime.datetime(year=self.year, month=self.month, day=day)
            if c_calendar.is_workday(d):
                self.workdays_num += 1
                self.workdays_list.append(d)
            else:
                self.dayoff_num += 1
                self.dayoff_list.append(d)


if __name__ == '__main__':
    c = Calendar(2024, 7)
    c.days_analyse()
