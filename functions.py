#Look at app.py in book_database_project to see how to clean the CSV data & load it into the db
from models import Base, session, engine

import datetime
import csv
import time

# def check_csv():
#     with open('csv/inventory.csv') as csv_info:
#         data = csv.reader(csv_info)
#         price_col = []
#         for row in data:
#             price_list = (row[1].split('$'))
#             price_col.append(price_list)
#     for price_list in price_col[1:]:
#         price_float = float(price_list[1])
#         print_int = int(price_float*100)
#         print(print_int)

def clean_price(input_price):
    try:
        price_split = input_price.split('$')
        price_float = float(price_split[1])
    except ValueError:
        input('''
        \n**** Price Error ****
        \rThe date format should only include: dollars & cents separated with a period
        \rEx: 24.56
        \rPress Enter to try again
        \r********************''')
        return
    else:
        # print(int(price_float * 100))
        return int(price_float * 100)  

def clean_date(date_str):
    try:
        month = int(date_str.split('/')[0])
        day = int(date_str.split('/')[1])
        year = int(date_str.split('/')[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
        \n**** Date Error ****
        \rThe date format should be: MONTH DD, YYYY & in the past
        \rEx: March 22, 1965
        \rPress Enter to try again
        \r********************''')
        return
    else: 
        return return_date

def add_csv(input_file):
    with open(input_file) as csvfile:
        if input_file == 'csv/inventory.csv':
            data = csv.reader(csvfile)
            next(data) #skips header row
            for row in data:
                # book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()
                # if book_in_db == None:
                    product_name = row[0]
                    print(product_name)
                    price = clean_price(row[1])
                    print(price)
                    product_quantity = int(row[2])
                    print(product_quantity)
                    date_updated = clean_date(row[3])
                    print(date_updated)
                    # new_book = Book(title=title, author=author, published_date=date, price=price)
                # session.add(new_book)
            # session.commit()
        # elif input_file == 'csv/brands.csv':
        #     data = csv.reader(csvfile)
        #     for row in data:
        #         book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()
        #         if book_in_db == None:
        #             title = row[0]
        #             author = row[1]
        #             date = clean_date(row[2])
        #             price = clean_price(row[3])
        #             new_book = Book(title=title, author=author, published_date=date, price=price)
        #             session.add(new_book)
        #     session.commit()



add_csv('csv/inventory.csv')