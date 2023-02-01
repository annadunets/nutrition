import psycopg2, re
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

    try:
        cursor.execute('SELECT LASTVAL()')
        id = cursor.fetchone()[0]
    except psycopg2.errors.ObjectNotInPrerequisiteState:
        id = None  

    cursor.close()
    conn.close()
    return id


def insert_into_receipts(receipt_name):
    
    sql = "INSERT INTO receipts (receipt_name, date) VALUES (%s, %s);"

    today = date.today()
    values = (receipt_name, today)
    
    # pass the query and the values tuple to the execute function
    id = execute_insert_query(sql, values)
    return id


def insert_into_table_receipts_content(receipt_id, product_id, quantity, unit_of_measurement):

    sql = "INSERT INTO receipts_content (receipt_id, product_id, quantity, unit_of_measurement) VALUES (%s, %s, %s, %s);"

    values = (receipt_id, product_id, quantity, unit_of_measurement)

    execute_insert_query(sql, values)


def insert_into_products(product_name, fat, carbohydrate, protein):

    sql = "INSERT INTO products (product_name, fat, carbohydrate, protein) VALUES (%s, %s, %s, %s);"

    values = (product_name, fat, carbohydrate, protein)

    id = execute_insert_query(sql, values)
    return id


def select_from_products(data):

    conn = connect_to_db()
    cursor = conn.cursor()
    
    sql = "SELECT product_id FROM products WHERE product_name = %s;"
    
    cursor.execute(sql, [data.strip(),])

    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result
