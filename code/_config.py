# encoding: utf-8
# author: zhaotianhong

CONFIG = {
    'path_in':'../DATA/original',
    'path_out':'../DATA/result/trip_stop.txt',
    'path_original':r'../DATA/result/original.txt',
    'date':{'24':[1448294400,1448380800],
            '25':[1448380800,1448467200],
            '26':[1448467200,1448553600],
            '27':[1448553600,1448640000],
            '28':[1448640000,1448726400]},

    # 间断点切分
    'break_value':1200,
    # 120s内且在500米以内的停留视为一个停留集合
    'stop_cluster':[120,500]
}