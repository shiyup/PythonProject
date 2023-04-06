import time
import csv
# from mysqldb import DataManager
from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementNotInteractableException

fo = open("drugDetail.csv", "w", newline='', encoding='utf-8')
header = ["url", "sku_id", "价格", "品牌", "商品名", "厂家", "通用名", "规格", "批准文号", "剂型"]
# 创建一个DictWriter对象，第二个参数就是上面创建的表头
writer = csv.DictWriter(fo, header)
writer.writeheader()


def deal_detail(url, sku_id, browser, wait):
    real_url = "https:" + url
    browser.get(real_url)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.sku-name'))
    )
    # 用js进行下拉操作，如不这样，有部分数据加载不出来
    browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(10)
    html = browser.page_source
    detail_doc = pq(html)
    # 价格
    price = detail_doc(".p-price span.price").eq(0).text()
    # 品牌
    brand = detail_doc("#parameter-brand a").eq(0).text()
    # 商品名称
    goods_name = detail_doc(".parameter2 li").eq(0).attr("title")
    # 规格与包装
    list_data = detail_doc(".Ptable-item .clearfix").items()
    producer = '-'
    common_name = '-'
    spec = '-'
    approval_num = '-'
    dosage_form = '-'
    products = []
    for info in list_data:
        name = info("dt").text()
        if name == '生产企业':
            producer = info("dd").text()
        if name == '药品通用名':
            common_name = info("dd").text()
        if name == '产品规格':
            spec = info("dd").text()
        if name == '批准文号':
            approval_num = info("dd").text()
        if name == '剂型':
            dosage_form = info("dd").text()
    print(real_url, sku_id, price, brand, goods_name, producer, common_name, spec, approval_num, dosage_form)
    products.append(
        [real_url, sku_id, price, brand, goods_name, producer, common_name, spec, approval_num, dosage_form])
    save_csv(products)


def save_csv(data):
    # 写入一行记录，以字典的形式，key需要与表头对应
    for item in data:
        item = dict(zip(header, item))
        print(data)
        writer.writerow(item)


if __name__ == '__main__':
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 60)  # 最多等待时间
    with open('./drugListNew.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sku_id = row['sku_id']
            url = row['url']
            print(sku_id, url)
            try:
                deal_detail(url, sku_id, browser, wait)
            except TimeoutException:
                browser.close()
                # 重新开一个窗口
                browser = webdriver.Chrome()
                wait = WebDriverWait(browser, 60)
                deal_detail(url, sku_id, browser, wait)
