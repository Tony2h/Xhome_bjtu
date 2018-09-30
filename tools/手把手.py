
from selenium import webdriver
import csv

url = 'https://music.163.com/#/discover/playlist/?cat=%E6%B5%81%E8%A1%8C&limit=35&offset=0'   #&limit=35&offset=0

driver = webdriver.Chrome()
_driver = webdriver.Chrome()
csv_file = open("playlist_style1.csv","a",newline='')
writer = csv.writer(csv_file)
#writer.writerow(['name','singer','style'])

writer.writerow([])
while url != 'javascript:void(0)':
    driver.get(url)
    driver.switch_to.frame('contentFrame')
    data = driver.find_element_by_id('m-pl-container').find_elements_by_tag_name('li')
    for i in range(len(data)):
        nb = data[i].find_element_by_class_name('nb').text
        if '万' in nb and int(nb.split('万')[0])>1700:
            #读取列表内歌曲信息
            _url = data[i].find_element_by_tag_name('a').get_attribute('href')
            _driver.get(_url)
            _driver.switch_to.frame('contentFrame')
            _song = _driver.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
            song = []
            for i in range(len(_song)):
                singer = _song[i].find_element_by_css_selector('div.text').get_attribute('title')
                name = _song[i].find_element_by_tag_name('b').get_attribute('title')
                style = '流行'
                print(singer,name,style)
                writer.writerow([name, singer,style])

    url = driver.find_element_by_css_selector('a.zbtn.znxt').get_attribute('href')

csv_file.close()
