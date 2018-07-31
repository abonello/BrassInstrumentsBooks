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
        book[str(max(book['indexes'])+1)] = {   "arranger": arranger,
                                                "bookNo": bookNo,
                                                "clefs": clefs,
                                                "comment": comment,
                                                "composer": composer,
                                                "grades": grades,
                                                "id": max(book['indexes'])+1,
                                                "img": "",
                                                "instruments": instruments,
                                                "pieces": [],
                                                "publisher": publisher,
                                                "title": title,
                                                "volume": volume
                                            }
        book['indexes'].append(max(book['indexes'])+1)

        with open("data/books.json", "w") as outfile:
            json.dump(book, outfile, sort_keys=True, indent=4)
        
        currentRoute = "index"
        message = "Trying to save this book. {}, {}, {}, {}, {}, {}, clefs:{}, grades: {}, instruments: {}, comment: {}".format(title, volume, bookNo, composer, arranger, publisher, clefs, grades, instruments, comment)
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
    return render_template("view_book_details.html", current_route=currentRoute, message="", thisBook=thisBook)
    # return render_template("view_book_details.html", current_route=currentRoute, message="This is the detailed view of book with ID:{}.".format(id), thisBook=thisBook)

@app.route('/add_piece/<id>')
def add_piece(id):
    store=""
    with open("data/books.json", "r") as readdata:
        store = readdata.read()
    books = json.loads(store)
    thisBook = books[id]
    currentRoute = "add_piece"
    return render_template("add_piece.html", current_route=currentRoute, message="This is the ADD PIECE page of Brass Instruments Books", thisBook=thisBook)

@app.route('/save_new_piece/<id>', methods=['GET', 'POST'])
def save_new_piece(id):
    # print("Received data for book with id: {}".format(id))

    if request.method == 'POST': 
        backupData()
        store=""
        with open("data/books.json", "r") as readdata:
            store = readdata.read()
        books = json.loads(store)
        thisBook = books[id]
        try:
            thisBook['pieces']
            this_id = max(thisBook['pieces'][0])+1
            thisBook['pieces'][0].append(this_id)
        except:
            # print("There were no pieces set yet")
            # thisBook['pieces'] = [{"entries": [], "p_index": [], "numberInBook": "", 
            #                         "pieceComposer": "", "pieceTitle": ""}]
            # thisBook['pieces'] = [[],{}]
            this_id = 1
            thisBook['pieces'] = [[this_id],{}]


        

        thisPiece={}
        thisPiece['pieceTitle'] = request.form['title']
        thisPiece['numberInBook'] = request.form['number']
        thisPiece['pieceComposer'] = request.form['composer']
        thisPiece['p_index'] = this_id
        # thisPiece['entries'] = []
        thisPiece['instrument'] = request.form['instrument']
        thisPiece['grade'] = request.form['grade']
        thisPiece['list'] = request.form['list']
        thisPiece['syllabusYear'] = request.form['syllabusYear']
        thisPiece['comment'] = request.form['comment']


        # entry = {}
        # entry['instrument'] = request.form['instrument']
        # entry['grade'] = request.form['grade']
        # if request.form['optradio1']:
        #     entry['list'] = 'A'
        # elif request.form['optradio2']:
        #     entry['list'] = 'B'
        # elif request.form['optradio3']:
        #     entry['list'] = 'C'
        # entry['list'] = request.form['list']
        # entry['syllabusYear'] = request.form['syllabusYear']
        # entry['comment'] = request.form['comment']
        # thisPiece['entries'].append(entry)
        # thisPiece['p_index'].append(this_id)
        thisBook['pieces'][1][str(this_id)] = thisPiece



        with open("data/books.json", "w") as outfile:
            json.dump(books, outfile, sort_keys=True, indent=4)

    currentRoute="view_book_details"
    return render_template("view_book_details.html", current_route=currentRoute, message="", thisBook=thisBook)

def backupData():
    store=""
    storeBkU1=""
    storeBkU2=""
    with open("data/books.json", "r") as readdata:
        store = readdata.read()
    dataNow = json.loads(store)
    with open("data/books_bkup1.json", "r") as bkup1:
        storeBkU1 = bkup1.read()
    dataBkU1 = json.loads(storeBkU1)
    with open("data/books_bkup2.json", "r") as bkup2:
        storeBkU2 = bkup2.read()
    dataBkU2 = json.loads(storeBkU2)
    with open("data/books_bkup1.json", "w") as outfile:
        json.dump(dataNow, outfile, sort_keys=True, indent=4)
    with open("data/books_bkup2.json", "w") as outfile:
        json.dump(dataBkU1, outfile, sort_keys=True, indent=4)
    with open("data/books_bkup3.json", "w") as outfile:
        json.dump(dataBkU2, outfile, sort_keys=True, indent=4)
    
