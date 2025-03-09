from flask import Flask, jsonify, request
from utils.database import get_db_connection
from routes import api_blueprint  
from utils.logger import setup_logger
import logging

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False  
app.register_blueprint(api_blueprint, url_prefix='/api')
setup_logger()

if __name__ == "__main__":
    print("Starting Flask app on http://0.0.0.0:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)