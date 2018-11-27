# encoding: utf-8
# file: static.py
# author: zhaotianhong
# time: 2018/4/14 14:48


CONFIG = {
    # 调整统计参数：range：统计范围，超出范围用MORE表示；unit：每个统计单元的大小
    # car_trip_dis_s一辆车总行驶距离；
    # car_trip_time_s总行驶时间；
    # car_stop_time_s总停留时间；
    # trip_dis_s每段行驶的距离；
    # trip_time_s每段行驶的时间；
    # stop_time_s每次停留的时间；
    # 单位：s,m
    'car_trip_dis_s': {'range': 500000, 'unit': 3000},
    'car_trip_time_s': {'range': 36000, 'unit': 180},
    'car_stop_time_s': {'range': 86400, 'unit': 3600},
    'trip_dis_s': {'range': 100000, 'unit': 3000},
    'trip_time_s': {'range': 36000, 'unit': 1800},
    'stop_time_s': {'range': 36000, 'unit': 180},
    # 文件保存路径
    'out_put_dir':r'../DATA/result'
}

def stas_(path):
    '''
    读取文件和初步统计：初步统计每辆车的累积时间和距离
    :param path: 原始文件路径
    :return: 
    '''
    all_data = {}
    all_stop_time, trip_time, trip_dis = [], [], []
    with open(path, 'r') as f:
        for line in f:
            line_arr = line[:-1].split('\t')
            car_id = line_arr[0]
            if car_id not in all_data.keys():
                if int(line_arr[-1]) == 0:
                    time_stop = int(line_arr[-2])
                    all_stop_time.append(time_stop)
                    all_data[car_id] = {'stop_time': time_stop, 'trip_time': 0, 'trip_dis': 0}

                if int(line_arr[-1]) != 0:
                    dis_trip = int(line_arr[-1])
                    time_trip = int(line_arr[-2])
                    trip_dis.append(dis_trip)
                    trip_time.append(time_trip)
                    all_data[car_id] = {'stop_time': 0, 'trip_time': time_trip, 'trip_dis': dis_trip}

            else:
                if int(line_arr[-1]) == 0:
                    time_stop = int(line_arr[-2])
                    all_stop_time.append(time_stop)
                    all_data[car_id]['stop_time'] += time_stop
                if int(line_arr[-1]) != 0:
                    dis_trip = int(line_arr[-1])
                    time_trip = int(line_arr[-2])
                    trip_dis.append(dis_trip)
                    trip_time.append(time_trip)
                    all_data[car_id]['trip_time'] += time_trip
                    all_data[car_id]['trip_dis'] += dis_trip
    return all_data, all_stop_time, trip_time, trip_dis


def init_dict(_range,_unit):
    '''初始化统计字典'''
    r_dict, data_dict, x_ticks, trun = {}, {}, {}, 0
    _num = int(_range / _unit)
    for i in range(_num):
        data_dict[i] = 0
    data_dict['MORE'] = 0
    return data_dict

def update_dict(data_dict,unit):
    '''
    更新统计表字典：为了让人辨识度高一点
    :param data_dict: 原始字典
    :param unit: 每个区间的大小
    :return: 
    '''
    new_dict = {}
    for k in data_dict.keys():
        if type(k) == int:
            new_dict[(1+k)*unit] = data_dict[k]
        else:
            # more字段
            new_dict[k] = data_dict[k]
    return new_dict

def statistics_each(name,data):
    '''
    统计类型
    :param name: 统计类型名字
    :param data: 改类型的原始数据
    :return: 
    '''
    statistics_dict = init_dict(CONFIG[name]['range'], CONFIG[name]['unit'])
    for d in data:
        # 属于哪一区间
        index = int(d / CONFIG[name]['unit'])
        if index in statistics_dict:
            statistics_dict[index] += 1
        else:
            # 不在区间内为‘MORE
            statistics_dict['MORE'] += 1
    return update_dict(statistics_dict, CONFIG[name]['unit'])

def cut_data(all_data, stop_time, trip_time, trip_dis):
    '''
    统计各个类型的统计量
    :param all_data: 统计了车辆一天累积行驶时间与距离，累积停留时间
    :param stop_time: 每一个停留点的时间
    :param trip_time: 每一次行驶的时间
    :param trip_dis: 每一次行驶的距离
    :return: 
    '''
    car_trip_dis, car_trip_time, car_stop_time = [], [], []
    for k, v in all_data.items():
        car_trip_dis.append(v['trip_dis'])
        car_trip_time.append(v['trip_time'])
        car_stop_time.append(v['stop_time'])

    # 车辆一天行驶距离
    car_trip_dis_s = statistics_each('car_trip_dis_s',car_trip_dis)

    # 车辆一天行驶时间
    car_trip_time_s = statistics_each('car_trip_time_s', car_trip_time)

    # 车辆一天的停留时间
    car_stop_time_s = statistics_each('car_stop_time_s', car_stop_time)

    # 每次trip的距离
    trip_dis_s = statistics_each('trip_dis_s', trip_dis)

    # 每次trip的时间
    trip_time_s = statistics_each('trip_time_s', trip_time)

    # 每次停留的时间
    stop_time_s = statistics_each('stop_time_s', stop_time)

    return car_trip_dis_s, car_trip_time_s, car_stop_time_s, trip_dis_s, trip_time_s, stop_time_s


def out_put_file(file_name,data):
    '''
    输出文件；有一个MORE：表示超出这个范围的统计量。
    :param file_name: 输出文件名
    :param data: 统计数据
    :return: 
    '''
    path = CONFIG['out_put_dir']+"\\"+file_name+".csv"
    more = data.pop('MORE')
    # 先排序，按照key
    data = sorted(data.items(),key=lambda x:x[0])
    with open(path,'w') as fw:
        fw.write('WITHIN'+','+'NUM'+'\n')
        for v in data:
            fw.write(str(v[0])+','+str(v[1])+'\n')
        fw.write(str('MORE') + ',' + str(more) + '\n')



if __name__ == '__main__':
    path = r'../DATA/result/trip_stop.txt'
    # cacu_data车辆累积的行驶与停留时间与距离；
    # stop_time每次停留的时间；
    # trip_time每次行驶时间；
    # trip_dis每次行驶距离。
    cacu_data, stop_time, trip_time, trip_dis = stas_(path)

    # 变量：一辆车总行驶距离，总行驶时间，总停留时间；每一段行驶的距离，每一段行驶的时间，每一次停留的时间
    car_trip_dis_s, car_trip_time_s, car_stop_time_s, trip_dis_s, trip_time_s, stop_time_s = cut_data(cacu_data,
                                                                                                      stop_time,
                                                                                                      trip_time,
                                                                                                      trip_dis)

    # 文件名以统计变量名表示
    out_put_file('car_trip_dis_s',car_trip_dis_s)
    out_put_file('car_trip_time_s', car_trip_time_s)
    out_put_file('car_stop_time_s', car_stop_time_s)
    out_put_file('trip_dis_s', trip_dis_s)
    out_put_file('trip_time_s', trip_time_s)
    out_put_file('stop_time_s', stop_time_s)

