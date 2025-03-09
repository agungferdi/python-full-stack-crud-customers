import os

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "db"),       
    "user": os.environ.get("DB_USER", "root"),     
    "password": os.environ.get("DB_PASSWORD", "secret"),
    "database": os.environ.get("DB_NAME", "customer_db")
}