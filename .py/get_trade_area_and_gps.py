import requests
import json
from bs4 import BeautifulSoup
import os
import codecs
from openpyxl import Workbook

# 从美团API中获取城市url
def get_url_from_api(city_name):
    url = "https://apimobile.meituan.com/group/v1/area/search/"
    res = requests.get(url + city_name).text
    res = json.loads(res)
    if len(res['data']) == 0:
        return 0
    else:
        acronym = res['data'][0]['cityAcronym']
        if len(acronym) == 0:
            return 0
        else:
           return [('https://' + acronym + '.meituan.com/meishi/'), city_name]

# 从本地json文件从获取城市url
def get_url_from_json(city_name):
    if os.path.exists('city.json') == True:
        file = open('city.json', 'r').read()
        city_json = json.loads(file)
        if city_json.__contains__(city_name):
            return [city_json[city_name], city_name]
        else:
            return 0
    else:
        return 0

# 获取商圈数据
def get_area_data(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    html = requests.get(url[0], headers=headers).text
    if len(html) == 0:
        print('未找到该城市的商圈信息')
        return 0
    else:
        html = BeautifulSoup(html, "html.parser").find_all('script')
        city_json = ''    # 存放包含商圈信息的json字符串
        for i in html:
            i = str(i.string)
            if i.find('window._appState') != -1:
                city_json = i
                break
        city_json = city_json[19:-1]    # 去除首位不需要的字符,仅保留json数据
        city_json = json.loads(city_json)
        city_json = city_json['filters']['areas']
        return [city_json, url[1]]

# 处理数据 json=>txt
def process_data(data):
    res = ""
    for key, i in enumerate(data[0]):
        res += i['name'] + "\n"
        for j in data[0][key]['subAreas']:
            if j['name'] != '全部':
                res += data[1] + j['name'] + "\n"
    return res


def init():
    city = codecs.open('city_area.txt', 'r', 'UTF-8')
    while True:
        city_name = city.readline().strip()
        if not city_name:
            city.close()
            break
        # city_name = city_line
        url = get_url_from_json(city_name)
        if url == 0:
            url = get_url_from_api(city_name)
            if url == 0:
                print("输入的城市名有误,请重新输入")
                init()
        data = get_area_data(url)
        if data != 0:
            data = process_data(data)
            print(data)
            file = open('city_area_' + city_name + '.txt', 'w', encoding='UTF-8')
            file.write(data)
            file.close()
        f = codecs.open('city_area_' + city_name + '.txt', 'r', 'UTF-8')
        i = 0

        wb = Workbook()
        sheet = wb.active
        sheet.title = "qiang"

        def get_location(address, i):
            print(i)
            url = "http://restapi.amap.com/v3/geocode/geo"
            data = {
                'key': 'xxxx',  # 在高德地图开发者平台申请的key，需要替换为自己的key
                'address': address
            }
            r = requests.post(url, data=data).json()
            sheet["A{0}".format(i)].value = address.strip('\n')
            print(r)
            if r['status'] == '1':
                if len(r['geocodes']) > 0:
                    GPS = r['geocodes'][0]['location']
                    sheet["B{0}".format(i)].value = '[' + GPS + ']'
                else:
                    sheet["B{0}".format(i)].value = '[]'
            else:
                sheet["B{0}".format(i)].value = '未找到'
            # 将地址信息替换为自己的文件，一行代表一个地址，根据需要也可以自定义分隔符

        while True:
            line = f.readline()
            i = i + 1
            if not line:
                f.close()
                wb.save('city_area_gps_' + city_name + '.xlsx')
                break
            get_location(line, i)

if __name__ == '__main__':
    init()
