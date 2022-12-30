#Look at app.py in book_database_project to see how to clean the CSV data & load it into the db
from models import *

import datetime
import csv

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
                inventory_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
                if inventory_in_db == None:
                    product_name = row[0]
                    product_price = clean_price(row[1])
                    product_quantity = int(row[2])
                    date_updated = clean_date(row[3])
                    query = session.query(Brands).filter(Brands.brand_name == row[4]).all()
                    for info in query:
                        brand_id = info.brand_id
                    new_product = Product(product_name=product_name, product_price=product_price, product_quantity=product_quantity, date_updated=date_updated, brand_id=brand_id)
                session.add(new_product)
            session.commit()
        elif input_file == 'csv/brands.csv':
            data = csv.reader(csvfile)
            next(data) #skips header row
            for row in data:
                brand_in_db = session.query(Brands).filter(Brands.brand_name==row[0]).one_or_none()
                if brand_in_db == None:
                    brand_name = row[0]
                    new_brand = Brands(brand_name=brand_name)
                    session.add(new_brand)
            session.commit()

# main menu - V: details of a single product - N: add a new product - A: view an analysis - B: make a backup
def menu():
    while True:
        print('''
            \nStore Inventory Menu\n
            \rV. See details of a product
            \rN. Add a new product
            \rA. See an analysis of all products
            \rB. Backup the database as a CSV file
            \rE. Exit
            ''')
        choice = input('What would you like to do? ')
        if choice in ['V', 'N', 'A', 'B', 'E']:
            return choice
        else:
            input('''
            \rPlease choose one of the options above
            \rPress enter to choose again
            ''')

# add brand name instead of brand_id
def get_product():
    current_product_ids = []
    for product_id_number in session.query(Product.product_id):
        current_product_ids.append(product_id_number[0])
    try:
        product_searched = int(input('\nPlease enter the product ID number: '))
        if product_searched in current_product_ids:
            result = (session.query(Product).filter(Product.product_id == product_searched).all())[0]
            product_brand = session.query(Brands.brand_name).filter(Brands.brand_id == result.brand_id).all()[0].brand_name
            print(f'''
                \nProduct details
                \r***************\n
                \rProduct name: {result.product_name}
                \rProduct price: ${result.product_price/100}
                \rNumber in stock: {result.product_quantity}
                \rDate updated: {result.date_updated}
                \rBrand of product: {product_brand}
            ''')
        else:
            raise Exception
    except Exception:
        input('\nSelected product ID does not exist. \nPress enter to try another product ID')
        get_product()
    # return(product_searched)

def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'V':
            get_product()
            input('\nPress any key to return to the main menu ')
            app()
        elif choice == 'E':
            app_running = False
    exit("\nSee you next time! \U0001f44b\n")


app()