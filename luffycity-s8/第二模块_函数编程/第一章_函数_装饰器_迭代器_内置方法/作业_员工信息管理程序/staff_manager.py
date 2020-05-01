#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/13
# Location: DongGuang
# Desc:     第二模块作业<员工信息管理程序>


import os
import platform
import hashlib
import copy
from tabulate import tabulate


def Help(help_cmd):
    """
    帮助信息
    :param help_cmd:
    :return:
    """
    help_msg = """
    help加以下参数查看相关语句帮助信息
        find or -f   : 查询语句
        del or -d    : 删除语句
        add or -a    : 添加语句
        update or -u : 更新语句
        
           exit or q : 退出程序
    """
    help_find_msg = """
    >>>可进行模糊查询，支持以下查询语法，支持[=,>,<,>=,<=,like]判断语法:
        find name,age from staff_table where age > 22
        find * from staff_table where dept = "IT"
        find * from staff_table where enroll_date like "2013"
        find * from staff_table
    """
    help_add_msg = """
    >>>可新增纪录，以phone做唯一键，staff_id自增
        add staff_table Alex Li,25,134435344,IT,2015‐10‐29
    """
    help_del_msg = """
    >>>可删除指定条件纪录(不写where条件将删除表中所有数据)
        del from staff_table where id=3
    """
    help_update_msg = """
    >>>可修改员工信息(不写where条件将更新表中所有数据)
        update staff_table set dept="Market" where dept = "IT"
        update staff_table set age=25 where name = "Alex Li"
    """

    if help_cmd.strip() in ['help', 'h', 'H']:
        Log(help_msg)
    elif help_cmd.strip() in ['help find', 'help -f']:
        Log(help_find_msg)
    elif help_cmd.strip() in ['help add', 'help -a']:
        Log(help_add_msg)
    elif help_cmd.strip() in ['help del', 'help -d']:
        Log(help_del_msg)
    elif help_cmd.strip() in ['help update', 'help -u']:
        Log(help_update_msg)
    else:
        Log('没有这个选项')
        return False


def Log(msg, msg_type='help'):
    """
    输出日志
    :param msg_type: eg. error|info|help
    :param msg: log message
    :return:
    """
    if msg_type == 'error':
        print('\033[1;31m[ERROR]: {}\033[0m'.format(msg))
    elif msg_type == 'help':
        print('\033[1;34m[HELP]: {}\033[0m'.format(msg))
    else:
        print('\033[1;32m[INFO]: {}\033[0m'.format(msg))


def LoadStaffDB(file):
    """
    加载用户信息到内存
    :param file: STAFF_DB
    :return: staff_data
    """

    staff_data = {}
    for column in DB_COLUMN:
        staff_data[column] = []

    try:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                staff_id, name, age, phone, dept, in_date = line.strip().split(',')
                staff_data['id'].append(staff_id)
                staff_data['name'].append(name)
                staff_data['age'].append(age)
                staff_data['phone'].append(phone)
                staff_data['dept'].append(dept)
                staff_data['in_date'].append(in_date)
    except FileNotFoundError:
        exit('[{}]文件不存在，请检查'.format(file))

    return staff_data


def SaveStaffDB(file, save_staff_data):
    """
    把修改后的数据写到文件数据库
    :param file: 在存入的文件
    :param save_staff_data: 要存档的数据表
    :return:
    """
    dict_to_list = []
    new_file = '{}.new'.format(file)

    # 检测员工表有没有被修改，有修改在才保存操作
    STAFF_DATA_MD5_B = CheckMd5(STAFF_DATA)
    if STAFF_DATA_MD5_B == STAFF_DATA_MD5_A:
        Log("### You haven't made any changes, with no needs for save it", 'info')
        return None

    # 把数据字典转成列表（去掉字典的key)
    for k in DB_COLUMN:  # 在做列表转换时一定要用DB_COLUMN里面的字段来对应
        dict_to_list.append(save_staff_data[k])

    # 转成一个员工一行的列表
    new_list = DisplayDataTransform(dict_to_list)

    # 把每个员工的子列表取出来转成字符串，然后存入文件
    with open(new_file, 'w', encoding='utf-8') as save_f:
        for i in new_list:
            save_line = ','.join(i)
            save_f.write(save_line + '\n')

    # 存档后，将新库文件改名为旧库名 user_db.new => user_db
    if platform.system() == 'Windows':  # windows上不能用rename覆盖一个存在的文件
        os.remove(file)
    try:
        os.rename(new_file, file)
    except OSError as e:
        Log(e, 'error')


