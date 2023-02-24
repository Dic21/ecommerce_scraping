from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from datetime import date

today = date.today()

url = "https://www.hktvmall.com/hktv/zh/search?q=::category:BB01000001941:categoryHotPickOrder:BB01000001941"

driver = webdriver.Chrome("./chromedriver")
driver.implicitly_wait(30)
driver.get(url)
html = driver.page_source

csvfile = "hktv-supermarket.csv"

soup = BeautifulSoup(html, 'lxml')
product_div = soup.find("div", class_="productGrid")
brief_div = product_div.find_all("div", class_="product-brief")

# prepare data list
items = []
for index, row in enumerate(brief_div):
    item = []
    item.append(index+1)
    title = row.find("div", class_="brand-product-name")
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
    writer.writerow(["Ranking", "Goods", "URL", "Price", "RecordDate"])
    for item in items:
        writer.writerow(item)

driver.quit()