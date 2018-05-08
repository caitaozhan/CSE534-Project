import sys
import webbrowser
import time
from selenium import webdriver
import numpy as np


option = webdriver.ChromeOptions()
option.add_extension('Proxy-SwitchyOmega_v2.5.9.crx')
browser = webdriver.Chrome(chrome_options=option)
browser.get('chrome://extensions/')

time.sleep(20)  # set up switchyomega

url_list = ['http://sharpdaily.tw', 'http://www.ulop.net/', 'http://switch1.jp/', 
            'http://dongtaiwang.com/', 'https://zh.wikipedia.org/zh/%E5%85%AD%E5%9B%9B%E4%BA%8B%E4%BB%B6',
            'https://www.rfa.org/mandarin/yataibaodao/64-06032009120239.html']

size = len(url_list)

while 1:
    time.sleep(5)
    browser.get(url_list[np.random.randint(size)])