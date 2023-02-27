from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

today = date.today()

list = [
    {
    'name': 'supermarket',
    'url': 'https://www.hktvmall.com/hktv/zh/search?q=::category:BB01000001941:categoryHotPickOrder:BB01000001941'
    },
    {
    'name': 'gadgets',
    'url': 'https://www.hktvmall.com/hktv/zh/search?q=::category:BB19000072661:categoryHotPickOrder:BB19000072661'
    }
]

final_index = len(list)-1

driver = webdriver.Chrome("./chromedriver")
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options = options)

def collect_data(cate, round):
    driver.get(cate['url'])
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'productGrid'))) 
    html = driver.page_source
    csvfile = f"hktv-{cate['name']}-{today}.csv"

    soup = BeautifulSoup(html, 'lxml')
    product_div = soup.find("div", class_="productGrid")
    brief_div = product_div.find_all("div", class_="product-brief")

    # prepare data list
    items = []
    for index, row in enumerate(brief_div):
        item = []
        item.append(index+1)
        title = row.find("div", class_="brand-product-name")
        brand = title.text.split(" - ")[0]
        item.append(brand)
        item.append(title.text.strip())

        href = row.find("a", recursive=False).get("href")
        link = "https://www.hktvmall.com/hktv/zh/"+href
        item.append(link)
        price = row.find("div", class_="price").find("span")
        item.append(price.text.strip())
        item.append(today)
        # set into items list
        items.append(item)

    #write to csv
    with open(csvfile, 'w+', newline="", encoding='UTF-8') as fp:
        writer = csv.writer(fp)

        writer.writerow(["Ranking", "Brand", "Goods", "URL", "Price", "RecordDate"])
        for item in items:
            writer.writerow(item)
    
    if(round == final_index):
        print("Finish!")

for i in range(len(list)):
    collect_data(list[i], i)

driver.quit()