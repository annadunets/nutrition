import psycopg2
import config_local as config


def connect_to_db():
    conn = psycopg2.connect(database=config.DATABASE,
                        host=config.DB_HOST,
                        user=config.DB_USER,
                        password=config.DB_PASSWORD,
                        port=config.DB_PORT)
    return conn


def execute_query(sql, values):
    conn = connect_to_db()
    cursor = conn.cursor()
        
    cursor.execute(sql, values)
    print("The table 'products' is updated with following query:")
    print(cursor.query)
    conn.commit()

    cursor.close()
    conn.close()


def alter_products_info(product_name, energy, fat, carbohydrate, protein):
    
    sql = """UPDATE products SET energy = %s WHERE product_name = %s;
             UPDATE products SET fat = %s WHERE product_name = %s;
             UPDATE products SET carbohydrate = %s WHERE product_name = %s;
             UPDATE products SET protein = %s WHERE product_name = %s;"""
    
    values = (energy, product_name, fat, product_name, carbohydrate, product_name, protein, product_name)
    
    # pass the query and the values tuple to the execute function
    id = execute_query(sql, values)
    return id

def insert_into_receipt_processing_logs(receipt_id, message):
    
    sql = "INSERT INTO receipt_processing_logs (receipt_id, message) VALUES (%s, %s);"

    values = (receipt_id, message)

    id = execute_query(sql, values)
    return id
