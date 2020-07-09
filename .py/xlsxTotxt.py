import xlrd
import codecs

def init():
    city = codecs.open('city_area.txt', 'r', 'UTF-8')
    while True:
        city_name = city.readline().strip()
        if not city_name:
            city.close()
            break
        fileName = 'city_area_gps_' + city_name + '.xlsx'
        fileHandler = xlrd.open_workbook(fileName)
        sheet_name1 = u'trade_area'
        page = fileHandler.sheet_by_name(sheet_name1)
        col1 = page.col_values(0)  # 商圈
        col2 = page.col_values(1)  # GPS

        f2 = open('city_area_gps_' + city_name + '.txt', "w", encoding='UTF-8')
        for i in range(len(col1)):
            text = col1[i].strip(city_name).strip('\n')
            label = str(col2[i]).strip('\n')
            data = city_name + '\t' + text + '\t' + label + '\n'
            f2.write(data)

if __name__ == '__main__':
    init()








