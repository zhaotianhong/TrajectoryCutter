# encoding: utf-8
# file: write_to_shp.py
# author: zhaotianhong
# time: 2018/5/17 9:33

import os
from osgeo import gdal
from osgeo import ogr



def read_data(path=r'../DATA/result/trip_stop.txt'):
    '''
    去读停留点文件
    :param path: 
    :return: 
    '''
    data = []
    with open(path,'r') as f:
        for line in f:
            line_arr = line[:-1].split('\t')
            plyline = line_arr[-1]
            data.append([int(line_arr[0]),line_arr[1],int(line_arr[2]),int(line_arr[3]),line_arr[4],line_arr[5],int(line_arr[10]),int(line_arr[11]),plyline])
    return data

# 创建shap文件
def createShap_line():
    data = read_data()
    path_out = r'../DATA/result/SHP'

    #为了支持中文路径，请添加下面这句代码
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","NO")
    #为了使属性表字段支持中文，请添加下面这句
    gdal.SetConfigOption("SHAPE_ENCODING","")
    #注册所有的驱动
    ogr.RegisterAll()
    #数据格式的驱动
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds=driver.CreateDataSource(path_out)
    shapLayer=ds.CreateLayer("trip_stay_line",geom_type=ogr.wkbLineString25D)
    #添加字段
    # 先创建一个叫FieldID的整型属性
    oFieldID = ogr.FieldDefn("car_ID", ogr.OFTInteger)
    shapLayer.CreateField(oFieldID, 1)

    oFieldtype = ogr.FieldDefn("type", ogr.OFTString)
    shapLayer.CreateField(oFieldtype, 1)

    oFieldstart = ogr.FieldDefn("start", ogr.OFTString)
    shapLayer.CreateField(oFieldstart, 1)

    oFieldend = ogr.FieldDefn("end", ogr.OFTString)
    shapLayer.CreateField(oFieldend, 1)

    oFieldend = ogr.FieldDefn("start_str", ogr.OFTString)
    shapLayer.CreateField(oFieldend, 1)

    oFieldend = ogr.FieldDefn("end_str", ogr.OFTString)
    shapLayer.CreateField(oFieldend, 1)

    oFielddis = ogr.FieldDefn("distance", ogr.OFTInteger)
    shapLayer.CreateField(oFielddis, 1)

    oFieldtime = ogr.FieldDefn("duration", ogr.OFTInteger)
    shapLayer.CreateField(oFieldtime, 1)

    oDefn = shapLayer.GetLayerDefn()
    feature = ogr.Feature(oDefn)
    for line in data:
        feature.SetField(0,line[0])
        feature.SetField(1, line[1])
        feature.SetField(2, line[2])
        feature.SetField(3, line[3])
        feature.SetField(4, line[4])
        feature.SetField(5, line[5])
        feature.SetField(6, line[6])
        feature.SetField(7, line[7])

        line_f = ogr.Geometry(ogr.wkbLineString25D)
        features = line[-1].split(' ')
        for one in features:
            if len(one)>3:
                xyt = one.split(',')
                x = float(xyt[0])
                y = float(xyt[1])
                t = (int(xyt[2])-1448380800)/86400.0
                line_f.AddPoint(x,y,t)

        feature.SetGeometry(line_f)
        shapLayer.CreateFeature(feature)
    feature.Destroy()
    ds.Destroy()

def read_point(path = r'../DATA/result/original.txt'):
    '''
    读取点数据（原始数据）
    :param path: 
    :return: 
    '''
    data = []
    with open(path,'r') as f:
        for line in f:
            line_arr = line.split('\t')
            car_id = int(line_arr[0])
            xyt = line_arr[1][:-2].split(' ')
            for xyt_e in xyt:
                xyt_arr = xyt_e.split(',')
                data.append([car_id,float(xyt_arr[0]),float(xyt_arr[1]),float(xyt_arr[2]),xyt_arr[3]])
    return data


# 创建shap文件
def createShap_point():
    '''
    原始数据的可视化
    :return: 
    '''
    data = read_point()
    path_out = r'../DATA/result/SHP'
    # 为了支持中文路径，请添加下面这句代码
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    # 为了使属性表字段支持中文，请添加下面这句
    gdal.SetConfigOption("SHAPE_ENCODING", "")
    # 注册所有的驱动
    ogr.RegisterAll()
    # 数据格式的驱动
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.CreateDataSource(path_out)
    shapLayer = ds.CreateLayer("didi_point", geom_type=ogr.wkbPoint25D)
    # 添加字段
    # 先创建一个叫FieldID的整型属性
    oFieldID = ogr.FieldDefn("car_ID", ogr.OFTInteger)
    shapLayer.CreateField(oFieldID, 1)

    oFieldtype = ogr.FieldDefn("x", ogr.OFTString)
    shapLayer.CreateField(oFieldtype, 1)

    oFieldstart = ogr.FieldDefn("y", ogr.OFTString)
    shapLayer.CreateField(oFieldstart, 1)

    oFieldend = ogr.FieldDefn("t", ogr.OFTInteger)
    shapLayer.CreateField(oFieldend, 1)

    oFieldend = ogr.FieldDefn("type", ogr.OFTString)
    shapLayer.CreateField(oFieldend, 1)


    oDefn = shapLayer.GetLayerDefn()
    feature = ogr.Feature(oDefn)
    for line in data:
        feature.SetField(0, line[0])
        feature.SetField(1, line[1])
        feature.SetField(2, line[2])
        feature.SetField(3, int(line[3]))
        feature.SetField(4, line[4])


        line_f = ogr.Geometry(ogr.wkbPoint25D)

        x = float(line[1])
        y = float(line[2])
        t = (int(line[3]) - 1448380800) / 86400.0
        line_f.AddPoint(x, y, t)

        feature.SetGeometry(line_f)
        shapLayer.CreateFeature(feature)
    feature.Destroy()
    ds.Destroy()


if __name__ == '__main__':
    # path = r'J:\trip_stop.txt'
    # # path =r'E:\python\beijingdidi_show\test.txt'
    # data = read_data(path)
    # createShap(data)
    # createShap_point()
    createShap()