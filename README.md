# Beijing_DIDI
## 描述
对某一天滴滴gps轨迹识别其`停留点`与`运动轨迹`,统计其停留点的个数，停留长，运动轨迹长度，运动时间。
## 文件
* `main.py`：入口
* `_get_trip_stop`：对整条轨迹识别出停留点与运动轨迹
* `_write_to_shp`：将轨迹输出为shape文件
## 依赖
`OGR`,`matplotlib`<br>
<br>
[OGR安装](https://blog.csdn.net/savannahmyself/article/details/77185238)
[  下载地址](http://www.gisinternals.com/query.html?content=filelist&file=release-1911-x64-gdal-2-3-0-mapserver-7-0-7.zip)
## 流程
1. 间断点识别<br>
2. 停留点聚类<br>
3. 识别与融合停留点<br>
4. 轨迹识别<br>

![](https://github.com/zhaotianhong/Beijing_DIDI/blob/master/Figure_1.png)