def MakeTempDict():
    """
    创建包含所有列的的初始字典用于存放各where条件匹配的脏数据
    :return: 包含key的字典
    """
    temp_dict = {}
    for i in DB_COLUMN:
        temp_dict[i] = []
    return temp_dict


def DisplayDataTransform(init_data):
    """
    转换最终匹配的数据格式使其能用tabulate展示出来
    :param init_data: eg. [[1,3,4,5],[22,33,44,55],['zayne','wayne','payne','rain']]
    :return: show_data eg. [[1,22,'zayne'],[3,33,'wayne'],[4,44,'payne'],[5,55,'rain']]
    """
    show_data = []
    if len(init_data) > 0 and len(init_data[0]) > 0:
        for i in range(len(init_data[0])):
            s = [init_data[k][i] for k in range(len(init_data))]
            show_data.append(s)
    return show_data


def IsNumber(text):
    """
    检查是否是数字
    :param text: eg. 12|abc|IT
    :return:  True or False
    """
    try:
        float(text)
        return True
    except ValueError:
        return False


def CheckMd5(data):
    """
    计算员工信息表MD5值,用于在程序中判断有没有做修改
    :param data:
    :return:
    """
    data_md5 = hashlib.md5(str(data).encode('utf-8'))
    hex_md5 = data_md5.hexdigest()
    return hex_md5


def ConditionMatch(con_col, con_val, con_decide):
    """
    条件匹配
    :param con_col:  eg. age,name,phone,...
    :param con_val:  eg. 22,Jushua Cheng,13636363636,...
    :param con_decide:  eg. =,>,<,like,>=,<=
    :return: matched data eg. {'age':[22,33],'name':['Jushua Cheng','Wayne Zheng'],'phone':[13636363636,18686868686]}
    """
    con_matched = MakeTempDict()

    if con_decide == '=':
        decide = 'con_val == n'
    elif con_decide == '>':
        decide = 'con_val < n'
    elif con_decide == '<':
        decide = 'con_val > n'
    elif con_decide == '>=':
        decide = 'con_val <= n'
    elif con_decide == '<=':
        decide = 'con_val >= n'
    elif con_decide == 'like':
        decide = 'con_val in n'

    for idx, n in enumerate(STAFF_DATA[con_col]):
        if con_decide in ['<', '>', '>=', '<=']:
            con_val, n = float(con_val), float(n) if IsNumber(con_val) and IsNumber(n) \
                else Log('Syntax error: < 或 > 条件判断只支持数字的关键字及字段', 'error')
        if eval(decide):
            for column in DB_COLUMN:
                con_matched[column].append(STAFF_DATA[column][idx])

    if con_matched != MakeTempDict():  # 如查条件查询后还是跟初始列表一样，说明没有匹配到数据，返回空
        return con_matched
    else:
        Log('没有找到符合条件的数据', 'info')
        return None


def AddAction(add_statement, add_staff_data):
    """
    find动作匹配
    :param add_statement:  eg. add staff_table Wayne Zheng,28,18666888866,IT,2017-09-25
    :param add_staff_data:  STAFF_DATA
    :return:
    """
    global STAFF_DATA
    # 截取新增数据字段并转为列表
    add_staff_info = add_statement.split('staff_table')[1]
    add_staff_info_list = [i.strip() for i in add_staff_info.split(',')]

    # id 自增，计算下一个id号，并把id插到 add_staff_info_list
    # max_id = len(add_staff_data['id'])
    # next_id = max_id + 1
    # 以上方法不严谨（当有删除某条数据时，用len长度来取最大的id数会有问题）
    # 用以下这种方法取当前数据表中最大的id数加1做为新增数据的id
    id_list = [int(i) for i in STAFF_DATA['id']]  # 将id列表取出并转为数字类型
    next_id = max(id_list) + 1
    add_staff_info_list.insert(0, str(next_id))

    if not IsNumber(add_staff_info_list[2]):
        Log('Syntax error: [age]字段必须要为数字', 'error')

    if not IsNumber(add_staff_info_list[3]):
        Log('Syntax error: [phone]字段必须要为数字', 'error')

    # phone为唯一键
    if add_staff_info_list[3] in add_staff_data['phone']:
        Log('Primary key conflict: [phone]字段为唯一键，[{}]号码在staff_table表中已存在'.format(add_staff_info_list[3]), 'error')
    else:
        for idx, n in enumerate(DB_COLUMN):
            add_staff_data[n].append(add_staff_info_list[idx])

        STAFF_DATA = add_staff_data  # 新增或修改的数据全部暂存在STAFF_DATA中
        SaveStaffDB(STAFF_DB, STAFF_DATA)  # 保存修改到文件
        print(tabulate([add_staff_info_list], DB_COLUMN, 'fancy_grid'))
        Log('新增[1]条数据', 'info')


