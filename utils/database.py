import os
import mysql.connector
from mysql.connector import Error
import logging
import time

def get_db_connection():
    retries = 10  # Increased retries
    delay = 5     # Longer delay between retries
    
    for attempt in range(retries):
        try:
            connection = mysql.connector.connect(
                host=os.getenv("DB_HOST", "db"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", "secret"),
                database=os.getenv("DB_NAME", "customer_db"),
                port=3306
            )
            if connection and connection.is_connected():
                logging.info("Database connection established successfully")
                return connection
            else:
                logging.error("Failed to establish database connection")
                if attempt < retries - 1:
                    logging.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
        except Error as e:
            logging.error(f"Database connection attempt {attempt+1} failed: {e}")
            if attempt < retries - 1:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
    
    logging.error("All database connection attempts failed")
    raise ConnectionError("Could not establish database connection after multiple attempts")