@app.route('/delete_book/<id>', methods=['GET', 'POST'])
def delete_book(id): 
    backupData()
    currentRoute = "view_books"
    store=""
    with open("data/books.json", "r") as readdata:
        store = readdata.read()
    books = json.loads(store)
    thisBook = books.pop(id, None)
    books['indexes'].remove(int(id))
    with open("data/books.json", "w") as outfile:
            json.dump(books, outfile, sort_keys=True, indent=4)
    # return "Books: {}<br><hr><br>{}".format(books, thisBook)
    # return "Did not receive a POST method."
    return render_template("view_books.html", current_route=currentRoute, message="This is the VIEW BOOKS page of Brass Instruments Books", books=books)

@app.route('/delete_piece/<id>/<p_index>', methods=['GET', 'POST'])
def delete_piece(id, p_index): 
    # print("Reached delete_piece Route")
    # print("id: {}".format(id))
    # print("type(id): {}".format(type(id)))
    # print("p_index: {}".format(p_index))
    backupData()


    currentRoute = "view_books"
    store=""
    with open("data/books.json", "r") as readdata:
        store = readdata.read()
    books = json.loads(store)


    # thisBook = books.pop(id, None)
    # books['indexes'].remove(int(id))
    

    # print(books['indexes'])
    # print(books[id]['pieces'])
    # books[id]['pieces'].remove(int(p_index))
    print(books[id]['pieces'][1][p_index])
    thisBook = books[id]['pieces'][1].pop(p_index, None)
    print("Item deleted: {}".format(thisBook))
    print("Items remaining: {}".format(books))

    books[id]['pieces'][0].remove(int(p_index))
    # print(books)
    # print(books[1]['id']['pieces'][0])
    # print(books[str('id')])
    with open("data/books.json", "w") as outfile:
            json.dump(books, outfile, sort_keys=True, indent=4)
    # return "Books: {}<br><hr><br>{}".format(books, thisBook)
    # return "Did not receive a POST method."
    # return "Reached delete_piece route."
    return render_template("view_books.html", current_route=currentRoute, message="This is the VIEW BOOKS page of Brass Instruments Books", books=books)

@app.route('/edit_book/<id>', methods=['GET', 'POST'])
def edit_book(id):
    currentRoute = "edit_book"
    store=""
    with open("data/books.json", "r") as readdata:
        store = readdata.read()
    books = json.loads(store)
    thisBook = books.pop(id, None)
    return render_template("edit_book.html", current_route=currentRoute, message="This is the EDIT BOOK page of Brass Instruments Books", thisBook=thisBook)
    # return ("Edit book with ID: {}".format(id))

@app.route('/save_book_edit/<id>', methods=['GET', 'POST'])
def save_book_edit(id):
    if request.method == 'POST':
        backupData()
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
        # pieces=book[id]['pieces']
        # img=book[id]['img']



        book[id]["arranger"] = arranger
        book[id]["bookNo"] = bookNo
        book[id]["clefs"] = clefs
        book[id]["comment"] = comment
        book[id]["composer"] = composer
        book[id]["grades"] = grades
        book[id]["instruments"] = instruments
        book[id]["publisher"] = publisher
        book[id]["title"] = title
        book[id]["volume"] = volume

        # book[str(max(book['indexes']))] = {   "arranger": arranger,
        #                                         "bookNo": bookNo,
        #                                         "clefs": clefs,
        #                                         "comment": comment,
        #                                         "composer": composer,
        #                                         "grades": grades,
        #                                         "id": max(book['indexes'])+1,
        #                                         "img": "",
        #                                         "instruments": instruments,
        #                                         "pieces": ,
        #                                         "publisher": publisher,
        #                                         "title": title,
        #                                         "volume": volume
        #                                     }
        # book['indexes'].append(max(book['indexes'])+1)

        with open("data/books.json", "w") as outfile:
            json.dump(book, outfile, sort_keys=True, indent=4)
        
        currentRoute = "index"
        # message = "<p>Trying to save this book.<br> id: {},<br> title{},<br> volume: {},<br> bookNo: {},<br> composer: {},<br> arranger: {},<br> publisher: {},<br> clefs: {},<br> grades: {},<br> instruments: {},<br> comment: {},<br> pieces: {},<br> img: {}</p>".format(id, title, volume, bookNo, composer, arranger, publisher, clefs, grades, instruments, comment, pieces, img)
        # return message
        message = "Book {} is updated.".format(id)
        return render_template("index.html", current_route=currentRoute, message=message)
    # return "POST was not accepted."

if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT', 8080)), debug=True)