# 工具箱

from selenium import webdriver
def get_page(url):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    brwoser = webdriver.Chrome(chrome_options=option)
    try:
        brwoser.get(url)
        return brwoser.page_source
    except:
        print('请求ip网页失败')


