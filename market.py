# Scraping Market Website (Fetching important data)

from requests_html import HTMLSession
import csv

# Website URL
url = "https://barefootbuttons.com/product-category/version-1/"
ses = HTMLSession()

def get_links(url): 
  req = ses.get(url)
  
  items = req.html.find("div.product-small.box")
  links = [item.find("a", first=True).attrs["href"] for item in items]
  
  return links

def get_product(link):
  req = ses.get(link)

  title = req.html.find("h1", first=True).full_text
  price = req.html.find("span.woocommerce-Price-amount.amount bdi")[1].full_text # That's means we want the bdi tag that its after this class
  sku = req.html.find("span.sku", first=True).full_text
  category = req.html.find("a[rel=tag]", first=True).full_text

  product = {
    "title": title.strip(),
    "price": price.strip(),
    "sku": sku.strip(),
    "Category": category.strip(),
  }

  print(product)
  return product


products_number = len(get_links(url))
print(f"Products Number: {products_number}")

results = []

for link in get_links(url): 
  results.append(get_product(link))

print(results)

try: 
  with open("market.csv", "w", encoding="UTF-8", newline="") as mf: 
    wr = csv.DictWriter(mf, fieldnames= results[0].keys(),)
    wr.writeheader()
    wr.writerows(results)

  print("File Created.")








except Exception as e: 
  print(f"Error: {e}")




