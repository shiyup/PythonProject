import time
import requests
import csv
# from mysqldb import DataManager
from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementNotInteractableException
from bs4 import BeautifulSoup

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)  # 最多等待时间


# db = DataManager()

def index_page(page):
    '''
    自动切换页码
    :param page: 当前页码
    '''
    print('正在爬取第', page, '页')
    try:
        url = 'https://mall.jd.com/view_search-612358-1000015441-1000015441-0-0-0-0-1-1-60.html'
        browser.get(url)
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.jPage > a.current'), str(page))
        )  # 比较当面页面是否是我们想要的页面
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.jSearchListArea li.jSubObject')))
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')  # 用js进行下拉操作，如不这样，有部分数据加载不出来
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
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    cookie = "shshshfpx=3d912eea-b7b4-6b1f-a57f-61c614f9f51a-1662433170; 3AB9D23F7A4B3C9B=ZJ6HXAFOI5QLVWKQW66R5NBBFZWQILO77CLOG6YIDDITTLYB743Q7GKBUTU3PEPSPGDWMY64B4HVN5QK7ZCXGYNC34; shshshfpa=4edf3f8f-2af8-2ed2-d3c1-fa3f8eae9aff-1680007260; __jdc=125919621; __jdv=125919621|direct|-|none|-|1680007260241; shshshfpb=e3bphjWhUtKtyKCvlVFUz4A; areaId=15; ipLoc-djd=15-1213-3038-59931; pin=mrs%E6%96%BDsyp; unick=mrs%E6%96%BDsyp; thor=85459431301E803C3BDA5CA4038A3898BAB6A7D7B18A8BEA58E48FDD20A06DE203723B81D9454708E02FF6D5A8BCC023845F901C524E1F74233317564F8646B7F57540DAAB9538ADD096FB86C35DF03DC4AEE8A9825817DDC9266C20C2304ED6DF8242A79BFE4BDFEC3FB191814ADFD980448751AD62EE2CF3BBC4773F32B96A1BEE969DEA597A313D45A978D2889052; shshshfp=ebe2f17fe5aa5560a507a6dcd87fabb7; 3AB9D23F7A4B3CSS=jdd03ZJ6HXAFOI5QLVWKQW66R5NBBFZWQILO77CLOG6YIDDITTLYB743Q7GKBUTU3PEPSPGDWMY64B4HVN5QK7ZCXGYNC34AAAAMHGG2RXPQAAAAADP7N73AGUUHGJYX; __jda=125919621.1680007260239169147394.1680007260.1680158802.1680166165.3"
    headers = {"User-Agent": user_agent, 'cookie': cookie}
    html = browser.page_source
    doc = pq(html)
    items = doc('.jSearchListArea li.jSubObject').items()
    products = []
    fo = open("JdDrugInfo.csv", "w", newline='', encoding='utf-8')
    for item in items:
        drug_name = item('.jDesc a').text()  # 药品名
        url = "https:" + item('.jDesc a').attr('href')  # 详情链接

        print(drug_name, url)

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 获取当前页的skuId  (可能没有)
        sku_info = soup.select_one("#choose-attrs .selected");
        if sku_info is None:
            products.append(get_drugs_soup('', '', soup))
        else:
            curr_sku_id = soup.select_one("#choose-attrs .selected").get("data-sku")
            # 查询多个sku
            sku_items = soup.select("#choose-attrs .item")
            for sku in sku_items:
                sku_id = sku.get("data-sku")
                sku_name = sku.get("data-value")
                if sku_id != curr_sku_id:
                    response2 = requests.get("https://item.jd.com/" + sku_id + ".html", headers=headers)
                    # 替换原来的soup
                    soup = BeautifulSoup(response2.text, 'html.parser')
                products.append(get_drugs_soup(sku_id, sku_name, soup))
        save_csv(products, fo)
        # 关闭文件
        fo.close()
        break

def get_drugs_soup(sku_id, sku_name, soup):
    # 价格
    price = soup.select_one(".p-price span.price").text.strip()
    # 品牌
    brand = soup.select_one("#parameter-brand a").text.strip()
    # 商品名称
    goods_name = soup.select_one(".parameter2 li").get("title")
    # 规格与包装
    list_data = soup.select(".Ptable-item .clearfix")
    producer = '-'
    common_name = '-'
    spec = '-'
    approval_num = '-'
    dosage_form = '-'
    for info in list_data:
        name = info.select_one("dt").text.strip()
        if name == '生产企业':
            producer = info.select_one("dd").text.strip()
        if name == '药品通用名':
            common_name = info.select_one("dd").text.strip()
        if name == '产品规格':
            spec = info.select_one("dd").text.strip()
        if name == '批准文号':
            approval_num = info.select_one("dd").text.strip()
        if name == '剂型':
            dosage_form = info.select_one("dd").text.strip()
    print(sku_id, sku_name, price, brand, goods_name, producer, common_name, spec, approval_num, dosage_form)
    return Drug(sku_id, sku_name, price, brand, goods_name, producer, common_name, spec, approval_num, dosage_form).array()



def save_csv(data,fo):
    print(data)
    header = ["sku_id", "sku_name", "价格", "品牌", "商品名", "厂家", "通用名", "规格", "批准文号", "剂型"]
    # 创建一个DictWriter对象，第二个参数就是上面创建的表头
    writer = csv.DictWriter(fo, header)
    writer.writeheader()
    # 写入一行记录，以字典的形式，key需要与表头对应
    for item in data:
        item = dict(zip(header, item))
        writer.writerow(item)


class Drug():
    def __init__(self, sku_id, sku_name, price, brand, goods_name, producer, common_name, spec, approval_num,
                 dosage_form):
        self.sku_id = sku_id
        self.sku_name = sku_name
        self.price = price
        self.brand = brand
        self.goods_name = goods_name
        self.producer = producer
        self.common_name = common_name
        self.spec = spec
        self.approval_num = approval_num
        self.dosage_form = dosage_form

    def array(self):
        return [self.sku_id, self.sku_name, self.price, self.brand, self.goods_name, self.producer, self.common_name, self.spec, self.approval_num, self.dosage_form]


if __name__ == '__main__':
    page = 3  # 最多100页
    # for i in range(1,(page+1)):
    #   index_page(i)
    index_page(1)

