import requests
import json
import os
from bs4 import BeautifulSoup

def get_city_data():
    url = "https://www.meituan.com/changecity/"
    html = requests.get(url).text
    if len(html) == 0:
        return 0
    print("数据获取成功")
    city_list = BeautifulSoup(html, "html.parser").find_all('a', attrs={'class': 'city'})
    city_obj = {}
    for key, v in enumerate(city_list):
        city_href = 'https:' + v['href'] + '/meishi/'
        city_name = v.string
        if city_obj.__contains__(city_name) == False:
            city_obj[city_name] = city_href
            print('[' + str(key) + ']' + city_name + ':' + city_href)
    return city_obj

if __name__ == '__main__':
    res = get_city_data()
    if res == 0:
        print('请求失败')
    else:
        print('请求成功')
        file = open('city.json', 'w')
        file.write(json.dumps(res))
        file.close()
