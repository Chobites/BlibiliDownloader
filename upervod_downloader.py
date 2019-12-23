# 1、This Script was debugged in Pycharm with Python37
# 2、you_get is not so stable when execute downloading in a long term
# 3、geckodriver.exe with installed FireFox needed
import sys
from selenium import webdriver
from you_get import common as you_get
import time
import os


# Get the number of video list pages and uper's name
def Get_VodPagesNum(uper_Uid_num):
    uper_Uid_str = str(uper_Uid_num)
    # uper's video list first page
    firstpage = 'https://space.bilibili.com/' + uper_Uid_str + '/video?tid=0&page=0'
    # Open Firefox
    browser = webdriver.Firefox()
    option = webdriver.FirefoxOptions()
    option.add_argument('-headless')
    # open uper's video list first page
    browser.get(firstpage)
    # Wait 2s
    time.sleep(2)
    # Get the number of video list pages on this first video list page
    pager_total_text = browser.find_element_by_class_name('be-pager-total').text
    # Get the name of Uper
    uper_name = browser.find_element_by_id('h-name').text
    print("Uper's name：", uper_name)
    print(pager_total_text)
    pager_total_str = ''
    # Transfer the page number from string to num
    for digit in pager_total_text:
        if digit.isdigit():
            pager_total_str = pager_total_str + digit
    if pager_total_str == '':
        pager_total_num = 0
    else:
        pager_total_num = int(pager_total_str)
    print('video list total number：', pager_total_num)
    browser.close()
    return [pager_total_num, uper_name]


# Define the download function
def downloadUperVod(uper_Uid_num, pager_total_num, directory):
    # transfer the uper's Uid into string
    uper_Uid_str = str(uper_Uid_num)
    # In  order to cover the last video list page in following for loop
    pager_total_num = pager_total_num + 1
    for page_index in range(1, pager_total_num):
        page_index_num = page_index
        page_index_str = str(page_index_num)
        page_url = 'https://space.bilibili.com/' + uper_Uid_str + '/video?tid=0&page=' + page_index_str
        # Open FireFox
        browser = webdriver.Firefox()
        # Open uper's video list page
        browser.get(page_url)
        time.sleep(2)
        # Find all video href in this video list page
        vod_urlList = browser.find_elements_by_class_name('cover')
        # Create a file path for each video list page,all videos in this page will be downloaded in individual file
        Downlaod_directory = directory + '/page'+page_index_str
        isExists= os.path.exists(Downlaod_directory)
        if not isExists:
         os.makedirs(Downlaod_directory)
        href_list = []
        for url in vod_urlList:
            href = url.get_attribute("href")
            if href not in href_list:
              href_list.append(href)
        browser.close()
        # Counter of the downloaded video in this page
        count = 0
        for vod_href in href_list[count:]:
          count = count + 1
          print('Total videos in this page :',len(href_list))
          print(vod_href)
          print('Downloading the ', page_index, 'th page ', count, 'th video')
          try:
            sys.argv = ['you-get', '-o', Downlaod_directory, vod_href]
            you_get.main()
          except TypeError:
              time.sleep(2)
              sys.argv = ['you-get', '-o', Downlaod_directory, vod_href, '--debug']
              you_get.main()
# Set the file path to store videos
filepath = 'H:/软件脚本/python/B站视频批量下载/source_B/'
# Set Uper's Uid
uper_uid = 7375428
[pager_total_num, uper_name] = Get_VodPagesNum(uper_uid)
directory = filepath + uper_name
downloadUperVod(uper_uid, pager_total_num, directory)
