import mysql.connector
from mysql.connector import Error

connection = mysql.connector.connect(host='localhost',
                                     database='exampledb',
                                     user='exampleuser',
                                     password='examplepass')
if connection.is_connected():
    db_Info = connection.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
    cursor = connection.cursor()
    
    
    table_query = "select * from exampleTable;"
    val = ("Random Title", "2021-01-01")
    cursor.execute(table_query)
    
    record = cursor.fetchall()
    print(record)
cb
def insert_into_db(connection, query, values=''):
    print('Inserting into db...')