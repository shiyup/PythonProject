import time
import csv
# from mysqldb import DataManager
from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementNotInteractableException

options = webdriver.ChromeOptions()
options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"')
options.add_argument('cookie="areaId=15; 3AB9D23F7A4B3C9B=ZJ6HXAFOI5QLVWKQW66R5NBBFZWQILO77CLOG6YIDDITTLYB743Q7GKBUTU3PEPSPGDWMY64B4HVN5QK7ZCXGYNC34; shshshfpx=3d912eea-b7b4-6b1f-a57f-61c614f9f51a-1662433170; shshshfpa=45111e38-40e2-8791-c65c-c6c0091a5f00-1680005791; __jdc=74320393; __jdv=74320393|search.jd.com|-|referral|-|1680005792249; shshshfpb=mwjSVOU_V2rvRiRv9AQkd4A; ipLoc-djd=15-1213-3038-59931; pin=mrs%E6%96%BDsyp; unick=mrs%E6%96%BDsyp; thor=85459431301E803C3BDA5CA4038A3898BECAA26D6A6E6AF626B5A13123B6010A9AEF4D6620E2EC3ED0131D134C85E6514E8463F63BF4707126037C1D77E1E5D6B6D227F892BBF70472C346B6DE8BB622FBD6B9F9F67ADC9CA28AB6C1D09B83C19664DCCEC64CA992BFF77EBA572B4F8F7A8A11117D48C1078F10C4384986FAE54947D9FE8BF5FE158D9C10264B69A24C; CA1AN5BV0CA8DS2EPC=79682569db0e18f3178300243cddcad5; PCA9D23F7A4B3CSS=7f13cf0a7c6e03369b9c897496ac3cc6; shshshfp=ebe2f17fe5aa5560a507a6dcd87fabb7; jsavif=1; 3AB9D23F7A4B3CSS=jdd03ZJ6HXAFOI5QLVWKQW66R5NBBFZWQILO77CLOG6YIDDITTLYB743Q7GKBUTU3PEPSPGDWMY64B4HVN5QK7ZCXGYNC34AAAAMHHJ475YAAAAAADNWLBAEDL3DF7YX; _gia_d=1; __jda=74320393.16800057922481165557535.1680005792.1680242100.1680313287.5; shshshsID=61e364828dcfd5e3b9af6693fa40ff11_2_1680313299417; __jdb=74320393.2.16800057922481165557535|5.1680313287"')
browser = webdriver.Chrome(chrome_options=options)
wait = WebDriverWait(browser, 100)  # 最多等待时间
fo = open("JdDrugInfo28.csv", "w", newline='', encoding='utf-8')
header = ["page", "url", "sku_id", "sku_name", "价格", "品牌", "商品名", "厂家", "通用名", "规格", "批准文号", "剂型"]
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
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.jPage > a.current'), str(page))
        )  # 比较当面页面是否是我们想要的页面
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.jSearchListArea li.jSubObject')))
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')  # 用js进行下拉操作，如不这样，有部分数据加载不出来
        time.sleep(2)
        get_products(page)
    except TimeoutException:
        print('出错')
        # index_page(page)
    except StaleElementReferenceException:
        print('等待刷新')
        #index_page(page)
    except ElementNotInteractableException:
        print('不可交互')
        # index_page(page)


