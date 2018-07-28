import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    currentRoute = "index"
    return render_template("index.html", current_route=currentRoute, message="This is the index page of Brass Instruments Books")

@app.route('/add_book')
def add_book():
    currentRoute = "add_book"
    return render_template("add_book.html", current_route=currentRoute, message="This is the ADD BOOK page of Brass Instruments Books")

@app.route('/add_piece')
def add_piece():
    currentRoute = "add_piece"
    bookInfo = {}
    bookInfo['title'] = "An Example book"
    bookInfo['volume'] = "2"
    bookInfo['book'] = "1"
    bookInfo['composer'] = "Beethoven"
    bookInfo['arranger'] = "Someone"
    bookInfo['publisher'] = "ABRSM"
    return render_template("add_piece.html", current_route=currentRoute, message="This is the ADD PIECE page of Brass Instruments Books", bookInfo=bookInfo)


if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT', 8080)), debug=True)