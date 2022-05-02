# 项目名称: 排座位辅助器
# 项目版本 2.0.0
# 创建时间 2022/4/23
# 创建人 Martian148
# 修改时间 2022/4/25
# 修改人 Martian148

#导入模块
import sys
#sys.path.append('C:\\Users\\qzez\\AppData\\Local\\Programs\\Python\\Python38-32\\Lib\\site-packages')



import easygui as ag
from random import *
import pytab as pt
import  os.path

# -*- coding: utf-8 -*-
# 保证中文可以显示
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

#全局变量定义
Version = ' v2.0.1'
Title = '排座位辅助器 ' + Version
init_ = {}

#主页面
def main_interface():
    choice_1 = ag.buttonbox(msg='', title='排座位辅助器'+Version, choices=('开始', '关于程序','命令行'), image='1.gif')

    name_, chair_ = [], []
    if choice_1 == '开始':
        name_, chair_ = input_information()
        ret_fraction = sort_seat(name_, chair_)
        print_pic(ret_fraction)
        end_sort()

    if choice_1 == '命令行':
        cmd_()

    if choice_1 == '关于程序':
        about_program()

#输入座位及人数信息
def input_information():
    input_name = ag.enterbox(msg='输入名单', title='排座位辅助器' + Version, default=' ', strip=True, image=None, root=None)
    name_ = input_name.split('\n')
    print(name_)

    input_chair = ag.enterbox(msg='输入座位', title='排座位辅助器v0.1' + Version, default=' ', strip=True, image=None, root=None)
    chair_ = input_chair.split('\n')
    print(chair_)

    return name_,chair_

#进行一次排座位
def sort_once(name_,chair_):
    row,col= len(chair_),len(chair_[0])
    pos = 0
    ret_chair = {}

    shuffle(name_)

    for j in range(col):
        now_col = []
        for i in range(row):
            if (chair_[i][j]=='1'):
                now_col.append(name_[pos])
                pos += 1
            else:
                now_col.append(' ')
        ret_chair[str(j)] = now_col
    return ret_chair

#读取要求文件
def read_file(row,col):
    near,set_list = [],[]
    set_ = {}

    if not os.path.isfile('.idea\define_t.xml'):
        return near,set_

    f = open('.idea\define_t.xml','r',encoding='utf-8')
    requirements_ = f.readlines()
    f.close()

    for i in range(len(requirements_)):
        if requirements_[i][len(requirements_[i])-1] == '\n':
            requirements_[i]=requirements_[i][:-1:]
    print(requirements_)
    for i in range(len(requirements_)):
        if requirements_[i][0]=='n':
            near.append(requirements_[i].split(' '))
        elif requirements_[i][0] == 's':
            set_list.append(requirements_[i].split(' '))

    for k in range(len(set_list)):
        if set_list[k][1] in set_:
            requirement_row = set_list[k][2].split(',')
            requirement_col = set_list[k][3].split(',')

            for i in range(len(requirement_row)):
                for j in range(len(requirement_col)):
                    set_[set_list[k][1]][int(requirement_row[i])][int(requirement_col[j])] = int(set_list[k][4])
        else:
            now_layout = [[0 for i in range(col)] for j in range(row)]
            requirement_row = set_list[k][2].split(',')
            requirement_col = set_list[k][3].split(',')

            for i in range(len(requirement_row)):
                for j in range(len(requirement_col)):
                    now_layout[int(requirement_row[i])][int(requirement_col[j])] = int(set_list[k][4])
            set_[set_list[k][1]] = now_layout
    print(set_)
    return near,set_

#计算此种排序权值
def calc_fraction(data,row,col,near,set_):
    fraction = 0

    for k in range(len(near)):
        for i in range(row):
            for j in range(col):
                if j == col-1:
                    break
                if (data[str(j)][i]==near[k][1] and data[str(j+1)][i]==near[k][2]) or (data[str(j)][i]==near[k][2] and data[str(j+1)][i]==near[k][1]) :
                    fraction += int(near[k][3])

    for i in range(row):
        for j in range(col):
            if data[str(j)][i] in set_:
                fraction += set_[data[str(j)][i]][i][j]
    return fraction

# 生成图片
def print_pic(print_data):
    pt.table(
        data=print_data,
        th_type='dark',
        table_type='striped'
    )
    pt.save(filename='座位表', dpi=800)

#排座位主程序
def sort_seat(name_,chair_):
    times = 10000
    pic_fraction = -1000000
    pic_data={}
    row,col= len(chair_),len(chair_[0])

    near,set_ = read_file(row,col)

    while(times):
        now_data = sort_once(name_, chair_)
        now_fraction = calc_fraction(now_data,row,col,near,set_)
        if now_fraction > pic_fraction:
            pic_fraction = now_fraction
            pic_data = now_data
        #print(times,':',now_fraction)
        times -= 1
    print(pic_fraction)
    return pic_data

#排序完成
def end_sort():
    end_choice = ag.msgbox(msg='完成任务啦，看看结果吧！', title = Title, ok_button='返回主界面', image=None, root=None)
    if end_choice == '返回主界面':
        main_interface()

#命令行主程序
def cmd_():
    input_cmd = ag.enterbox("请输入需要的命令",title= Title)
    if init_['Administration'] == 0:
        choice_ = ag.msgbox(msg='您没有相关权限', title= Title, ok_button='返回主界面', image=None, root=None)
        if choice_ == '返回主界面':
            main_interface()
        return
    
def read_init():
    init_['activation'] = 0
    
    if not os.path.isfile('.idea\initialization.xml'):
        return
    
    f = open('.idea\initialization.xml','r',encoding='utf-8')
    line = f.readline()
    while line:
        init_[line[0:line.find(' ')]]=line[line.find(' ')+1:]
        if init_[line[0:line.find(' ')]][-1] == '\n':
            init_[line[0:line.find(' ')]] = init_[line[0:line.find(' ')]][:-1:]
        line = f.readline()
    f.close()
    
    print(init_)
    
#关于程序主程序
def about_program():
    show_ = '程序名称：排座位辅助器\n' + '版本号： v2.0.0\n' + '项目简介：需要帮助班级同学们公平的抽到位置，也减小班干部的工作量，和一些同学的特殊需求，特意开发了此项目\n'
    show_ += '版权: @ 衢州二中 Martian148\n' + '说在后面的话：如有什么问题或特殊需求请私找我，本人QQ:1485868106，由于本人的水平有限，使用了简单的esaygui图形化框架，也没用什么算法，也希望各位大佬给我提一些改进的建议\n'
    show_ += '更详细的介绍：https://www.cnblogs.com/Martian148'
    choice_ = ag.msgbox(msg=show_, title=' ', ok_button='返回主界面', image=None, root=None)

    if choice_ == '返回主界面':
        main_interface()

#主程序

if __name__ == '__main__':
    read_init()
    main_interface()
