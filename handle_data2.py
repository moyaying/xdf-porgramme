import openpyxl
import re
import csv
import json

data_define = {}


def add_enum(key_name, begin_values, begin_index, item_value):
    """
    添加枚举元素
    :return:
    """
    if key_name not in data_define:
        data_define[key_name] = {"type": "enum", "data": {},
                                 "index": begin_index + len(begin_values) if begin_values is not None else begin_index}

    index = begin_index
    item_data_define = data_define[key_name]
    if item_value not in item_data_define['data']:
        index = item_data_define["index"]
        if begin_values is not None and item_value in begin_values:
            index = begin_values.index(item_value) + begin_index
        else:
            item_data_define["index"] = index + 1
        item_data_define['data'][item_value] = index
    else:
        index = item_data_define['data'][item_value]

    return index


def new_virtual(key_name, size):
    if key_name not in data_define:
        data_define[key_name] = {"type": "virtual", "data": {}, "index": 0, "size": size}
    return [key_name + '-' + str(i) for i in range(size - 1)]


def add_virtual(key_name, item_value):
    item_data_define = data_define[key_name]
    index = item_data_define["index"]
    if item_value not in item_data_define['data']:
        item_data_define['data'][item_value] = index
        item_data_define["index"] = index + 1
    else:
        index = item_data_define['data'][item_value]

    size = item_data_define["size"]
    zones = [0] * size
    zones[index] = 1
    return zones[:-1]


# 教学区
zoneSize = 10
zoneIdx = 0
teachingZone = {}


def handle_cell(line_n, row_n, data):
    if row_n == 0:  # 学员号
        pass  # ignore
    elif row_n == 1:  # 班级编码
        pass  # ignore
    elif row_n == 2:  # 班级名称
        pass  # ignore
    elif row_n == 3:  # 班型, 枚举（志高 1， 精进 2）
        key = "班型"
        idx = add_enum(key, ['志高', '精进'], 1, data)
        return [idx]
    elif row_n == 4:  # 进班日期
        pass
    elif row_n == 5:  # 离班日期
        pass
    elif row_n == 6:  # 离班类型
        if data == "无":
            return [0]
        else:
            return [1]
    elif row_n == 7:  # 班级标价
        return [data]
    elif row_n == 8:  # 实缴金额
        return [data]
    elif row_n == 9:  # 平均实缴金额
        return [data]
    elif row_n == 10:  # 标准部门
        key = "标准部门"
        idx = add_enum(key, ['少儿部'], 1, data)
        return [idx]
    elif row_n == 11:  # 年级
        if data == "二年级":
            return [2]
        elif data == "三年级":
            return [3]
        elif data == "四年级":
            return [4]
        elif data == "五年级":
            return [5]
        elif data == "六年级":
            return [6]
        elif data == "初一":
            return [7]
        elif data == "初二":
            return [8]
        elif data == "初三":
            return [9]
        else:
            return [1]
    elif row_n == 12:  # 科目
        key = "科目"
        idx = add_enum(key, ['语文', '数学'], 1, data)
        return [idx]
    elif row_n == 13 or row_n == 14:  # 开课日期, 结课日期.  格式支持: xxxx-xx-xx, xxxx/xx/xx
        obj = re.search(r'(\d{4}).(\d{2}).(\d{2})', str(data), re.M | re.I)
        values = obj.groups()
        return [values[0], int(values[1]), int(values[2])]
    elif row_n == 15:  # 教学区, 虚拟
        return add_virtual("教学区", data)
    elif row_n == 16:  # 班级归属
        obj = re.search(r'\D*(\d+).*', str(data), re.M | re.I)
        values = obj.groups()
        return [values[0]]
    elif row_n == 17:  # 离班课次
        return [data]
    elif row_n == 18:  # 课次
        return [data]
    elif row_n == 19:  # 授课方式
        key = "授课方式"
        idx = add_enum(key, ['线上'], 1, data)
        return [idx]
    elif row_n == 20:  # 在读学校
        pass
    elif row_n == 21:  # 财年
        pass
    elif row_n == 22:  # 进班课次
        return [data]
    elif row_n == 23:  # 是否报下个季度
        if data == "是":
            return [1]
        else:
            return [0]
    elif row_n == 24:  # 学员编号+科目
        pass
    elif row_n == 25:  # 主代课教师
        key = "主代课教师"
        idx = add_enum(key, None, 1, data)
        return [idx]
    elif row_n == 26:  # 是否管理者
        if data == '管理者':
            return [1]
        return [0]
    elif row_n == 27:  # 教师教龄（月）
        return [data]
    elif row_n == 28:  # 教师性别
        if data == "男":
            return [1]
        return [0]
    elif row_n == 29:  # 所学专业
        key = "所学专业"
        idx = add_enum(key, None, 1, data)
        return [idx]
    elif row_n == 30:  # 毕业院校
        key = "毕业院校"
        idx = add_enum(key, None, 1, data)
        return [idx]
    elif row_n == 31:  # 是否是四类人才
        if data == "是":
            return [1]
        return [0]
    elif row_n == 32:  # 岗位名称
        key = "岗位名称"
        idx = add_enum(key, None, 1, data)
        return [idx]
    elif row_n == 33:  # 学历
        key = "学历"
        idx = add_enum(key, ['大专', '本科', '硕士研究生', '博士研究生'], 1, data)
        return [idx]
    elif row_n == 34:  # 学员前三季度是否报读
        if data == "是":
            return [1]
        return [0]
    elif row_n == 35:  # 学员本次报读前报读过多少次本科目
        return [data]
    elif row_n == 36:  # 学员本次报读前报读过多少次全部科目
        return [data]

    return []


excel = openpyxl.load_workbook(filename="sample/sample2.xlsx", read_only=True)
ws = excel.active

csv_col = csv.writer(open("out/sample2.csv", 'w', newline=""))

line_num = 0
titles = []
for rows in ws.rows:
    # 标题titles
    if line_num == 0:
        titles = []
        for row_num in range(0, len(rows)):
            title = rows[row_num].value
            if row_num in [0, 1, 2, 4, 5, 20, 21, 24]:  # ignore
                pass
            elif row_num == 13 or row_num == 14:  # 开课日期, 结课日期
                titles.extend([title + '-年', title + '-月', title + '-日'])
            elif row_num == 15:  # 教学区, 虚拟
                titles.extend(new_virtual("教学区", 10))
            else:
                titles.append(title)
        csv_col.writerow(titles)
    else:  # 处理row数据
        row_data = []
        for row_num in range(0, len(rows)):
            item = rows[row_num].value
            if row_num == 0 and item is None:  # 学员号是 None => 空行
                break
            cell_data = handle_cell(line_num, row_num, item)
            row_data.extend(cell_data)
        csv_col.writerow(row_data)
    line_num = line_num + 1

# 写titles
with open('./out/sample2_titles.txt', 'w') as filehandle:
    json.dump(titles, filehandle)

# 写入映射关系
fo = open("out/sample2_data_mapping.txt", "w")
fo.write(str(data_define))
fo.close()