def get_products(page):
    '''
    爬取药品信息
    '''
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    cookie = "shshshfpx=3d912eea-b7b4-6b1f-a57f-61c614f9f51a-1662433170; 3AB9D23F7A4B3C9B=ZJ6HXAFOI5QLVWKQW66R5NBBFZWQILO77CLOG6YIDDITTLYB743Q7GKBUTU3PEPSPGDWMY64B4HVN5QK7ZCXGYNC34; shshshfpa=4edf3f8f-2af8-2ed2-d3c1-fa3f8eae9aff-1680007260; __jdc=125919621; __jdv=125919621|direct|-|none|-|1680007260241; shshshfpb=e3bphjWhUtKtyKCvlVFUz4A; areaId=15; ipLoc-djd=15-1213-3038-59931; pin=mrs%E6%96%BDsyp; unick=mrs%E6%96%BDsyp; thor=85459431301E803C3BDA5CA4038A3898BAB6A7D7B18A8BEA58E48FDD20A06DE203723B81D9454708E02FF6D5A8BCC023845F901C524E1F74233317564F8646B7F57540DAAB9538ADD096FB86C35DF03DC4AEE8A9825817DDC9266C20C2304ED6DF8242A79BFE4BDFEC3FB191814ADFD980448751AD62EE2CF3BBC4773F32B96A1BEE969DEA597A313D45A978D2889052; shshshfp=ebe2f17fe5aa5560a507a6dcd87fabb7; 3AB9D23F7A4B3CSS=jdd03ZJ6HXAFOI5QLVWKQW66R5NBBFZWQILO77CLOG6YIDDITTLYB743Q7GKBUTU3PEPSPGDWMY64B4HVN5QK7ZCXGYNC34AAAAMHGG2RXPQAAAAADP7N73AGUUHGJYX; __jda=125919621.1680007260239169147394.1680007260.1680158802.1680166165.3"
    headers = {"User-Agent": user_agent, 'cookie': cookie}
    html = browser.page_source
    doc = pq(html)
    items = doc('.jSearchListArea li.jSubObject').items()
    for item in items:
        products = []
        drug_name = item('.jDesc a').text()  # 药品名
        url = "https:" + item('.jDesc a').attr('href')  # 详情链接

        print(drug_name, url)
        browser.get(url)
        time.sleep(5)
        detail_wait = WebDriverWait(browser, 100)
        # 等待找到sku-name
        detail_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sku-name')))
        detail_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.p-price span.price')))
        detail_html = browser.page_source
        detail_doc = pq(detail_html)
        # 获取当前页的skuId  (可能没有)
        sku_info_length = detail_doc("#choose-attrs .selected").length
        if sku_info_length == 0:
            products.append(get_drugs_soup(page, url, '', '', detail_doc))
        else:
            curr_sku_id = detail_doc("#choose-attrs .selected").eq(0).attr("data-sku")
            # 查询多个sku
            sku_items = detail_doc("#choose-attrs .item").items()
            for sku in sku_items:
                sku_id = sku.attr("data-sku")
                sku_name = sku.attr("data-value")
                if sku_id != curr_sku_id:
                    # 找下一个规格的药品
                    url = "https://item.jd.com/" + sku_id + ".html"
                    browser.get(url)
                    time.sleep(3)
                    detail_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sku-name')))
                    detail_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.p-price span.price')))
                    # 替换原来的detail_doc
                    detail_doc = pq(browser.page_source)
                products.append(get_drugs_soup(page, url, sku_id, sku_name, detail_doc))
        save_csv(products)

def get_drugs_soup(page, url, sku_id, sku_name, detail_doc):
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
    print(page, url, sku_id, sku_name, price, brand, goods_name, producer, common_name, spec, approval_num, dosage_form)
    return Drug(page, url, sku_id, sku_name, price, brand, goods_name, producer, common_name, spec, approval_num, dosage_form).array()



def save_csv(data):
    print(data)
    # 写入一行记录，以字典的形式，key需要与表头对应
    for item in data:
        item = dict(zip(header, item))
        writer.writerow(item)


class Drug():
    def __init__(self, page, url, sku_id, sku_name, price, brand, goods_name, producer, common_name, spec, approval_num,
                 dosage_form):
        self.page = page
        self.url = url
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
        return [self.page, self.url, self.sku_id, self.sku_name, self.price, self.brand, self.goods_name, self.producer, self.common_name, self.spec, self.approval_num, self.dosage_form]


if __name__ == '__main__':
    page = 125  # 最多125页
    for i in range(16, (page+1)):
        index_page(i)
        time.sleep(3)

