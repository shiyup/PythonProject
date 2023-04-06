import time
#from mysqldb import DataManager
from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException,ElementNotInteractableException


browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)   #最多等待时间
#db = DataManager()

def index_page(page):
    '''
    自动切换页码
    :param page: 当前页码
    '''
    print('正在爬取第',page,'页')
    try:
        url = 'https://search.jd.com/Search?keyword=%E4%BA%AC%E4%B8%9C%E5%A4%A7%E8%8D%AF%E6%88%BF&enc=utf-8&pvid=20ed755a83784fd5b13356e7bb8f2008'
        browser.get(url)
        if page > 1:
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'#J_bottomPage .p-skip > input')) #找到输入页码的地方
            )
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_bottomPage .p-skip > a')) #找到确定按钮
            )
            input.clear() #清空
            input.send_keys(page) #输入页码
            submit.click()   #点击进行翻页
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#J_bottomPage .p-num > a.curr'),str(page))
            ) #比较当面页面是否是我们想要的页面
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_goodsList li')))
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight)') #用js进行下拉操作，如不这样，有部分数据加载不出来
        time.sleep(2)
        get_products()
    except TimeoutException:
        print('出错，重新爬取')
        index_page(page)
    except StaleElementReferenceException:
        print('等待刷新，重新爬取')
        index_page(page)
    except ElementNotInteractableException:
        print('不可交互，重新爬取')
        index_page(page)

def get_products():
    '''
    爬取药品信息
    '''
    html = browser.page_source
    doc = pq(html)
    items = doc('#J_goodsList li').items()
    for item in items:
        shop = item('.p-shop').text()                       #店铺名
        durg_name = item('.p-name em').text()               #药品名
        url = item('.p-name a').attr('href')                #详情链接
        efficacy = item('.p-name .promo-words').text()      #疗效
        price = item('.p-price').text()                     #价格
        comments = item('.p-commit a').text()               #评论人数
        print(shop,durg_name,url,efficacy,price,comments)
        product = [
            shop,durg_name,efficacy,price,comments
        ]
        #db.save_data(product)


if __name__ == '__main__':
    page = 3    #最多100页
    #for i in range(1,(page+1)):
    #   index_page(i)
    index_page(1)