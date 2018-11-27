# encoding: utf-8

'''
用高德导航轨迹补充缺失的轨迹
'''

import requests
import random
import _tools

KEYS = ['946a317c917d70ca56a48cb1a4787163',
        'f7ce9c42c10ff75e38f3b8ccd6ab1f9d',
        'f2d13bf197cce2f48b2616a41a34faf8',
        'ad51ff9223a78e1c5ba930e94341ad03',
        'dfb29682d166b9f1cc96eac05d39b53b']


def get_navigation(p1, p2, t1, t2):
    '''用高德车辆导航接口获得导航数据坐标系：火星'''
    plot, repair_data = '', []
    key = KEYS[random.randint(0, 4)]
    dive = r'http://restapi.amap.com/v3/direction/driving?key=' + key + '&origin=' + p1 + '&destination=' + p2
    try:
        content = requests.get(dive).json()
    except:
        return None
    for step in content['route']['paths'][0]['steps']:
        line = step['polyline']
        plot += line + ';'
    lines = plot[:-1].split(';')
    for line in lines:
        xy = line.split(',')
        repair_data.append([float(xy[0]), float(xy[1])])

    each_up = int(abs(t2 - t1) / len(repair_data))
    for line in repair_data:
        t1 += each_up
        line.append(t1)
        line.append(1)

    return repair_data


def repair(result):
    '''
    两个点之间距离相隔1000米以上，用导航gps轨迹修复
    :param result: 
    :return: 
    '''
    for k, v in result.items():
        add_point = []
        add_point.extend(v[-1])
        if len(v[-1]) > 2:
            for i in range(len(v[-1])-1):
                first = v[-1][i]
                second = v[-1][i + 1]
                dis = _tools.haversine(first[0], first[1], second[0], second[1])
                # 两点相隔1km
                if dis > 1000:
                    p1 = str(first[0]) + ',' + str(first[1])
                    t1 = first[2]
                    p2 = str(second[0]) + ',' + str(second[1])
                    t2 = second[2]
                    repair_data = get_navigation(p1, p2, t1, t2)
                    if not repair_data:
                        return None
                    add_point.extend(repair_data)
        add_point = sorted(add_point,key=lambda x:x[2])
        v[-1] = add_point
    return result


    


if __name__ == '__main__':
    p1 = '116.54832,39.88112'
    p2 = '116.48725,39.98947'
    # get_navigation(p1, p2)
