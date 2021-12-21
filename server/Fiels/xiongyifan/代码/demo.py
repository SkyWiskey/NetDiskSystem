# from openpyxl import Workbook,load_workbook
#
# workbook = load_workbook('1.xlsx')
#
# sheet = workbook.active
#
# for i in sheet.iter_rows(1):
#     print(i[0].value)
# import time,datetime
#
# print(time.strftime('%Y-%m-%d %X'))
# print(datetime.datetime.now())

# username = 'liwanyu'
#
#
# text = input(f"({username or '未登录'})>>> ")
# import os
# file = r'D:\python project\project\高级编程\网络编程\NetDiskSystem\client\core\handler.py'
# print(os.path.dirname(file))
import time
length = 1
while length < 11:
    print('■'*length,f'...  进度{length*10}%',end='\n')
    time.sleep(0.25)
    length += 1