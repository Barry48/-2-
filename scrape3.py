import json
import re

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag  # 明確導入 Tag 類型，以便進行檢查

URL = "https://www.books.com.tw/web/sys_saletopb/books/19?attribute=30"

try:
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "lxml")
    # 1. 先獲取整個列表，而不是直接存取索引
    book_list_uls = soup.find_all("ul", {"class": "clearfix"})

    # 2. 檢查列表長度是否足夠，這一步就防止了 IndexError
    if len(book_list_uls) > 2:
        book_list_ul = book_list_uls[2]

        # 3. 進行類型檢查 (這一步現在主要是為了 Pylance，因為我們幾乎可以確定它是 Tag)
        if isinstance(book_list_ul, Tag):
            books = []
            # 遍歷每個 <li> item (現在這裡已無任何警告)
            for item in book_list_ul.select(".item"):
                rank_tag = item.select_one(".stitle .no")
                title_tag = item.select_one(".type02_bd-a h4 a")
                price_tag = item.select_one(".type02_bd-a .msg .price_a")

                # 確保所有標籤都存在
                if not (rank_tag and title_tag and price_tag):
                    continue

                rank = rank_tag.text.strip()
                title = title_tag.text.strip()
                #author = author_tag.text.strip() if author_tag else "N/A"

                price_match = re.search(r"(\d+)元", price_tag.text)
                price = price_match.group(1) if price_match else "N/A"

                if int(rank) < 21:# 只取前20名
                    books.append(
                        {"title": title, "price": f"NT${price}", "rank": rank}
                    )

            # 格式化輸出和存檔...
            for book in books:
                print(
                    f"書名: {book['title']:<40} | 評分: {book['rank']:<10} | 價格: {book['price']}"
                )
            with open("books_info.json", "w", encoding="utf-8") as f:
                json.dump(books, f, ensure_ascii=False, indent=2)
                print("\n資料已儲存至 books_info.json")
except requests.RequestException as e:
    print(f"請求失敗: {e}")