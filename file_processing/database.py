import psycopg2
import config
from datetime import date


def connect_to_db():
    conn = psycopg2.connect(database=config.DATABASE,
                        host=config.DB_HOST,
                        user=config.DB_USER,
                        password=config.DB_PASSWORD,
                        port=config.DB_PORT)
    return conn


def execute_insert_query(sql, values):
    conn = connect_to_db()
    cursor = conn.cursor()
        
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()


def insert_into_receipts(receipt_name):
    
    sql = "INSERT INTO receipts (receipt_name, date) VALUES (%s, %s);"

    today = date.today()
    values = (receipt_name, today)
    
    # pass the query and the values tuple to the execute function
    execute_insert_query(sql, values)


def insert_into_table_receipts_content(data):
    
    sql = "INSERT INTO receipts_content (product_name, date) VALUES (%s, %s);"

    today = date.today()
    values = (data, today)
        
    execute_insert_query(sql, values)


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
