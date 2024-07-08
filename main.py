import os
import re

from saturation_analysis import Saturation
from work_calendar import Calendar

CURRENT_PATH = os.getcwd()
INPUT_DIR = os.path.join(CURRENT_PATH, 'input')


def get_file_name():
    if os.listdir(INPUT_DIR):
        return os.listdir(INPUT_DIR)[0]
    return None


def get_input_file():
    file_name = get_file_name()
    if file_name:
        return os.path.join(INPUT_DIR, file_name)
    return None


def get_year_month(file_name):
    match = re.search(r'上下班打卡_.*?(\d{4})(\d{2})\d{2}-', file_name)
    if match:
        year = match.group(1)
        month = match.group(2)
        return year, month
    return None


if __name__ == '__main__':
    input_file = get_input_file()
    file_name = get_file_name()

    year, month = get_year_month(file_name)
    calendar = Calendar(year, month)
    calendar.days_analyse()

    st = Saturation(calendar)
    result = st.analysis(input_file)

    if not os.path.exists('output'):
        os.makedirs('output')
    result.to_csv(os.path.join(CURRENT_PATH, 'output/result.csv'), index=False)
    print("finish!")

