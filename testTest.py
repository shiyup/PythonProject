import time
from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait






if __name__ == '__main__':
    detail_browser = webdriver.Chrome()
    detail_browser.get("https://item.jkcsjd.com/4201264.html")
    time.sleep(2)
    detail_wait = WebDriverWait(detail_browser, 60)
    # 等待找到sku-name
    detail_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sku-name')))
    detail_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.p-price span.price')))

    detail_html = detail_browser.page_source
    detail_doc = pq(detail_html)
    # 价格
    price = detail_doc(".p-price span.price").eq(0).text()
    print(price)

    detail_browser.execute_script("window.open('https://item.jkcsjd.com/3083217.html')")
    detail_html = detail_browser.page_source
    detail_doc = pq(detail_html)

    # 价格
    price = detail_doc(".p-price span.price").eq(0).text()
    print(price)