import os

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),  # Changed from "db" to "localhost"    
    "user": os.environ.get("DB_USER", "root"),     
    "password": os.environ.get("DB_PASSWORD", ""),  # Empty password is correct
    "database": os.environ.get("DB_NAME", "customer_db")
}