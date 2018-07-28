import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    current_route = "index"
    return render_template("index.html", current_route=current_route, message="This is the index page of Brass Instruments Books")

@app.route('/add_book')
def add_book():
    current_route = "add_book"
    return render_template("add_book.html", current_route=current_route, message="This is the ADD BOOK page of Brass Instruments Books")


if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT', 8080)), debug=True)