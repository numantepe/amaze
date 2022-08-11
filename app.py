from flask import Flask, request, render_template, jsonify, g

app = Flask(__name__)

@app.route("/")
def welcome_page():
    return render_template("index.html")

@app.route("/search-product", methods=["POST"])
def search_product():
    print("search_product:", request.form.get("search_product"))
    print("min_price:", request.form.get("min_price"))
    print("max_price:", request.form.get("max_price"))
    print("min_num_of_stars:", request.form.get("min_num_of_stars"))
    print("max_num_of_stars:", request.form.get("max_num_of_stars"))
    print("min_num_of_ratings:", request.form.get("min_num_of_ratings"))
    print("max_num_of_ratings:", request.form.get("max_num_of_ratings"))
    print("max_num_of_products:", request.form.get("max_num_of_products"))
    print("chosen_op:", request.form.get("chosen_op"))

    return "OOOOOOOKKKKKK"