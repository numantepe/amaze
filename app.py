from flask import Flask, request, render_template, jsonify, g

app = Flask(__name__)

@app.route("/")
def welcome_page():
    return render_template("index.html")
