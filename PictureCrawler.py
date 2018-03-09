import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
DIR_NAME = os.path.dirname(os.path.abspath(__file__))


def createFolder(directory):  # 創建資料夾工具
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def spiltHtml(html):  # 從網址篩出圖片編號工具 ex: http://www.mm131.com/xinggan/3730.html >> 3730
    a = html.split('/')
    b = a[len(a)-1]
    c = b.replace('.html', '')
    return c


class PicCrawler(object):
    # ChromeDriver設置
    chrome_path = DIR_NAME+'/chromedriver.exe'
    driver = webdriver.Chrome(chrome_path)

    # Scripts
    root_path = 'C:/Users/nick_z_chen/Desktop/'                                                 # 圖檔指定路徑
    root_folder_name = 'root'                                                                # 根目錄名稱
    root_folder_path = root_path + root_folder_name                                          # 根目錄路徑
    createFolder(root_folder_path)                                                           # 創建根目錄

    # URL設置
    base_url = 'http://www.mm131.com/'
    url = ['xinggan', 'qingchun', 'xiaohua', 'chemo', 'qipao', 'mingxing']
    first_level_link = []  # 第一層網址 空list
    first_level_folder_names = []  # 第一層資料夾名稱 空list
    first_level_folder_paths = []

    # 抓取分類 ex: 大学校花、清纯美女、性感美女
    for i in url:
        driver.get(base_url + i)                                                    # 開啟網址
        driver.find_element(By.XPATH, "//dl[@class='list-left public-box']")        # 抓取分類名稱定位
        first_folder_name = driver.find_element(
            By.XPATH, "(//dl[@class='list-left public-box']//a)[2][text()]").text   # 抓取分類名稱
        first_folder_path = os.path.join(root_folder_path, first_folder_name)       # 設定分類資料夾路徑
        createFolder(first_folder_path)                                             # 創建分類資料夾

        # 抓取分類底下一層 ex: 内地艺人戴予桐性感自拍、美女模特吴丹天生高贵丽
        first_level_link_elements = driver.find_elements(
            By.XPATH, "//dl[@class='list-left public-box']//dd/a[@target]")                  # 所有第一層分類定位 list

        for i in range(0, len(first_level_link_elements)):
            first_level_link.append(first_level_link_elements[i].get_attribute("href"))      # 第一層網址存進list
            first_level_folder_names.append(first_level_link_elements[i].text)               # 第一層資料夾名稱list
            first_level_folder_path = first_folder_path + '/' + first_level_folder_names[i]  # 第一層資料夾path
            createFolder(first_level_folder_path)                                            # 創建 第一層資料夾
            first_level_folder_paths.append(first_level_folder_path)                         # 第一層資料夾path 組成list

    # 抓取完資料關閉瀏覽器
    driver.close()

    # 使用上面功能抓取到的資料 開始抓圖
    for i in range(0, len(first_level_link)):
        num = 1  # 圖片起始編號 ex: 1.jpg
        while True:
            img_path = first_level_folder_paths[i] + '/' + str(num) + '.jpg'
            html = 'http://img1.mm131.me/pic/' + spiltHtml(first_level_link[i]) + '/' + str(num) + '.jpg'
            headers = {'Referer': 'http://www.mm131.com/'}
            r = requests.request("GET", html, headers=headers)
            if r.status_code == 200:                                                         # 直到抓圖失敗404就跳下一類別
                with open(img_path, 'wb') as f:
                    f.write(r.content)
                    f.close()
                print(html)
                print(img_path)
                num += 1
                continue
            break





















