from mydbutils import make_connection, executeScriptsFromFile, read_config, display_database
from mysql.connector import Error
from sqlalchemy import URL, create_engine, text
import argparse
import pandas as pd


def create_schema(config_file='superstore_test_db.ini', filename = 'superstore_test_db.sql'):
    conn = make_connection(config_file, section = 'mysql', 
                       list_remove_from_config = ['drivername', 'database','username'])
    executeScriptsFromFile(conn, filename)


def load_data_from_csv(database = 'superstore_test_db', config_file='superstore_test_db.ini'):
    config = read_config(config_file, section = 'mysql', list_remove_from_config = ['user'])
    url_object = URL.create(**config)
    engine = create_engine(url_object)
    print(engine)

    # read csv, define col names
    data = pd.read_csv("train.csv", skiprows=1, names=['row_id', 'OrderID','OrderDate','ShipDate','ShipMode','CustomerID','CustomerName','Segment','Country','City','State','PostalCode','Region','ProductID','Category','SubCategory','ProductName','Sales'])
    pd.set_option('display.max_columns', None)
    # Convert the date columns to date format
    data["OrderDate"] = pd.to_datetime(data["OrderDate"])
    data["ShipDate"] = pd.to_datetime(data["ShipDate"])
    # split the Name column into two columns
    data['FirstName'] = data.CustomerName.str.split(' ', expand = True)[0]
    data['LastName'] = data.CustomerName.str.split(' ', expand = True)[1]

    ### Insert Customers table
    df_customers = data.loc[:,['CustomerID','FirstName','LastName','Segment','Country','City','State','PostalCode','Region']]
    df_customers = df_customers.drop_duplicates(subset='CustomerID', keep="first")
    df_customers.to_sql(name='customers', con = engine, if_exists = 'append',index = False, chunksize = 1000)

    # Insert Category table
    df_category = data.loc[:,['Category','SubCategory']]
    df_category = df_category.drop_duplicates(subset=['Category', 'SubCategory'], keep="first")
    df_category = df_category.sort_values(by=['Category','SubCategory'])
    df_category['CategoryID'] = range(1, len(df_category) + 1)
    # print(df_category)
    df_category.to_sql(name='category', con = engine, if_exists = 'append',index = False, chunksize = 1000)

    # Insert Products table
    df_products = data.loc[:,['ProductID','Category','SubCategory','ProductName']]
    df_products = df_products.drop_duplicates(subset=['ProductID'], keep="first")
    df_products = df_products.merge(df_category, how = 'left', on = ['Category', 'SubCategory'])
    df_products = df_products.drop(['Category','SubCategory'], axis=1)
    # print(df_products)
    df_products.to_sql(name='products', con = engine, if_exists = 'append',index = False, chunksize = 1000)

    # Insert Orders table
    df_orders = data.loc[:,['OrderID','OrderDate','ShipDate','ShipMode','CustomerID']]
    df_orders = df_orders.drop_duplicates(subset=['OrderID'], keep="first")
    df_orders.to_sql(name='orders', con = engine, if_exists = 'append',index = False, chunksize = 1000)

    # Insert Sales table
    df_sales = data.loc[:,['OrderID','ProductID','Sales']]
    df_sales = df_sales.drop_duplicates(subset=['OrderID','ProductID'], keep="first")
    df_sales.to_sql(name='sales', con = engine, if_exists = 'append',index = False, chunksize = 1000)

    # Dislay Database Schema
    for db_pair in [ (database, config_file) ]:
        display_database(db_pair[0], db_pair[1])


def get_arguments():
    """
    Parse and validate the command line arguments
    :return: the String of database type to set up: Development or Test
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('type',
                        help='Create Development or Test database?',
                        nargs = '?',
                        type=str,
                        choices=['Development', 'Test'],
                        default='Test')
    
    parser.add_argument('load',
                        help='Load Data from CSV?',
                        nargs = '?',
                        type=str,
                        choices=['Yes', 'No'],
                        default='Yes')

    arguments = parser.parse_args()

    type = arguments.type
    load = arguments.load

    return type, load


def main():
    db_type, load_data = get_arguments()
    if db_type == 'Test':
        try:
            create_schema(config_file='superstore_test_db.ini')
            print('Successfully Created!')
        except Error as e:
            print('Query failed')
            print(e)
        
        if load_data == 'Yes':
            load_data_from_csv(database = 'superstore_test_db', config_file='superstore_test_db.ini')

    elif db_type == 'Development':
        try:
            create_schema(config_file='superstore_db.ini', filename = 'superstore_db.sql')
            print('Successfully Created!')
        except Error as e:
            print('Query failed')
            print(e)

        if load_data == 'Yes':
            load_data_from_csv(database = 'superstore_db', config_file='superstore_db.ini')


if __name__ == '__main__':
    main()