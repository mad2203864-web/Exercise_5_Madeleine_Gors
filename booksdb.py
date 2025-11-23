import sqlite3
from pathlib import Path

class BooksDB:
    def __init__(self):
        self.dbpath = Path(__file__).with_name('booksdb.sqlite')

    def getauthors(self):
        self.db = sqlite3.connect(self.dbpath.resolve())
        self.db.execute("PRAGMA foreign_keys = 1")
        cursor = self.db.execute("""SELECT author_id,first_name,last_name FROM authors ORDER BY last_name;""")
        authorlist = []
        # create our list of tuples that WTForms likes for SelectField
        for row in cursor:
            nexttuple = (row[0], f"{row[2]}, {row[1]}")
            authorlist.append(nexttuple)
        self.db.close()
        return authorlist

    def getbooksbyauthorid(self, authorid):
        self.db = sqlite3.connect(self.dbpath.resolve())
        self.db.execute("PRAGMA foreign_keys = 1")
        searchterm = (authorid,)  # Even if only one value, sqlite queries assume the parameters that match the ? are in a tuple
        cursor = self.db.execute("""SELECT b.title, b.yearpub,a.first_name,a.last_name,p.publisher_name
                        FROM books AS b INNER JOIN books_authors AS ba ON b.book_id = ba.book_id
                        INNER JOIN authors AS a ON a.author_id = ba.author_id
                        INNER JOIN publishers AS p  ON p.publisher_id = b.publisher_id
                        WHERE a.author_id = ?;""", searchterm)

        # we will now create a list of dictionaries (very JSON like) which is what Jinja2 Templates like
        booklist = []
        for row in cursor:
            booklist.append({'title': row[0], 'year': row[1], 'author': f"{row[3]}, {row[2]}", 'publisher': row[4]})
        self.db.close()
        return booklist

    def getpublishers(self):
        self.db = sqlite3.connect(self.dbpath.resolve())
        self.db.execute("PRAGMA foreign_keys = 1")
        cursor = self.db.execute("""SELECT publisher_id,publisher_name FROM publishers;""")
        # create our list of tuples that WTForms likes for SelectField
        publisherlist = []
        for row in cursor:
            nexttuple = (row[0],row[1])
            publisherlist.append(nexttuple)
        self.db.close()
        return publisherlist

    def getbooksbypublisherid(self,pubid):
        self.db = sqlite3.connect(self.dbpath.resolve())
        self.db.execute("PRAGMA foreign_keys = 1")
        searchterm = (pubid,)  # Even if only one value, sqlite queries assume the parameters that match the ? are in a tuple
        cursor = self.db.execute("""SELECT b.title, b.yearpub,a.first_name,a.last_name,p.publisher_name
                        FROM books AS b INNER JOIN books_authors AS ba ON b.book_id = ba.book_id
                        INNER JOIN authors AS a ON a.author_id = ba.author_id
                        INNER JOIN publishers AS p  ON p.publisher_id = b.publisher_id
                        WHERE p.publisher_id = ?;""", searchterm)
        # we will now create a list of dictionaries (very JSON like) which is what Jinja2 Templates like
        booklist = []
        for row in cursor:
            booklist.append({'title': row[0], 'year': row[1], 'author': f"{row[3]}, {row[2]}", 'publisher': row[4]})
        self.db.close()
        return booklist

    def getbooksbytitle(self, title):
        self.db = sqlite3.connect(self.dbpath.resolve())
        self.db.execute("PRAGMA foreign_keys = 1")
        #Note, this is a very expensive query in a relational database and probably sqlite as well
        title = f"%{title}%"
        searchterm = (title,)  # Even if only one value, sqlite queries assume the parameters that match the ? are in a tuple
        cursor = self.db.execute("""SELECT b.title, b.yearpub,a.first_name,a.last_name,p.publisher_name
                        FROM books AS b INNER JOIN books_authors AS ba ON b.book_id = ba.book_id
                        INNER JOIN authors AS a ON a.author_id = ba.author_id
                        INNER JOIN publishers AS p  ON p.publisher_id = b.publisher_id
                        WHERE b.title Like ?;""", searchterm)
        # we will now create a list of dictionaries (very JSON like) which is what Jinja2 Templates like
        booklist = []
        for row in cursor:
            booklist.append({'title': row[0], 'year': row[1], 'author': f"{row[3]}, {row[2]}", 'publisher': row[4]})
        self.db.close()
        return booklist
