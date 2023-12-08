# SuperstoreSales
Application to store sales data
The executable file is in the main directory as AppMain.exe

Install Softwares:
- Anaconda --> VS Code --> Python 3.9.12
- Install PYQT5:
    > pip3 install PyQt5
    > pip3 install pyqt5-tools
- Install mysql:
    > pip3 install mysql-connector-python-rf

Setup Database:
- Username and Password and AWS url are on the .ini files, the application will call these files to connect to databases (test & development database)
- Create a schema in your local host with schema name "superstore_db"
- Change the superstore_db.ini file to match your username and password of localhost
- Run CSV-insert.jpynb to insert data from spreadsheet to database
