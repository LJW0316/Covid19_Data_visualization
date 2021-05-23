import requests
import pandas as pd
import json
import time


def getOriginalData():
    """
    爬取数据
    :return: 爬取的疫情数据
    """
    # 模拟浏览器的请求头
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/90.0.4430.212 Safari/537.36 '
    }
    url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=324213531709'  # 数据源
    r = requests.get(url, headers=headers)  # 爬取数据
    data_json = json.loads(r.text)  # 将数据处理成json
    data = data_json['data']  # 得到有用信息
    return data


def saveData(data, name):
    """
    保存数据
    :param data:数据源
    :param name:文件名
    :return:None
    """
    file_name = name + '_' + time.strftime('%Y_%m%d', time.localtime(time.time())) + '.csv'  # 保存文件位置文件名
    data.to_csv('data/' + file_name, index=None, encoding='utf_8_sig')  # 以utf8编码保存
    print(file_name + ' 保存成功 ')


def getData(data, info_list):
    """
    处理原始数据
    :param data:所需的原始数据指定部分
    :param info_list:数据
    :return:处理过后的数据
    """
    info = pd.DataFrame(data)[info_list]  # 主要信息
    today_data = pd.DataFrame([i['today'] for i in data])  # 生成today的数据
    today_data.columns = ['today_' + i for i in today_data.columns]  # 修改列名
    total_data = pd.DataFrame([i['total'] for i in data])  # 生成total的数据
    total_data.columns = ['total_' + i for i in total_data.columns]  # 修改列名
    return pd.concat([info, total_data, today_data], axis=1)  # info、today和total横向合并最终得到汇总的数据


def getChineseCurrentData(data):
    """
    获取中国各省最新数据
    :param data:爬取的总信息
    :return:中国各省的最新疫情数据
    """
    data_province = data['areaTree'][2]['children']  # 找到中国各省的当日数据
    today_province = getData(data_province, ['id', 'lastUpdateTime', 'name'])  # 获得处理后数据
    return today_province


def getWorldCurrentData(data):
    """
    获得全球最新疫情信息
    :param data:爬取的总信息
    :return:全球各国最新的疫情数据
    """
    areaTree = data['areaTree']  # 获取全球各国信息
    today_world = getData(areaTree, ['id', 'lastUpdateTime', 'name'])  # 获取处理后数据
    return today_world


def worldAlltimeData(today_world):
    """
    获得全球历史疫情数据
    :param today_world:世界最新数据，用于使用id得到国家名
    :return:全球历史疫情数据
    """
    country_dict = {key: value for key, value in zip(today_world['id'], today_world['name'])}  # 获得
    start = time.time()
    for country_id in country_dict:  # 遍历每个国家的编号
        try:
            # 按照编号访问每个国家的数据地址，并获取json数据
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/90.0.4430.212 Safari/537.36 '
            }
            url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode=' + country_id
            r = requests.get(url, headers=headers)
            json_data = json.loads(r.text)

            # 生成每个国家的数据
            country_data = getData(json_data['data']['list'], ['date'])
            country_data['name'] = country_dict[country_id]

            # 数据叠加
            if country_id == '9577772':
                alltime_world = country_data
            else:
                alltime_world = pd.concat([alltime_world, country_data])

            print('-' * 20, country_dict[country_id], '成功', country_data.shape, alltime_world.shape,
                  ',累计耗时:', round(time.time() - start), '-' * 20)

        except requests.exceptions.RequestException:  # 获取失败
            print('-' * 20, country_dict[country_id], 'wrong', '-' * 20)

    return alltime_world


def get():  # 开始爬取数据
    data = getOriginalData()  # 获得原始数据
    today_province = getChineseCurrentData(data)  # 中国各省最新数据
    today_world = getWorldCurrentData(data)  # 全球各国最新数据
    alltime_world = worldAlltimeData(today_world)  # 全球历史疫情数据

    # 保存数据
    saveData(today_province, 'todayChina')
    saveData(today_world, 'todayWorld')
    saveData(alltime_world, 'alltime_world')
