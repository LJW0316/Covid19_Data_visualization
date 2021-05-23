import getData
import analyse


def main():
    print('正在获取数据...')
    getData.get()
    while True:
        print('1.显示全国各省市累计数据')
        print('2.显示世界各国累计数据')
        print('3.显示国家历史数据')
        print('0.退出')
        c = input('请选择功能：')
        if c == '0':
            break
        elif c == '1':
            analyse.showTodayChina()
        elif c == '2':
            analyse.showTodayWorld()
        elif c == '3':
            name = input('请输入国家名：')
            analyse.showAlltimeWorld(name)


if __name__ == '__main__':
    main()
