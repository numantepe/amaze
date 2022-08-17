from flask import Flask, request, render_template, jsonify, g
from bs4 import BeautifulSoup
import requests
import lxml
import cchardet 
import chardet
import threading

app = Flask(__name__)

def get_html_doc(requests_session, search_amazon_url, html_docs, i):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'referer': search_amazon_url + "&ref=nb_sb_noss",
        'upgrade-insecure-requests': '1',
        'cache-control': 'no-cache',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
        }

    r = requests_session.get(search_amazon_url, headers=headers)

    while(r.status_code > 500):
        r = requests_session.get(search_amazon_url, headers=headers)

    html_docs[i] = r.content #or r.text?

def scrape_html_doc(chosen_country, amazon_url, product_set, html_doc): 
    soup = BeautifulSoup(html_doc, 'lxml')

    products = soup.select("div.s-result-item.s-asin")

    #with open("html.txt", "w") as f:
    #    f.write(products[0].prettify())

    for product in products:
        try:
            h2_desc_url = product.select("h2")[0]

            if(chosen_country == "ca"):
                desc = h2_desc_url.select("span.a-size-base-plus")[0].get_text()
            elif(chosen_country == "us"):
                desc = h2_desc_url.select("span.a-size-medium")[0].get_text()
            url = amazon_url + h2_desc_url.select("a")[0].get("href")

            image = product.select("img.s-image")[0].get("src")

            price = float(product.select("span.a-offscreen")[0].get_text()[1:])

            div_stars_ratings = product.select("div.a-section.a-spacing-none.a-spacing-top-micro")[0]

            stars = float(div_stars_ratings.select("span.a-icon-alt")[0].get_text()[:3])
            ratings = int(div_stars_ratings.select("span.a-size-base.s-underline-text")[0].get_text().replace(',', ''))

            max_ratings_min_price = ratings / price 
            max_stars_min_price = stars / price
            max_ratings_max_stars = ratings / (5.0 - stars)
            max_ratings_max_stars_min_price = (ratings / (5 - 0 - stars)) / price

            t = (desc, url, image, price, stars, ratings, max_ratings_min_price,
                max_stars_min_price, max_ratings_max_stars, max_ratings_max_stars_min_price)

            product_set.append(t)
        except:
            pass

@app.route("/")
def welcome_page():
    return render_template("index.html")

@app.route("/search-product", methods=["POST"])
def search_product():
    search_product = request.form.get("search_product")
    chosen_country = request.form.get("chosen_country")

    amazon_url = ""
    if(chosen_country == "ca"):
        amazon_url = "https://www.amazon.ca"
    elif(chosen_country == "us"):
        amazon_url = "https://www.amazon.com"

    search_amazon_url = amazon_url + "/s?k="
    for word in search_product.split():
        search_amazon_url += word + "+"
    search_amazon_url = search_amazon_url[:-1]

    product_list = [] 

    requests_session = requests.Session()

    np = 0
    if(chosen_country == "ca"):
        np = 8
    elif(chosen_country == "us"):
        np = 21

    search_amazon_urls = [search_amazon_url + "&page=" + str(i) for i in range(1, np)]

    threads = [None] * (np - 1)
    html_docs = [None] * (np - 1)
    for i in range(np - 1):
        t = threading.Thread(target=get_html_doc, args=[requests_session, search_amazon_urls[i], html_docs, i])
        t.start()
        threads[i] = t
    for thread in threads:
        thread.join()
 
    for i in range(np - 1):
        scrape_html_doc(chosen_country, amazon_url, product_list, html_docs[i])

    print("length:", len(product_list))

    #with open("items.txt", "w") as f:
    #    for p in list(product_list):
    #        for x in p:
    #            f.write(str(x))
    #            f.write("\n")
    #        f.write("===============")
    #    f.write("\n")

    found = []

    for p in product_list:
        found.append({"desc" : p[0], "url" : p[1], "image" : p[2], 
                        "price" : p[3], "stars" : p[4], "ratings" : p[5],
                        "max_ratings_min_price" : p[6],
                        "max_stars_min_price" : p[7],
                        "max_ratings_max_stars" : p[8],
                        "max_ratings_max_stars_min_price" : p[9]})

    return jsonify(found) 

if __name__ == '__main__':
    app.run()
