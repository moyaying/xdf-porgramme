# importe required libraries
import openpyxl
import re
import json
import csv

# open given workbook
# and store in excel object
# excel = openpyxl.load_workbook("Test.xlsx")
excel = openpyxl.load_workbook("../sample/sample.xlsx")

# select the active sheet
sheet = excel.active

fo = open("../out/type_enum.txt", "w")
i = 0
typeEnum = dict()
for col in sheet.columns:
    title = col[0].value
    if type(title) != str:
        continue
    if str(title).find('去掉') != -1:
        continue
    if type(title) == str and (str.find(title, '枚举') != -1 or str.find(title, '虚拟') != -1):
        # print(title)
        s = set()
        for k in range(1, len(col)):
            item = col[k]
            s.add(item.value)
        # print(len(s), ' ')
        dic = dict([(item, index) for index, item in enumerate(s)])
        # print(str(dic))
        typeEnum[title] = dic

        if str.find(title, '枚举') != -1:
            fo.write(title)
            fo.write('\n')
            fo.write(str(dic))
            fo.write('\n\n')
        # fo.write(str(typeEnum))

fo.close()

# writing the data in csv file
# writer object is created
col = csv.writer(open("../out/tt.csv",
                      'w',
                      newline=""))
valued_rows = []
valued_name = dict()
expandN = dict()  # 年月日
v_expend = dict()
v_expend_title = dict()
i = 0
for r in sheet.rows:
    # row by row write
    # operation is perform
    # col.writerow([cell.value for cell in r])
    row_data = []
    if i == 0:  # 标题
        for i in range(0, len(r)):
            title = r[i].value
            if type(title) != str or title.find('去掉') != -1:
                continue
            if (str(title).find('枚举') != -1 or str(title).find('虚拟') != -1) and len(typeEnum[title]) == 1:
                continue
            if str(title).find('年月日') != -1:
                expandN[i] = 4
                for k in range(1, expandN[i]):
                    index = i * 100 + k
                    title_sub = str(title) + str(k)
                    valued_rows.append(index)
                    valued_name[index] = title_sub
                    row_data.append(title_sub)
            elif str(title).find('虚拟') != -1:
                v_expend[i] = len(typeEnum[title])
                v_expend_title[i] = title
                v = 0
                for key in typeEnum[title].keys():
                    if v == len(typeEnum[title]) - 1:  # 最后一个不用
                        break
                    title_sub = str(title) + str(key)
                    valued_rows.append(v + 1000)
                    valued_name[v + 1000] = title_sub
                    row_data.append(title_sub)
                    v = v + 1
            else:
                valued_rows.append(i)
                valued_name[i] = title
                row_data.append(title)

            with open('../out/titles.txt', 'w') as filehandle:
                json.dump(row_data, filehandle)
    else:
        for i in range(0, len(r)):
            value = r[i].value
            if i in expandN:
                for k in range(1, expandN[i]):
                    index = i * 100 + k
                    obj = re.search(r'(\d{4}).(\d{2}).(\d{2})', str(value), re.M | re.I)
                    value_2 = obj.group(k)
                    row_data.append(int(value_2))
            elif i in v_expend:
                v = 0
                for key in typeEnum[v_expend_title[i]].keys():
                    if v == len(typeEnum[v_expend_title[i]]) - 1:  # 最后一个不用
                        break
                    # value_2 = typeEnum[v_expend_title[i]][key]
                    if str(value) == str(key):
                        row_data.append(1)
                    else:
                        row_data.append(0)
                    v = v + 1
            elif i in valued_rows:
                if str(valued_name[i]).find('只需数字') != -1:  # 格式支持: （xxx12xxx）
                    searchObj = re.search(r'（\D*(\d+)\D*）', str(value), re.M | re.I)
                    value = searchObj.group(1)
                elif str(valued_name[i]).find('枚举') != -1:
                    value = typeEnum[valued_name[i]][value]
                elif str(valued_name[i]).find('年月日') != -1:  # 格式支持: xxxx-xx-xx
                    print(value)
                    obj = re.search(r'(\d{4}).(\d{2}).(\d{2})', str(value), re.M | re.I)
                    value = obj.group(1)
                row_data.append(value)
    col.writerow(row_data)
    i = i + 1
