from functions import dbcMysql, getDBCFiles
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
        
    user = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')
    host = os.getenv('MYSQL_HOST')
    #port = os.getenv('MYSQL_PORT')
    database = os.getenv('MYSQL_DATABASE')

    dbcFiles = getDBCFiles('./dbc')

    if len(dbcFiles) > 0:
        dbcMysql(dbcFiles, host, database, password, user)

if __name__ == '__main__':
    main()
        