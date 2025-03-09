import logging
from flask import jsonify

def handle_error(e, message="Internal Server Error", status_code=500):
    logging.error(f"Error: {str(e)}")
    return jsonify({"error": message}), status_code