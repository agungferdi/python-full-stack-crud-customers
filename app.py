from flask import Flask, jsonify, request, render_template
from utils.database import get_db_connection
from routes import api_blueprint  
from utils.logger import setup_logger
import logging
import os

app = Flask(__name__, 
           template_folder='templates',
           static_folder='static',
           static_url_path='/static')
app.config['JSON_SORT_KEYS'] = False  
app.register_blueprint(api_blueprint, url_prefix='/api')
setup_logger()

# Add this route to serve your HTML frontend
@app.route('/')
def index():
    try:
        logging.info("Rendering index.html template")
        return render_template('index.html')
    except Exception as e:
        logging.error(f"Error rendering index.html: {str(e)}")
        return f"Error: {str(e)}", 500

# Add error handler for 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Add CORS support for API communication
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == "__main__":
    print("Starting Flask app on http://0.0.0.0:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)