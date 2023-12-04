from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser
from sqlite3 import OperationalError
import csv
from pandas import DataFrame
from IPython.display import display

def read_config(config_file = 'superstore_db.ini', section = 'mysql', list_remove_from_config = []):
    parser = ConfigParser()
    parser.read(config_file)
    
    config = {}
    
    if parser.has_section(section):
        # Parse the configuration file.
        items = parser.items(section)
        
        # Construct the parameter dictionary.
        for item in items:
            config[item[0]] = item[1]
            
    else:
        raise Exception(f'Section [{section}] missing ' + \
                        f'in config file {config_file}')
    
    for remove in list_remove_from_config:
            config.pop(remove, None)
    return config
        
def make_connection(config_file = 'superstore_db.ini', section = 'mysql', list_remove_from_config = []):
    try:
        db_config = read_config(config_file, section, list_remove_from_config)
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            return conn

    except Error as e:
        print('Connection failed.')
        print(e)
        
        return None

def do_query_multi(sql):
    cursor = None
    
    # Connect to the database.
    conn = make_connection()
        
    if conn != None:
        try:
            cursor = conn.cursor()
            results = cursor.execute(sql, multi=True)
            
        except Error as e:
            print('Query failed')
            print(e)
            
            return [(), 0]

    # Return the fetched data as a list of tuples,
    # one tuple per table row.
    if conn != None:
        for result in cursor.execute(sql, multi=True):
            print(result)
        rows = cursor.fetchall()
        count = cursor.rowcount
            
        conn.close()
        return [rows, count]
    else:
        return [(), 0]
    
def do_query(sql):
    cursor = None
    
    # Connect to the database.
    conn = make_connection(config_file = 'superstore_db.ini', section = 'mysql', list_remove_from_config = ['drivername','username'])
        
    if conn != None:
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
        except Error as e:
            print('Query failed')
            print(e)
            
            return [(), 0]

    # Return the fetched data as a list of tuples,
    # one tuple per table row.
    if conn != None:
        rows = cursor.fetchall()
        count = cursor.rowcount
            
        conn.close()
        return [rows, count]
    else:
        return [(), 0]


def insert_query(tablename, values):
    cursor = None
    # Connect to the database.
    conn = make_connection(config_file = 'superstore_db.ini', section = 'mysql', list_remove_from_config = ['drivername','username'])
    # Prepare sql statement
    sql = ( "INSERT INTO " + tablename + " VALUES (" + "%s,"*(len(values)-1) + "%s)" )

    if conn != None:
        try:
            cursor = conn.cursor()
            # Execute insert statement with tuple values
            cursor.execute(sql, values)
            conn.commit()
            
        except Error as e:
            print('Query failed')
            print(e)
            conn.rollback()
            cursor.close()


def set_data_to_table_cells(ui_table, rows, money_index):
    """ Function to set data from list of tuples
    to ui_table cells, and change the column index
    in money_index to money value
    """
    from PyQt5.QtWidgets import QTableWidgetItem
    row_index = 0
    for row in rows:
        # print(row)
        column_index = 0
        i = 0
        for data in row:
            string_item = str(data)
            if money_index:
                if i in money_index:
                    string_item = "${:,.2f}".format(data)
            item = QTableWidgetItem(string_item)
            ui_table.setItem(row_index, column_index, item)
            column_index += 1
            i += 1

        row_index += 1

def adjust_column_widths(ui_table):
    """ Function to resize all the columns
    in the ui_table, the last column will
    be stretched
    """
    from PyQt5.QtWidgets import QHeaderView
    columns_count = ui_table.columnCount()
    header = ui_table.horizontalHeader()
    i = 0
    while i < columns_count:
        if i < columns_count - 1:
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        else:
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        i += 1

def executeScriptsFromFile(conn, filename):
    """
    filename = "superstore_db_schema.sql"
    """
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    check = 0

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    if conn != None:
        try:
            cursor = conn.cursor()
            for command in sqlCommands:
                if command != '\n':
                    try:
                        cursor.execute(command)
                        check = 1
                    except OperationalError:
                        print("Command skipped: ")

            cursor.close()
        except Error as e:
            print('Query failed')
            print(e)
    
    return check

def insert_csv(sql_insert, filename, config_file='superstore_db.ini'):
    conn = make_connection(config_file)
    cursor = conn.cursor()
    first = True
    check = 0
    with open(filename, newline='') as csv_file:
        data = csv.reader(csv_file, delimiter=',', quotechar='"')
        for row in data:
            if not first:
                try:
                    cursor.execute(sql_insert, row)
                    check = 1
                except Error:
                    print("ERROR: could be end of file")
            first = False
        conn.commit()
    
    cursor.close()
    return check

def output_dataframe_to_DB(df, table_name, conn):
    try:
        cursor = conn.cursor()
        # creating column list for insertion
        cols = ",".join([str(i) for i in df.columns.tolist()])
        # Insert DataFrame recrds one by one.
        for i,row in df.iterrows():
            sql = "INSERT INTO " + table_name + " (" +cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
            cursor.execute(sql, tuple(row))
            # the connection is not autocommitted by default, so we must commit to save our changes
            conn.commit()
    except Exception as e:
        conn.rollback()
        cursor.close()

def display_table(table, cursor):
    """
    Use the cursor to return the contents of the database table
    in a dataframe.
    """
    sql = f"SELECT * FROM {table}"
    cursor.execute(sql)
    
    # Get the names of the columns.
    columns = cursor.description
    column_names = [column_info[0] for column_info in columns]

    # Fetch and return the contents in a dataframe.
    df = DataFrame(cursor.fetchall())
    df.columns = column_names
    return df

def display_database(database_name, config_file):
    """
    Use the configuration file to display the tables
    of the database named database_name.
    """
    conn = make_connection(config_file=config_file,list_remove_from_config = ['drivername', 'username'])
    cursor = conn.cursor()
    
    print('-'*(len('DATABASE ' + database_name)))
    print(f'DATABASE {database_name}')
    print('-'*(len('DATABASE ' + database_name)))
    
    # Get the names of the database tables.
    cursor.execute('SHOW TABLES');
    results = cursor.fetchall()
    tables = [result[0] for result in results]
    
    # Display the contents of each table in a dataframe.
    for table in tables:
        print()
        print(table)
        
        df = display_table(table, cursor)
        display(df.head(20))
        
    cursor.close()
    conn.close()
