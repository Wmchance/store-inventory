#Look at app.py in book_database_project to see how to clean the CSV data & load it into the db
from models import *

import datetime
import csv
from datetime import date

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
        \rThe date format should be: MM/DD/YYYY & in the past
        \rEx: 03/22/1965
        \rPress Enter to try again
        \r********************''')
        return
    else: 
        return return_date

def clean_quantity(given_quantity):
    try:
        cleaned_quantity = int(given_quantity)
    except ValueError:
        input('''
        \n**** Quantity Error ****
        \rThe quantity must be a whole number (Can't be fractions, decimals, or letters)
        \rEx: 10, 456, etc...
        \rPress Enter to enter a new quantity
        \r********************
        ''')
        return
    else:
        return cleaned_quantity


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
            \nStore Inventory Menu
            \r********************\n
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

def view_product():
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
        view_product()

def get_brand_id_from_brand_name():
    current_brand_names = []
    for products in session.query(Brands.brand_name):
        current_brand_names.append(products[0])
    print('\nCurrent brands:')
    index_list = []
    for index, brand in enumerate(current_brand_names, 1):
        print(f'{index}. {brand}')
        index_list.append(index)
    try:
        user_choice = int(input('\nSelect the brand by entering the corresponding number from the above list: '))
        if user_choice not in index_list:
            raise Exception
    except:
        input('''
        \n**** Brand Error ****
        \rThe entered value must be a number from the give list
        \rPress enter to prick the brand again
        \r**********************
        ''')
        return
    else:
        return user_choice

def add_product():
    print('''
    \nAdd new product
    \r***************\n''')
    product_name = input('Enter product name: ')
    quantity_error = True
    while quantity_error:
        product_quantity = clean_quantity(input('Enter the quantity of the product: '))
        if type(product_quantity) == int:
            quantity_error = False
    price_error = True
    while price_error:
        product_price = clean_price('$'+input('Enter the price in dollars & cents (ex. 25.28): '))
        if type(product_price) == int:
            price_error = False
    date_updated = today = date.today()
    brand_id_error = True
    while brand_id_error:
        brand_id = get_brand_id_from_brand_name()
        if type(brand_id) == int:
            brand_id_error = False
    product_in_db = session.query(Product).filter(Product.product_name == product_name).first()
    if product_in_db == None:
        new_product = Product(product_name=product_name, product_price=product_price, product_quantity=product_quantity, date_updated=date_updated, brand_id=brand_id)
        session.add(new_product)
    else:
        product_in_db.product_price=product_price
        product_in_db.product_quantity=product_quantity
        product_in_db.date_updated=date_updated
    session.commit()

def find_most_expensive_item():
    ordered_products = session.query(Product.product_name, Product.product_price).order_by(Product.product_price.desc()).all()
    return ordered_products[0]

def find_least_expensive_item():
    ordered_products = session.query(Product.product_name, Product.product_price).order_by(Product.product_price.asc()).all()
    return ordered_products[0]

# https://docs.sqlalchemy.org/en/14/core/tutorial.html
def count_brand_with_most_products():
    max_products_brand_info = (session.query(Product.brand_id, func.count(Product.brand_id).label('max_num')).group_by(Product.brand_id).order_by(desc('max_num')).all())[0]
    max_products_brand = session.query(Brands.brand_name).filter(Brands.brand_id == max_products_brand_info.brand_id).first()[0]
    max_product_info = [max_products_brand, max_products_brand_info.max_num]
    return max_product_info
    
def backup_dbs_to_csv():
    with open('backup_inventory.csv', 'w', newline='') as inventory_csv:
        fieldnames = Product.__table__.columns.keys()
        writer = csv.DictWriter(inventory_csv, fieldnames=fieldnames)
        writer.writeheader()
        inventory_db = session.query(Product)
        for row in inventory_db:
            writer.writerow({
                fieldnames[0]: row.product_id, 
                fieldnames[1]: row.product_name, 
                fieldnames[2]: row.product_quantity, 
                fieldnames[3]: '$'+str(row.product_price/100), 
                fieldnames[4]: f'{str(row.date_updated.month)}/{str(row.date_updated.day)}/{str(row.date_updated.year)}', 
                fieldnames[5]: session.query(Brands.brand_name).filter(Brands.brand_id == row.brand_id).first()[0]
                })

    with open('backup_brands.csv', 'w', newline='') as brands_csv:
        fieldnames = Brands.__table__.columns.keys()
        writer = csv.DictWriter(brands_csv, fieldnames=fieldnames)
        writer.writeheader()
        brands_db = session.query(Brands)
        for row in brands_db:
            writer.writerow({
                fieldnames[0]: row.brand_id, 
                fieldnames[1]: row.brand_name
                })


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'V':
            view_product()
            #Todo: Set input to uppercase 
            input('\nPress any key to return to the main menu ')
        elif choice == 'N':
            add_product()
            #Todo: Set input to uppercase 
            input('\nProduct added. \nPress any key to return to the main menu ')
        elif choice == 'A':
            print(f'''
            \nInventory Analysis
            \r******************\n
            \rMost Expensive Item: {find_most_expensive_item().product_name} - ${(find_most_expensive_item().product_price)/100}
            \rLeast Expensive Item: {find_least_expensive_item().product_name} - ${(find_least_expensive_item().product_price)/100}
            \rBrand with Most Products: {count_brand_with_most_products()[0]} - {count_brand_with_most_products()[1]} products
            ''')
            input('\nPress any key to return to the main menu ')
        elif choice == 'B':
            backup_dbs_to_csv()
            input('''
            \nBackups have been created & stored as the below filenames:
            \r'backup_inventory.csv' & 'backup_brands.csv'
            \nPress enter to return to the main menu''')
        elif choice == 'E':
            app_running = False
    exit("\nSee you next time! \U0001f44b\n")

app()