import os
import datasus_dbc
from shell import shell as sh
import time
from math import trunc
import dbfread
import csv
import mysql.connector

def dbcMysql(file_list, host, database, password, user):
            
    try:
        if not os.path.exists('./dbc/dbf'):
            os.makedirs('./dbc/dbf')

        def getDBF(file):
                 yield from dbfread.DBF(file)

        for file in file_list:
            try:
                dbfFile = file.replace(".dbc", ".dbf")
                print('Descomprimindo ',file)
                datasus_dbc.decompress(dbc_path=file, dbf_path=dbfFile)
                command = f'mv {file.replace(".dbc", ".dbf")} ./dbc/dbf/{file.split("/")[-1].replace(".dbc", ".dbf")}'
                sh(command)
                table = file.split('/')[-1]
                if ('a.csv' in table or 'b.csv' in table or 'c.csv' in table):
                    table = table[:-6]
                else:
                    table = table[:-5]

                file = f'./dbc/dbf/{file.split("/")[-1].replace(".dbc", ".dbf")}'
                start_time = time.time()

                if not os.path.exists('./dbc/csv'):
                    os.makedirs('./dbc/csv')

                csvFile = f'./dbc/csv/{file.split("/")[-1].replace(".dbf", ".csv")}'

                csv.DictWriter(open(csvFile, "w", newline=""), fieldnames=[field.name for field in dbfread.DBF(file).fields]).writerows(getDBF(file))

                #command = f'dbf2mysql -h {host} -d {database} -t {table} -c -vv -P {password} -U {user} -q {csvFile}'

                 # Function to map DBF data types to MySQL data types
                def dbf_to_mysql_type(dbf_type):
                    if dbf_type == 'C':
                        return 'VARCHAR(255)'
                    elif dbf_type == 'N':
                        return 'INT'
                    elif dbf_type == 'F':
                        return 'FLOAT'
                    elif dbf_type == 'D':
                        return 'DATE'
                    elif dbf_type == 'T':
                        return 'DATETIME'
                    elif dbf_type == 'L':
                        return 'BOOLEAN'
                    elif dbf_type == 'M':
                        return 'TEXT'
                    else:
                        return 'VARCHAR(255)'
                
                dbf_table = dbfread.DBF('./dbc-files/dbf/' + file_list[0].split('/')[-1].replace(".dbc", ".dbf"))
                
                columns = [(field.name, dbf_to_mysql_type(field.type)) for field in dbf_table.fields]
                            
                mydb = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
                    )
                
                mycursor = mydb.cursor()
                table_name = file.split('/')[-1][:-4]

                create_table = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{col[0]} {col[1]}' for col in columns])});"
                mycursor.execute(create_table)
                mydb.commit()

                command = f"mysqlimport --ignore-lines=1 --fields-terminated-by=',' --local -u {user} -p {password} -h {host} -P 3306 {database} -v {csvFile}"

                shell = sh(command)
                print(shell.output())
                end_time = time.time()
                print(trunc(end_time - start_time), 'segundos')
            except Exception as e:
                print(e)
                print(f"Erro ao processar arquivo {file}")
                continue
    except Exception as e:
        print(e)
        return print("Erro ao descomprimir arquivos.")
        
def getDBCFiles(path):
    """
    Retrieves a list of files with the '.dbc' extension from the specified path.

    Args:
        path (str): The directory path to search for files.

    Returns:
        list: A list of file paths with the '.dbc' extension.

    Raises:
        None

    """
    files = []
    try:
        for diretorio, subpastas, arquivos in os.walk(path, topdown=True):
            for arquivo in arquivos:
                if arquivo.endswith('.dbc'):
                    files.append(os.path.join(diretorio, arquivo))  
    except:
        return print("Arquivos não encontrados.")
    finally:
        return files