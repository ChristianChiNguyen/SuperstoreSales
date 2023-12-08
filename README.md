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
- Username and Password and AWS url are on the .ini files, the application will call these files to connect to databases (test & development database).
- To set up databases in local host, change the superstore_db.ini file to match your username and password of localhost.
- Run the below command in directory to create schema and set up databases and transform data from train.csv to databases (Test/Development, Yes/No for loading data):
     > Python CreateDatabase.py Test Yes
  
