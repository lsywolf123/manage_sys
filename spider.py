# -*- coding: utf-8 -*-
import requests
from lxml import etree
from xlwt import *


def area_list_get():
    area_list = []
    pic_url = 'http://yyk.99.com.cn/hunan'
    html = requests.get(pic_url).text
    selector = etree.HTML(html)
    area_content = selector.xpath('//div[@class="fontlist"]/ul/li/a[@target="_self"]/@href')
    # print html
    for area_url in area_content:
        area_list.append(area_url)
    return area_list


def hospital_list_get():
    hospital_list = []
    for area in area_list_get():
        html = requests.get(area).text
        selector = etree.HTML(html)
        hospital_content = selector.xpath('//div[@class="tablist"]/ul/li/a[@target="_blank"]/@href')
        for hospital in hospital_content:
            hospital_list.append(hospital)
    return hospital_list


def hospital_spider():
    hospital_list = hospital_list_get()
    count = 1
    data_dict = {}
    for hospital_url in hospital_list:
        html = requests.get(hospital_url+'jianjie.html').text
        selector = etree.HTML(html)
        region_content = selector.xpath('//div[@class="w960"]/div/p/a[@target="_self"]')
        province = region_content[1].text
        city = region_content[2].text
        area = region_content[3].text
        name = region_content[3].tail.split('>')[1]
        print count, name
        base_info_content = selector.xpath('//div[@class="hpi_content clearbox"]/ul/li')
        extra_name = base_info_content[0].xpath('string(.)').split()[0].split(u'：')[1]
        property = base_info_content[1].xpath('string(.)').split()[0].split(u'：')[1]
        rank = base_info_content[2].xpath('string(.)').split()[0].split(u'：')[1]
        phone = base_info_content[3].xpath('string(.)').split()[0].split(u'：')[1]
        address = base_info_content[4].xpath('string(.)').split()[0].split(u'：')[1]
        extra_info_content = selector.xpath('//td[@class="tdr"]')
        department_num = extra_info_content[6].xpath('string(.)').strip()
        staff_num = extra_info_content[7].xpath('string(.)').strip()
        extra_info_content = selector.xpath('//td[@class="tdr lasttd"]')
        bed_num = extra_info_content[0].xpath('string(.)').strip()
        out_num = extra_info_content[1].xpath('string(.)').strip()
        if_hos_secure = extra_info_content[2].xpath('string(.)').strip()
        hostpital_info_list = [province, city, area, name, extra_name, rank, property, address, phone, department_num, staff_num, bed_num, out_num, if_hos_secure]
        data_dict[count] = hostpital_info_list
        count += 1
    return data_dict


def add_to_excel():
    file = Workbook(encoding='utf-8')
    table = file.add_sheet('医院信息.xls')
    data = hospital_spider()
    ldata = []
    num = [a for a in data]
    num.sort()
    for x in num:
        t = [int(x)]
        for a in data[x]:
            t.append(a)
        ldata.append(t)
    for i,p in enumerate(ldata):
        for j,q in enumerate(p):
            table.write(i,j,q)
    file.save('医院信息.xls')


def test():
    pic_url = 'http://www.51eliao.com/invbidtype-0.html'
    html = requests.get(pic_url).text
    print '*************************************************************************************************************************'
    print html
    for i in range(2):
        pic_url = 'http://www.51eliao.com/InvBidType.aspx?typeid=0'
        html = requests.post(pic_url).text
        print '*************************************************************************************************************************'
        print html


if __name__ == "__main__":
    test()