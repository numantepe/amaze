from flask import Flask, request, render_template, jsonify, g
from bs4 import BeautifulSoup
import requests

class Product:
    def __init__(self, image = None, desc = None, url = None, price = None, stars = None, ratings = None):
        self.image = image
        self.desc = desc
        self.url = url
        self.price = price
        self.stars = stars
        self.ratings = ratings

app = Flask(__name__)

@app.route("/")
def welcome_page():
    return render_template("index.html")

@app.route("/search-product", methods=["POST"])
def search_product():
    search_product = request.form.get("search_product")
    min_price = request.form.get("min_price")
    max_price = request.form.get("max_price")
    min_num_of_stars = request.form.get("min_num_of_stars")
    max_num_of_stars = request.form.get("max_num_of_stars")
    min_num_of_ratings = request.form.get("min_num_of_ratings")
    max_num_of_ratings = request.form.get("max_num_of_ratings")
    max_num_of_products = request.form.get("max_num_of_products")
    chosen_op = request.form.get("chosen_op") # op1 op2 op3 op4
    chosen_country = request.form.get("chosen_country")

    # OPTION 4 WILL BE AS MANY STARS AND RATINGS AS POSSIBLE AND ALSO AS CHEAP AS POSSIBLE

    amazon_url = ""
    if(chosen_country == "ca"):
        amazon_url = "https://www.amazon.ca"
    elif(chosen_country == "us"):
        amazon_url = "https://www.amazon.com"

    search_amazon_url = amazon_url + "/s?k="
    for word in search_product.split():
        search_amazon_url += word + "+"
    search_amazon_url = search_amazon_url[:-1]

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        #'referer': 'https://www.amazon.com/s?k=web+scraping+books&ref=nb_sb_noss',
        'upgrade-insecure-requests': '1',
        'cache-control': 'no-cache',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
        }

    r = requests.get(search_amazon_url, headers=headers)

    while(r.status_code > 500):
        r = requests.get(search_amazon_url, headers=headers)

    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'lxml')

    products = soup.select("div.s-result-item.s-asin")[3:]

    with open("html.txt", "w") as f:
        f.write(products[0].prettify())
    
    product_list = []

    for product in products:
        try:
            p = Product()

            h2_desc_url = product.select("h2")[0]
            p.desc = h2_desc_url.select("span.a-size-base-plus")[0].get_text()
            p.url = amazon_url + h2_desc_url.select("a")[0].get("href")

            p.image = product.select("img.s-image")[0].get("src")

            p.price = float(product.select("span.a-offscreen")[0].get_text()[1:])

            div_stars_ratings = product.select("div.a-section.a-spacing-none.a-spacing-top-micro")[0]
            p.stars = float(div_stars_ratings.select("span.a-icon-alt")[0].get_text()[:3])
            p.ratings = int(div_stars_ratings.select("span.a-size-base.s-underline-text")[0].get_text().replace(',', ''))
        except:
            pass

        product_list.append(p)

    for p in product_list:
        print(p.desc)
        print(p.url)
        print(p.image)
        print(p.price)
        print(p.stars)
        print(p.ratings)
        print("=====================")

    return  amazon_url
