import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML
import time


def pdFrameListToList(frame):
    """
    将pdFrame转换的嵌套列表展开
    :param frame:pdFrame转换的嵌套列表
    :return:展开后的列表
    """
    res = [x for k in frame for x in k]
    return res


def showAllTimeWorld():
    pass


def drawTable(Name, totalConfirm, totalDeath, header, xLabel):
    """
    画柱状统计图
    :param Name:x轴名称
    :param totalConfirm:累计确诊人数列表
    :param totalDeath:累计死亡人数列表
    :param header:统计表头
    :param xLabel:x轴单位
    :return:None
    """
    # 设置数据位置
    size = len(Name)
    index = np.arange(size)
    width = 0.5
    # 设置表格大小
    params = {'figure.figsize': '30, 15'}
    plt.rcParams.update(params)
    # 绘制表格主体
    rects = plt.bar(index, totalConfirm, width=width, label='累计确诊')
    plt.bar(index, totalDeath, width=width, label='累计死亡')
    # 设置x轴
    plt.xticks(index, Name)
    plt.xlabel(xLabel)
    # 设置y轴
    plt.ylabel('人数')
    # 纵轴显示数字
    for rect in rects:
        x = rect.get_x()
        height = rect.get_height()
        plt.text(x, 1.02 * height, str(height))
    # 设置标题
    plt.title(header + time.strftime('截至%Y年%m月%d日', time.localtime(time.time())))
    plt.legend()
    plt.show()


def showTodayChina():
    """
    画中国各省疫情图
    :return:None
    """
    # 获取数据
    fileName = "data/todayChina" + '_' + time.strftime('%Y_%m%d', time.localtime(time.time())) + '.csv'
    todayChinaData = pd.read_csv(fileName)
    provinceName = todayChinaData[['name']].values.tolist()
    provinceName = pdFrameListToList(provinceName)
    totalConfirm = todayChinaData[['total_confirm']].values.tolist()
    totalConfirm = pdFrameListToList(totalConfirm)
    totalDeath = todayChinaData[['total_dead']].values.tolist()
    totalDeath = pdFrameListToList(totalDeath)
    # 画图
    drawTable(provinceName, totalConfirm, totalDeath, '中国各省市累计确诊情况\n', '省份')


def showTodayWorld():
    """
    画世界各国疫情图
    :return:None
    """
    # 获取数据
    fileName = "data/todayWorld" + '_' + time.strftime('%Y_%m%d', time.localtime(time.time())) + '.csv'
    todayWorldData = pd.read_csv(fileName)
    todayWorldDataSorted = todayWorldData.sort_values(by='total_confirm', ascending=False).head(30)
    countryName = todayWorldDataSorted[['name']].values.tolist()
    countryName = pdFrameListToList(countryName)
    totalConfirm = todayWorldDataSorted[['total_confirm']].values.tolist()
    totalConfirm = pdFrameListToList(totalConfirm)
    totalDeath = todayWorldDataSorted[['total_dead']].values.tolist()
    totalDeath = pdFrameListToList(totalDeath)
    # 画图
    drawTable(countryName, totalConfirm, totalDeath, '世界累计确诊前30国家情况\n', '国家')


def main():
    showTodayChina()
    showTodayWorld()


if __name__ == '__main__':
    main()
