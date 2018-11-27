# encoding: utf-8
# author: zhaotianhong
import shutil
import time
from math import radians, cos, sin, asin, sqrt
import os
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    '''用经纬度计算距离，单位米'''
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r * 1000


def timestamp_to_time(timestamp):
    '''时间戳转时间'''
    time_local = time.localtime(int(timestamp))
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt


def time_to_timestamp(dt):
    '''时间转时间戳'''
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = time.mktime(timeArray)
    return int(timestamp)


def get_all_csv(f_dir):
    '''获取所有的文件'''
    print('file location:', f_dir)
    L = []
    for root, dirs, files in os.walk(f_dir):
        for file in files:
            L.append(os.path.join(root, file))
    print('file number:', len(L))
    return L


def read_data(path, START_TIME, END_TIME):
    '''
    读取数据：1.筛选时间段；2.筛选记录低于500条的文件；3.根据经纬度重新计算速度并标记（0：静止，1：运动）
    :param path: 文件路径
    :return: 
    '''
    # time_list用于去时间记录为重复的
    data_list, time_list, total_dis = [], [], 0
    with open(path, 'r') as f:
        for line in f:
            if len(line) > 10:
                line_arr = line[:-1].split(',')
                time_stamp = int(line_arr[2])
                if time_stamp not in time_list and time_stamp > START_TIME and time_stamp < END_TIME:
                    data_list.append([float(line_arr[0]), float(line_arr[1]), time_stamp, float(line_arr[3]),
                                      timestamp_to_time(time_stamp)])
                    time_list.append(time_stamp)
    # 文件无数据
    if len(data_list) == 0:
        return None
    # 排序，按时间戳排序
    data_list = sorted(data_list, key=lambda x: x[2])
    # 计算运动或者静止
    temp_data = [data_list[0]]
    temp_data[0][3] = 0
    for i in range(1, len(data_list)):
        dis = haversine(temp_data[-1][0], temp_data[-1][1], data_list[i][0], data_list[i][1])
        total_dis += dis
        time_gap = abs(data_list[i][2] - temp_data[-1][2])
        v = dis / time_gap
        # 静止条件速度低于1m/s
        if v == 0:
            data_list[i][3] = 0
            temp_data.append(data_list[i])
        else:
            data_list[i][3] = 1
            temp_data.append(data_list[i])

    # 记录小于500且总距离小于500，返回空
    if len(data_list) <= 500 and total_dis < 500:
        return None
    return data_list


def show_map(merge_list, data):
    '''3D显示用于分析'''

    fig = plt.figure()
    ax = Axes3D(fig)
    num = 0

    move = []
    for k, v in merge_list.items():
        if len(v[-1]) > 2:
            move.extend(v[-1])

    for k, v in merge_list.items():
        num += 1
        x, y, z = [], [], []
        for i in v[-1]:
            x.append(i[0])
            y.append(i[1])
            z.append(i[2])
        if len(v[-1]) == 2:
            ax.plot(x, y, z, 'b')
        else:
            ax.plot(x, y, z, 'r--')
    x_move, y_move, t_move = [], [], []
    x_stay, y_stay, t_stay = [], [], []

    for line in data:
        if [line[0], line[1], line[2], line[4]] in move:
            x_move.append(line[0])
            y_move.append(line[1])
            t_move.append(line[2])
        else:
            x_stay.append(line[0])
            y_stay.append(line[1])
            t_stay.append(line[2])
    ax.scatter(x_move, y_move, t_move)
    ax.scatter(x_stay, y_stay, t_stay)
    plt.show()


def write_to_files(data, car_id, xyt):
    '''
    写出文件
    :param data: 识别数据
    :param path: 输出路径
    :param xyt: 布尔型，是否要输出xyt用于画矢量图
    :return: 
    '''
    # 安装时间顺序写出
    path = r'../DATA/result/trip_stop.txt'

    keys = sorted(data.keys())
    with open(path, 'a+') as fw:
        for k in keys:
            v = data[k]
            type, xyt_str = 'TRIP', ''
            if len(v[-1]) == 2:
                type = 'STAY'
            time = str(v[4])
            dis = str(v[5])
            start_int = str(v[-1][0][2])
            start_str = str(v[-1][0][3])
            end_int = str(v[-1][-1][2])
            end_str = str(v[-1][-1][3])
            start_xy = (str(v[-1][0][0]), str(v[-1][0][1]))
            end_xy = (str(v[-1][-1][0]), str(v[-1][-1][1]))
            # 是否需要xyt
            if xyt:
                for line in v[-1]:
                    xyt_str += str(line[0]) + ',' + str(line[1]) + ',' + str(line[2]) + ' '
                fw.write(str(
                    car_id) + '\t' + type + '\t' + start_int + '\t' + end_int + '\t' + start_str + '\t' + end_str + '\t'
                         + start_xy[0]  + '\t' + start_xy[1] + '\t' + end_xy[0] + '\t' + end_xy[1] + '\t'
                         + time + '\t' + dis + '\t' + xyt_str + '\n')
            else:
                fw.write(str(
                    car_id) + '\t' + type + '\t' + start_int + '\t' + end_int + '\t' + start_str + '\t' + end_str +'\t' + start_xy[0]
                         + '\t' + start_xy[1] + '\t' + end_xy[0] + '\t' + end_xy[1] + '\t'  + time + '\t' + dis + '\n')


def reset_dir():
    '''
    重置文件
    :return: 
    '''
    filelist = os.listdir(r'../DATA/result')
    for f in filelist:
        filepath = os.path.join(r'../DATA/result', f)
        if os.path.isfile(filepath):
            os.remove(filepath)
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath, True)


def write_original_files(data, result, car_id):
    '''
    写出文件
    :param data: 识别数据
    :param path: 输出路径
    :return: 
    '''
    move = []
    for k, v in result.items():
        if len(v[-1]) > 2:
            move.extend(v[-1])
    # 安装时间顺序写出
    path = r'../DATA/result/original.txt'
    xyt_str = ''
    data = sorted(data, key=lambda x: x[2])
    with open(path, 'a+') as fw:
        for line in data:
            if [line[0], line[1], line[2], line[4]] in move:
                type = 'MOVE'
            else:
                type = 'STAY'
            xyt_str += str(line[0]) + ',' + str(line[1]) + ',' + str(line[2]) + ',' + type + ' '
        fw.write(str(car_id) + '\t' + xyt_str + '\n')
