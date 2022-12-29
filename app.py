from models import *
from functions import *

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    # In production, add add_csv('csv/brands.csv') first
    # add_csv('csv/inventory.csv')