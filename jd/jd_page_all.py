import time
import csv
# from mysqldb import DataManager
from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementNotInteractableException

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 100)  # 最多等待时间
fo = open("drugListNew.csv", "w", newline='', encoding='utf-8')
header = ["page", "main_sku_id", "drug_name", "url", "sku_id", "price"]
# 创建一个DictWriter对象，第二个参数就是上面创建的表头
writer = csv.DictWriter(fo, header)
writer.writeheader()


# db = DataManager()

def index_page(page):
    '''
    自动切换页码
    :param page: 当前页码
    '''
    print('正在爬取第', page, '页')
    try:
        url = 'https://mall.jd.com/view_search-612358-1000015441-1000015441-0-0-0-0-1-' + str(page) + '-60.html'
        browser.get(url)
        time.sleep(2)
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.jPage > a.current'), str(page))
        )  # 比较当面页面是否是我们想要的页面
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.jSearchListArea li.jSubObject')))
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')  # 用js进行下拉操作，如不这样，有部分数据加载不出来
        time.sleep(2)
        get_products(page)
    except TimeoutException:
        print('出错')
        index_page(page)
    except StaleElementReferenceException:
        print('等待刷新')
        index_page(page)
    except ElementNotInteractableException:
        print('不可交互')
        index_page(page)


def get_products(page):
    '''
    爬取药品信息
    '''
    html = browser.page_source
    doc = pq(html)
    items = doc('.jSearchListArea li.jSubObject').items()
    products = []
    for item in items:
        drug_name = item('.jDesc a').text()  # 药品名
        main_sku_id = item('.jdNum').attr('jdprice')  # sku_id
        price = item('.jdNum').attr('preprice')  # 价格
        skus = item('.jScroll .jScrollWrap li').items()
        for sku in skus:
            url = sku.attr("data-href")     # 详情链接
            sku_id = sku.attr("sid")  # sku_id
            print(page, main_sku_id, drug_name, url, sku_id, price)
            products.append([page, main_sku_id, drug_name, url, sku_id, price])

    save_csv(products)



def save_csv(data):
    print(data)
    # 写入一行记录，以字典的形式，key需要与表头对应
    for item in data:
        item = dict(zip(header, item))
        writer.writerow(item)


if __name__ == '__main__':
    page = 125  # 最多125页
    for i in range(1, (page+1)):
        index_page(i)
        time.sleep(10)

