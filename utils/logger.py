import logging
import mysql.connector
from mysql.connector import Error
from config.config import DB_CONFIG

def setup_logger():
    logging.basicConfig(
        filename='logs/api.log',
        level=logging.INFO,  
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

setup_logger()  

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        logging.info("Database connection successful")
        return connection
    except mysql.connector.Error as e:
        logging.error(f"Database connection error: {e}")
        return None