def FindAction(find_statement, temp_matched_data):
    """
    add动作匹配
    :param temp_matched_data:
    eg.  {'dept': ['IT'], 'age': ['21'], 'id': ['3'], 'name': ['Rain Wang'],
          'in_data': ['2017‐04‐01'], 'phone': ['13451054608']}
    :param find_statement: eg. find * from staff_table | find name,age fro staff_table
    :return:
    """
    filter_key = find_statement.split('find')[1].split('from')[0]
    find_columns = [i.strip() for i in filter_key.split(',')]
    final_data = []

    # * 代表所有字段
    if '*' in find_columns:
        if len(find_columns) == 1:
            find_columns = DB_COLUMN
        else:
            Log('Action syntax error: * 不能与其它列同时存在！', 'error')
            return False

    # 过滤字段为空报错
    # if len(find_columns) == 1:
    #     if not find_columns[0]:
    # filter_key为空的情况下，经过split方法，会生成一个带空字符的列表:['']
    # 所以 find_columns[0]不会报错，可以用下面一条判断替代上面两层判断
    if find_columns[0] not in DB_COLUMN:
        Log('Action syntax error: find与from之间一定有字段或*', 'error')
        return False

    # 过滤find后面的列 age,name,.. 的数据暂存到新列表里面
    for i in find_columns:
        row = temp_matched_data[i]
        final_data.append(row)

    new_final_data = DisplayDataTransform(final_data)
    print(tabulate(new_final_data, find_columns, 'fancy_grid'))
    Log('查询到[{}]条数据'.format(len(new_final_data)), 'info')


def DelAction(*args):
    """
    del动作匹配
    :param args: 0:运作语句; 1:符合where条件的数据
    :return:
    """
    global STAFF_DATA
    del_staff_data = args[1]

    # 取出要删除数据的id
    del_id_list = [i for i in del_staff_data['id']]
    del_staff_data_bak = copy.deepcopy(del_staff_data)

    # 从staff_table中删除条件匹配到的id的数据
    for i in del_id_list:
        del_idx = STAFF_DATA['id'].index(i)
        for k in STAFF_DATA:
            del STAFF_DATA[k][del_idx]

    # 将条件匹配的数据转成列表，用于打印  {'key':[123,'abc'],'key2':[234,'ccd']} to [[123,'abc'],[234,'ccd']]
    del_staff_list = []
    for k in DB_COLUMN:  # 这里一定要用 DB_COLUMN 这个列表来取key, 不然后期字段与值不能对应
        del_staff_list.append(del_staff_data_bak[k])

    del_list = DisplayDataTransform(del_staff_list)
    SaveStaffDB(STAFF_DB, STAFF_DATA)  # 保存修改到文件
    print(tabulate(del_list, DB_COLUMN, 'fancy_grid'))
    Log('删除了[{}]条数据'.format(len(del_list)), 'info')


def UpdateAction(update_statement, update_staff_data):
    """
    update动作匹配
    :param update_statement:
    :param update_staff_data:
    :return:
    """
    global STAFF_DATA

    if 'set' not in update_statement:
        Log('Action syntax error: [update]语句缺少必要的[set]关键字', 'error')
        return None

    set_statement = update_statement.split('set')[1]

    if '=' not in set_statement:
        Log('Action syntax error: [update]语句中的[set]关键字值必须是用[=]]', 'error')
        return None

    # 取要set(修改)的字段与要set(修改后)的值
    set_col, set_val = set_statement.split('=')
    set_col = set_col.strip()
    set_val = set_val.replace('"', '').replace("'", "").strip()

    if set_col == 'phone' and len(update_staff_data['phone']) > 1:
        Log('Primary key conflict: [phone]字段为唯一键，不能多条数据同时改为同一个值', 'error')
        return False
    elif set_col == 'phone' and set_val in STAFF_DATA['phone']:
        Log('Primary key conflict: [phone]字段为唯一键，[{}]号码在staff_table表中已存在'.format(set_val), 'error')
        return False
    elif set_col == 'id':
        Log('Key error: [id]字段为自增字段，不可修改', 'error')
        return False

    # 取出条件匹配到的数据中的id, 再找到id在STAFF_DATA中的索引，并把要set的字段改成要set的值
    # 顺便把条件匹配到的数据也修改了
    for i in update_staff_data['id']:
        idx, idx_1 = STAFF_DATA['id'].index(i), update_staff_data['id'].index(i)
        STAFF_DATA[set_col][idx] = update_staff_data[set_col][idx_1] = set_val

    # 修改后的匹配数据转成列表用于打印
    update_staff_list = [update_staff_data[k] for k in DB_COLUMN]  # 字段顺序记住永远用DB_COLUMN的
    show_update_list = DisplayDataTransform(update_staff_list)
    SaveStaffDB(STAFF_DB, STAFF_DATA)  # 保存修改到文件
    print(tabulate(show_update_list, DB_COLUMN, 'fancy_grid'))
    Log('修改了[{}]条数据'.format(len(update_staff_data['id'])), 'info')


