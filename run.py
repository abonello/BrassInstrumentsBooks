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

@app.route('/save_book', methods=['GET', 'POST'])
def save_book():
    if request.method == 'POST':
        title = request.form['title']
        volume = request.form['volume']
        bookNo = request.form['bookNo']
        composer = request.form['composer']
        arranger = request.form['arranger']
        publisher = request.form['publisher']
        clefs = []
        for ndx, clef in enumerate(["Treble Clef", "Bass Clef"]):
            if request.form.get('clefs'+str(ndx+1)) != None:
                clefs.append(clef)
        grades = ""
        for grade in range (1,9):
            if request.form.get('grade'+str(grade)) != None:
                grades += str(grade)
                grades += ", "
        grades = grades[0:-2]
        instruments = []
        for ndx, instrument in enumerate(["Trumpet / Cornet / Flugelhorn", "French Horn", "E flat Horn", "Trombone", "Baritone / Euphonium", "Bass Trombone", "Tuba"]):
            if request.form.get(str(ndx+1)) != None:
                instruments.append(instrument)
        comment = request.form['comment']

        store=""
        with open("data/books.json", "r") as readdata:
            store = readdata.read()
        book = json.loads(store)
        book[str(max(book['indexes'])+1)] = {   "title": title,
                                            "volume": volume,
                                            "bookNo": bookNo,
                                            "composer": composer,
                                            "arranger": arranger,
                                            "publisher": publisher,
                                            "clefs": clefs,
                                            "grades": grades,
                                            "instruments": instruments,
                                            "comment": comment}
        book['indexes'].append(max(book['indexes'])+1)

        with open("data/books.json", "w") as outfile:
            json.dump(book, outfile, sort_keys=True, indent=4)
        
        return "Trying to save this book. {}, {}, {}, {}, {}, {}, clefs:{}, grades: {}, instruments: {}, comment: {}".format(title, volume, bookNo, composer, arranger, publisher, clefs, grades, instruments, comment)
    return "POST was not accepted."



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