import requests
import json
from bs4 import BeautifulSoup

#使用 lxml 解析器 (推薦：速度快、容錯性強)
try:
    response = requests.get("http://books.toscrape.com/catalogue/category/books/travel_2/index.html")
    response.encoding = "utf-8"
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    print("--- 使用 lxml 解析成功 ---")

except requests.RequestException as e:
    print(f"網路請求失敗: {e}")

articles = soup.find_all('article', class_='product_pod')

books = []
for article in articles:
    title = article.h3.a.get('title')  #.h3.a 取得 h3 標籤下的 a 標籤，.get('title') 取得 title 屬性值
    price = article.find('p', class_='price_color').text
    rating = article.p.get('class')[1]

    books.append(
        {"title": title, "price": price, "rating": rating}
    )
#格式化輸出和存檔...
for book in books:
    print(
        f"書名: {book['title']:<40} | 評分: {book['rating']:<10} | 價格: {book['price']}"
    )

with open("books_info.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, indent=2)
print("\n資料已儲存至 books_info.json")