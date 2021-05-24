import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time


def drawAnimation(xData, yData, header):
    params = {'figure.figsize': '6.8, 4.8'}
    plt.rcParams.update(params)
    plt.ion()
    plt.figure(1)
    t_list = []
    result_list = []
    plt.ticklabel_format(style='plain', useOffset=False)
    for i in range(len(yData)):
        t_list.append(xData[i])
        result_list.append(yData[i])
        if i > 5:
            del t_list[0]
            del result_list[0]
        plt.plot(t_list, result_list, c='r', ls='-', marker='o', mec='b', mfc='w')
        plt.title(header)
        plt.ylabel('确诊人数')
        plt.xlabel('时间')
        plt.pause(0.5)


def showAlltimeWorld(countryName):
    # 获取数据
    fileName = "data/alltime_world" + '_' + time.strftime('%Y_%m%d', time.localtime(time.time())) + '.csv'
    worldAlltimeData = pd.read_csv(fileName)
    historyData = worldAlltimeData.loc[worldAlltimeData['name'] == countryName]  # 得到指定国家历史数据
    confirmData = historyData['total_confirm'].values.tolist()
    dateData = historyData['date'].values.tolist()
    drawAnimation(dateData, confirmData, countryName + '历史数据')


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
    provinceName = todayChinaData['name'].values.tolist()
    totalConfirm = todayChinaData['total_confirm'].values.tolist()
    totalDeath = todayChinaData['total_dead'].values.tolist()
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
    countryName = todayWorldDataSorted['name'].values.tolist()
    totalConfirm = todayWorldDataSorted['total_confirm'].values.tolist()
    totalDeath = todayWorldDataSorted['total_dead'].values.tolist()
    # 画图
    drawTable(countryName, totalConfirm, totalDeath, '世界累计确诊前30国家情况\n', '国家')
