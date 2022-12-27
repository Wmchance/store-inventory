#Look at app.py in book_database_project to see how to clean the CSV data & load it into the db
# from models import Base, Book, session, engine

# import datetime
# import csv
# import time

# def add_csv():
#     with open('suggested_books.csv') as csvfile:
#         data = csv.reader(csvfile)
#         for row in data:
#             book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()
#             if book_in_db == None:
#                 title = row[0]
#                 author = row[1]
#                 date = clean_date(row[2])
#                 price = clean_price(row[3])
#                 new_book = Book(title=title, author=author, published_date=date, price=price)
#                 session.add(new_book)
#         session.commit()