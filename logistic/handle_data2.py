import os

import openpyxl
import re
import csv
import json
from libs import files

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
        print(item_value, index)
        item_data_define['data'][item_value] = index
        item_data_define["index"] = index + 1
    else:
        index = item_data_define['data'][item_value]

    size = item_data_define["size"]
    zones = [0] * size
    zones[index] = 1
    return zones[:-1]


def handle_cell(row_n, data):
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
        # if data == "无":
        #     return [0]
        # else:
        #     return [1]
        pass
    elif row_n == 7:  # 班级标价
        return [data]
    elif row_n == 8:  # 实缴金额
        return [data]
    elif row_n == 9:  # 平均实缴金额
        return [data]
    elif row_n == 10:  # 标准部门
        # key = "标准部门"
        # idx = add_enum(key, ['少儿部'], 1, data)
        # return [idx]
        pass
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
        # v = add_virtual("科目", data)  # 使用虚拟变量
        # return v
    elif row_n == 13 or row_n == 14:  # 开课日期, 结课日期.  格式支持: xxxx-xx-xx, xxxx/xx/xx
        # obj = re.search(r'(\d{4}).(\d{2}).(\d{2})', str(data), re.M | re.I)
        # values = obj.groups()
        # return [values[0], int(values[1]), int(values[2])]
        pass
    elif row_n == 15:  # 教学区, 虚拟
        # return add_virtual("教学区", data)
        pass
    elif row_n == 16:  # 班级归属
        # obj = re.search(r'\D*(\d+).*', str(data), re.M | re.I)
        # values = obj.groups()
        # return [values[0]]
        pass
    elif row_n == 17:  # 离班课次
        return [data]
    elif row_n == 18:  # 课次
        return [data]
    elif row_n == 19:  # 授课方式
        # key = "授课方式"
        # idx = add_enum(key, ['线上'], 1, data)
        # return [idx]
        pass
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
        # key = "主代课教师"
        # idx = add_enum(key, None, 1, data)
        # return [idx]
        pass
        # teachers = add_virtual("主代课教师", data)
        # return teachers
    elif row_n == 26:  # 是否管理者
        if data == '管理者':
            return [1]
        return [0]
    elif row_n == 27:  # 教师教龄（月）
        return [data]
    elif row_n == 28:  # 教师性别
        if data == "女":
            return [1]
        return [0]
    elif row_n == 29:  # 所学专业
        # key = "所学专业"
        # idx = add_enum(key, None, 1, data)
        # return [idx]
        pass
    elif row_n == 30:  # 毕业院校
        # key = "毕业院校"
        # idx = add_enum(key, None, 1, data)
        # return [idx]
        pass
    elif row_n == 31:  # 是否是四类人才
        if data == "是":
            return [1]
        return [0]
    elif row_n == 32:  # 岗位名称
        # key = "岗位名称"
        # idx = add_enum(key, None, 1, data)
        # return [idx]
        pass
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


def handle_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    sample_dir = os.path.join(root_dir, "sample")

    excel = openpyxl.load_workbook(filename=os.path.join(sample_dir, "sample2.xlsx"), read_only=True)
    ws = excel.active

    sample_logistic_out = os.path.join(root_dir, "out", "logistic")
    files.mkdir(sample_logistic_out)
    with open(os.path.join(sample_logistic_out, "sample2.csv"), 'w', newline="", encoding='utf-8-sig') as cvs_file:
        csv_col = csv.writer(cvs_file)

        line_num = 0
        titles = []
        for rows in ws.rows:
            # 标题titles
            if line_num == 0:
                titles = []
                for row_num in range(0, len(rows)):
                    title = rows[row_num].value
                    if row_num in [0, 1, 2, 4, 5, 6, 10, 13, 14, 15, 16, 19, 20, 21, 24, 25, 29, 30, 32]:  # ignore
                        pass
                    # elif row_num == 25:
                    #     titles.extend(new_virtual("主代课教师", 253))
                    # elif row_num == 12:  # 科目，使用虚拟变量
                    #     titles.extend(new_virtual("科目", 3))
                    # elif row_num == 13 or row_num == 14:  # 开课日期, 结课日期
                    #     titles.extend([title + '-年', title + '-月', title + '-日'])
                    # elif row_num == 15:  # 教学区, 虚拟
                    #     titles.extend(new_virtual("教学区", 10))
                    else:
                        titles.append(title)
                csv_col.writerow(titles)
            else:  # 处理row数据
                row_data = []
                for row_num in range(0, len(rows)):
                    item = rows[row_num].value
                    if row_num == 0 and item is None:  # 学员号是 None 则 当作空行
                        break
                    cell_data = handle_cell(row_num, item)
                    row_data.extend(cell_data)
                if len(row_data) > 0:
                    csv_col.writerow(row_data)
            line_num = line_num + 1

        # 写titles
        with open(os.path.join(sample_logistic_out, "sample2_titles.txt"), 'w') as filehandle:
            json.dump(titles, filehandle)

        # 写入映射关系
        with open(os.path.join(sample_logistic_out, "sample2_data_mapping.txt"), "w") as fo:
            fo.write(str(data_define))
            fo.close()


if __name__ == '__main__':
    handle_data()