def WhereStatement(where_statement):
    """
    解析where条件语句，并把子句发分给各条件查询的函数查询匹配记录
    :param where_statement:
    :return:
    """
    decide_list = ['>=', '<=', '>', '<', '=', 'like']
    error_decide_list = ['==', '<<', '>>', '=>', '=<']

    for k in decide_list:

        # 检查是否有非法的判断符（避免程序崩溃）
        for i in error_decide_list:
            if i in where_statement:
                Log('Condition syntax error：错误的条件判断符[{}]'.format(i), 'error')
                return False

        if k in where_statement:
            col, val = where_statement.split(k)
            col = col.replace("'", "").replace('"', '').strip()
            val = val.replace("'", "").replace('"', '').strip()

            if col and val:  # 条件判断符号两边必须要有值并且字段是存在的才进行下一步 eg. age > 20
                if col in DB_COLUMN:
                    con_match_record = ConditionMatch(col, val, k)
                    return con_match_record
                else:
                    Log('Condition syntax error: staff_table 表中没有[{}]这个字段'.format(col), 'error')
                    return False
            else:
                Log('Condition syntax error: [where]关键字后面缺少条件语句', 'error')
    else:
        Log('Condition syntax error： 条件语句中缺少正确的判断符[=,>,<,<=,>=,like]', 'error')


def StatementAnalysis(cmd):
    """
    解析用户输入的整条语句，并把相关语法交给相关语法函数进行进一步的解析操作
    :param cmd: user_cmd
    :return:
    """
    action_list = {
        'find': FindAction,
        'add': AddAction,
        'del': DelAction,
        'update': UpdateAction
    }

    # 如果有where 关键词就根据where后面的语句进行解析匹配记录
    if cmd.split()[0] in action_list and 'staff_table' in cmd:

        action_name = cmd.split()[0]
        if action_name not in ['add', 'update'] and 'from' not in cmd:  # add,update语句不需要from关键字
            Log('Syntax error: 缺少[from]关键字', 'error')
            return False

        if 'where' in cmd:  # 有where语句，先查询满足where条件的数据
            action_statement, condition_statement = cmd.strip().split('where')
            if 'from' not in action_statement and action_name not in ['add', 'update']:
                # 检查除add update 以外的动作语句中有没有from关键字，没有就报错并退出程序
                Log('Syntax error: 查询语句缺少<from>关键字', 'error')
                return False
            match_record = WhereStatement(condition_statement.strip())
            # 条件匹配有数据则继续下一步的动作与字段过虑
            if match_record:
                action_list[action_name](action_statement, match_record)

        # 如果没where条件，则返回所有记录给对应动作继续处理
        else:
            if action_name in ['del', 'update']:
                Log('温馨提示：del/update 语句未指定where条件将更新整个表中的数据', 'info')
                yes_or_no = input('确认此次操作请按[y] 放弃此次操作请按[b]>>:')
                if yes_or_no in ['Y', 'y']:
                    action_list[action_name](cmd, STAFF_DATA)
            else:  # add/find 语句不用where关键字
                action_list[action_name](cmd, STAFF_DATA)
    else:
        Log('Syntax error: 没有相应动作或数据表，请检查', 'error')


def main():
    """
    程序主入口
    :return:
    """
    while True:
        cmd = input("输入help可获取帮助信息[Staff Manager]>>: ").strip()
        if not cmd:
            continue
        elif cmd.strip().split()[0] == 'help':
            Help(cmd)
        elif cmd.strip() in ['exit', 'q']:
            break
        else:
            StatementAnalysis(cmd)


if __name__ == '__main__':
    STAFF_DB = 'user_db'
    DB_COLUMN = ['id', 'name', 'age', 'phone', 'dept', 'in_date']
    STAFF_DATA = LoadStaffDB(STAFF_DB)
    STAFF_DATA_MD5_A = CheckMd5(STAFF_DATA)
    main()