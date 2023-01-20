import psycopg2
from datetime import date


def connect_to_db():
    conn = psycopg2.connect(database="nutrition",
                        host="some-postgres",
                        user="postgres",
                        password="qwerty",
                        port="5432")
    return conn

def insert_into_db(data):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    sql = "INSERT INTO receipts (receipt_name, date) VALUES (%s, %s);"

    today = date.today()
    values = (data, today)
        
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()


def insert_into_table_receipts_content(data):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    sql = "INSERT INTO receipts_content (product_name, date) VALUES (%s, %s);"

    today = date.today()
    values = (data, today)
        
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()

def insert_into_products(data):
    pass

def select_from_products(data):

    conn = connect_to_db()
    cursor = conn.cursor()
    
    sql = "SELECT product_id FROM products WHERE product_name = %s;"
    
    print(data)
    cursor.execute(sql, [data.strip(),])

    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result
