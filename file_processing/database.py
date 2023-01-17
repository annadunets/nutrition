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
    
    
    #cursor.execute("CREATE TABLE IF NOT EXISTS files ( id SERIAL PRIMARY KEY, filename varchar(45) NOT NULL, date varchar(20));")
    sql = "INSERT INTO files (filename, date) VALUES (%s, %s);"

    today = date.today()
    values = (data, today)
        
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()