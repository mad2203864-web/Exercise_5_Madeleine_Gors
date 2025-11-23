import sqlite3
import csv
from pathlib import Path

datadirectory = 'datafiles'
dpath = Path(__file__).resolve().parent

p = Path(dpath, datadirectory, 'publishers.csv')
print(p)
with p.open('r', newline='') as f:
    reader = csv.reader(f)
    publisher_data = [(int(row[0]), row[1]) for row in reader]

print(publisher_data)

p = Path(dpath, datadirectory, 'authors.csv')
with p.open('r', newline='') as f:
    reader = csv.reader(f)
    author_data = [(int(row[0]), row[1], row[2]) for row in reader]

print(author_data)

p = Path(dpath, datadirectory,'books_authors.csv')
with p.open('r', newline='') as f:
    reader = csv.reader(f)
    books_authors_data = [(int(row[0]), int(row[1]), int(row[2])) for row in reader]

print(books_authors_data)


def int_or_blank(value):
    try:
        return int(value)
    except ValueError:
        return ''


p = Path(dpath, datadirectory, 'books.csv')
with p.open('r', newline='') as f:
    reader = csv.reader(f)
    book_data = [(int(row[0]), row[1], int_or_blank(row[2]), int(row[3])) for row in reader]

print(book_data)

# creates db if does not exist, opens it if it does
# immediately turns on Foreign Key Support after the initial connect
p = Path(__file__).with_name('booksdb.sqlite')
dbconn = sqlite3.connect(p.resolve())
dbconn.execute("PRAGMA foreign_keys = 1")

dbconn.execute("""CREATE TABLE IF NOT EXISTS publishers                                                                                          
                (publisher_id INT PRIMARY KEY NOT NULL,                                                                                          
                publisher_name TEXT NOT NULL,                                                                                                    
                UNIQUE(publisher_name));                                                                                                         
                """)

dbconn.executemany("INSERT  or IGNORE into publishers (publisher_id,publisher_name) VALUES (?,?)", publisher_data)
dbconn.commit()

cursor = dbconn.execute("""SELECT publisher_id,publisher_name FROM publishers;""")

for row in cursor:
    print(
        f"""                                                                                                                                   
    publisher_id: {row[
            0]}                                                                                                                       
    publisher_name: {row[1]}""")

dbconn.execute("""CREATE TABLE IF NOT EXISTS authors                                                                                             
                (author_id INT PRIMARY KEY NOT NULL,                                                                                             
                first_name TEXT NOT NULL,                                                                                                        
                last_name TEXT NULL,                                                                                                             
                UNIQUE(last_name,first_name));                                                                                                   
                """)

dbconn.executemany("INSERT  or IGNORE into authors (author_id,first_name,last_name) VALUES (?,?,?)", author_data)
dbconn.commit()

cursor = dbconn.execute("""SELECT author_id,first_name,last_name FROM authors;""")

for row in cursor:
    print(
        f"""                                                                                                                                   
    author_id: {row[
            0]}                                                                                                                          
    first_name: {row[
            1]}                                                                                                                         
    last_name: {row[2]}""")

dbconn.execute("""CREATE TABLE IF NOT EXISTS books                                                                                               
            (book_id INT PRIMARY KEY NOT NULL,                                                                                                   
            title TEXT NOT NULL,                                                                                                                 
            yearpub INT NOT NULL,                                                                                                                
            publisher_id INT NOT NULL,                                                                                                           
            UNIQUE(title),                                                                                                                       
            FOREIGN KEY(publisher_id) REFERENCES publishers(publisher_id));                                                                      
            """)

dbconn.executemany("INSERT  or IGNORE into books (book_id,title,yearpub,publisher_id) VALUES (?,?,?,?)", book_data)
dbconn.commit()

cursor = dbconn.execute("""select book_id, title, yearpub, publisher_id  from books;""")

for row in cursor:
    print(
        f"""                                                                                                                                   
    book_id: {row[
            0]}                                                                                                                            
    title: {row[
            1]}                                                                                                                              
    yearpub: {row[
            2]}                                                                                                                            
    publisher_id: {row[
            3]}                                                                                                                       
    """)

dbconn.execute("""CREATE TABLE IF NOT EXISTS books_authors                                                                                       
                (book_id INT,                                                                                                                    
                author_id INT,                                                                                                                   
                author_order INT,                                                                                                                
                FOREIGN KEY(book_id) REFERENCES books(book_id),                                                                                  
                FOREIGN KEY(author_id) REFERENCES authors(author_id));                                                                           
                """)

dbconn.executemany("INSERT  or IGNORE into books_authors (book_id, author_id, author_order) VALUES (?,?,?)",
                   books_authors_data)
dbconn.commit()

cursor = dbconn.execute("SELECT book_id, author_id, author_order from books_authors;")

for row in cursor:
    print(
        f"""                                                                                                                                   
    book_id: {row[
            0]}                                                                                                                            
    author_id: {row[
            1]}                                                                                                                          
    author_order: {row[
            2]}                                                                                                                       
    """)
