from models import *
from functions import *

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    # add_csv('csv/brands.csv')
    # add_csv('csv/inventory.csv')