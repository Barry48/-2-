import requests, re


url = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
response = requests.get(url)

match = re.findall(r'£\d+.\d{2}', response.text)

print(match)