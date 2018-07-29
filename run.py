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
        # pieces = {
        #     "pieceTitle":"",
        #     "numberInBook":"",
        #     "pieceComposer":"",
        #     "entries": [
        #         {
        #             "instrument": "",
        #             "grade": "",
        #             "syllabusYear": "",
        #             "list": ""
        #         }
        #     ]
        # }

        store=""
        with open("data/books.json", "r") as readdata:
            store = readdata.read()
        book = json.loads(store)
        book[str(max(book['indexes'])+1)] = {   "id": max(book['indexes'])+1,
                                                "title": title,
                                                "volume": volume,
                                                "bookNo": bookNo,
                                                "composer": composer,
                                                "arranger": arranger,
                                                "publisher": publisher,
                                                "clefs": clefs,
                                                "grades": grades,
                                                "instruments": instruments,
                                                "comment": comment
                                                }
        book['indexes'].append(max(book['indexes'])+1)

        with open("data/books.json", "w") as outfile:
            json.dump(book, outfile, sort_keys=True, indent=4)
        
        currentRoute = "index"
        message = "Trying to save this book. {}, {}, {}, {}, {}, {}, clefs:{}, grades: {}, instruments: {}, comment: {}".format(title, volume, bookNo, composer, arranger, publisher, clefs, grades, instruments, comment)
        # return "Trying to save this book. {}, {}, {}, {}, {}, {}, clefs:{}, grades: {}, instruments: {}, comment: {}".format(title, volume, bookNo, composer, arranger, publisher, clefs, grades, instruments, comment)
        return render_template("index.html", current_route=currentRoute, message=message)
    return "POST was not accepted."

@app.route('/view_books')
def view_books():
    currentRoute = "view_books"
    store=""
    with open("data/books.json", "r") as readdata:
        store = readdata.read()
    books = json.loads(store)
    
    return render_template("view_books.html", current_route=currentRoute, message="This is the VIEW BOOKS page of Brass Instruments Books", books=books)

@app.route('/view_book_details/<id>')
def view_book_details(id):
    currentRoute = "view_book_details"
    store=""
    with open("data/books.json", "r") as readdata:
        store = readdata.read()
    books = json.loads(store)
    thisBook = books[id]
    # return "This is the detailed view of book with ID:{}. <br>This book is {}".format(id, thisBook)
    return render_template("view_book_details.html", current_route=currentRoute, message="This is the detailed view of book with ID:{}.".format(id), thisBook=thisBook)

@app.route('/add_piece/<id>')
def add_piece(id):
    store=""
    with open("data/books.json", "r") as readdata:
        store = readdata.read()
    books = json.loads(store)
    thisBook = books[id]
    currentRoute = "add_piece"
    # bookInfo = {}
    # bookInfo['title'] = thisBook['title']
    # bookInfo['volume'] = thisBook['volume']
    # bookInfo['book'] = thisBook['bookNo']
    # bookInfo['composer'] = thisBook['composer']
    # bookInfo['arranger'] = thisBook['arranger']
    # bookInfo['publisher'] = thisBook['publisher']
    return render_template("add_piece.html", current_route=currentRoute, message="This is the ADD PIECE page of Brass Instruments Books", thisBook=thisBook)
    # return render_template("add_piece.html", current_route=currentRoute, message="This is the ADD PIECE page of Brass Instruments Books", bookInfo=bookInfo)


@app.route('/save_new_piece/<id>', methods=['GET', 'POST'])
def save_new_piece(id):
    print("Received data for book with id: {}".format(id))
    if request.method == 'POST': 
        store=""
        with open("data/books.json", "r") as readdata:
            store = readdata.read()
        books = json.loads(store)
        thisBook = books[id]
        try:
            thisBook['pieces']
            # print(pieces)
        except:
            print("There were no pieces set yet")
            thisBook['pieces'] = []
            # pieces = thisBook['pieces']

        thisPiece={}
        thisPiece['pieceTitle'] = request.form['title']
        thisPiece['numberInBook'] = request.form['number']
        thisPiece['pieceComposer'] = request.form['composer']
        thisPiece['entries'] = []
        entry = {}
        entry['instrument'] = request.form['instrument']
        entry['grade'] = request.form['grade']
        # entry['list'] = request.form['list']
        if request.form['optradio1']:
            entry['list'] = 'A'
        elif request.form['optradio2']:
            entry['list'] = 'B'
        elif request.form['optradio3']:
            entry['list'] = 'C'
        entry['syllabusYear'] = request.form['syllabusYear']
        thisPiece['entries'].append(entry)
        # thisPiece['instrument'] = request.form['instrument']
        # thisPiece['grade'] = request.form['grade']
        # thisPiece['list'] = request.form['list']
        # thisPiece['syllabusYear'] = request.form['syllabusYear']

        # pieces = {
        #     "pieceTitle":"",
        #     "numberInBook":"",
        #     "pieceComposer":"",
        #     "entries": [
        #         {
        #             "instrument": "",
        #             "grade": "",
        #             "syllabusYear": "",
        #             "list": ""
        #         }
        #     ]
        # }

        # print(thisPiece)
        thisBook['pieces'].append(thisPiece)
        
        # print(thisBook)
        # books[thisBook['id']] = thisBook
        

        with open("data/books.json", "w") as outfile:
            json.dump(books, outfile, sort_keys=True, indent=4)




    currentRoute="view_book_details"
    return render_template("view_book_details.html", current_route=currentRoute, message="", thisBook=thisBook)



if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT', 8080)), debug=True)