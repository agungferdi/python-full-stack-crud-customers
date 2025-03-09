import os
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "db"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "secret"),
            database=os.getenv("DB_NAME", "customer_db"),
            port=3306  
        )
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None