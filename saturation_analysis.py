import re
import pandas as pd
import datetime


class Saturation:
    def __init__(self, calendar):
        self.calendar = calendar
        self.saturation_target = 1.2
        self.saturation_current = 0  # 当前饱和度

        self.standard_working_hours = 9  # 标准工作时长
        self.clock_in_avg = None  # 平均上班打卡时间
        self.clock_out_avg = None  # 平均下班打卡时间
        self.working_hours_avg = None  # 平均工作时长
        self.working_hours_sum = 0  # 当前总工作时长
        self.overtime_days_num = 0  # 加班天数
        self.workdays_num = 0  # 工作总天数
        self.abnormal_days_num = 0  # 打卡异常天数
        self.working_hours_avg_target = None  # 目标平均工作时长
        self.clock_out_target = None  # 目标下班时间

    @staticmethod
    def add_hours_to_time(base_time, hours_to_add):
        base_time_obj = datetime.datetime.strptime(base_time, '%H:%M')
        new_time_obj = base_time_obj + datetime.timedelta(hours=hours_to_add)
        new_time_str = new_time_obj.strftime('%H:%M')

        return new_time_str

    def data_format(self):
        today = datetime.date.today()
        year_and_month = f'{self.calendar.year}/{self.calendar.month}'
        data = {'统计时间': [today], '统计年月': [year_and_month], '当月天数': [self.calendar.days_num],
                '当月工作需天数': [self.calendar.workdays_num], '平均工作时长(h)': [self.working_hours_avg],
                '当前饱和度': [self.saturation_current], '工作总天数': [self.workdays_num],
                '加班天数': [self.overtime_days_num], '打卡异常天数': [self.overtime_days_num],
                '目标平均工作时长(满足饱和度大于1.2)': [self.working_hours_avg_target],
                '目标下班时间': [self.clock_out_target]}

        df = pd.DataFrame(data)
        return df

    def analysis(self, input_file):
        df = pd.read_excel(input_file, sheet_name='概况统计与打卡明细')
        for row in df.itertuples():
            date = row[1]
            date_match = re.search(r'(\d{4}/\d{2}/\d{2})', str(date))
            if date_match:
                date = date_match.group(1)
            else:
                continue
            clock_in_status = row[47]  # 上班打卡状态
            clock_out_status = row[48]  # 下班打卡状态
            if clock_in_status != '正常' and clock_out_status != '正常':
                self.abnormal_days_num += 1
                continue
            date = datetime.datetime.strptime(date, '%Y/%m/%d')
            # working_timerange = row[7]  # 上班时间范围
            # clock_in = row[8]  # 上班打卡时间
            # clock_out = row[9]  # 下班打卡时间
            self.standard_working_hours = float(row[11])  # 标准工作时长
            working_hours = row[12]  # 工作时长
            if date in self.calendar.dayoff_list:
                self.overtime_days_num += 1
            self.workdays_num += 1
            self.working_hours_sum = self.working_hours_sum + float(working_hours)

        self.working_hours_avg = self.working_hours_sum / self.workdays_num
        self.saturation_current = self.working_hours_avg / self.standard_working_hours
        workdays_remain = self.calendar.workdays_num - self.workdays_num
        working_hours_remain = (self.calendar.workdays_num * self.saturation_target * self.standard_working_hours -
                                self.working_hours_sum)
        self.working_hours_avg_target = working_hours_remain / workdays_remain
        self.clock_out_target = self.add_hours_to_time('8:30', self.working_hours_avg_target)
        return self.data_format()
