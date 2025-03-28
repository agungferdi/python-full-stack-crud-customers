from .error_handler import handle_error
from flask import jsonify, request
from utils.database import get_db_connection
from models.customer import Customer
import mysql.connector

def register_customer_routes(api_blueprint):
    
    @api_blueprint.route('/customers', methods=['GET'])
    def list_customers():
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM customers")
            
            customers = [Customer.from_dict(row).to_dict() for row in cursor.fetchall()]
            return jsonify(customers), 200
            
        except Exception as e:
            return handle_error(e)

    
    @api_blueprint.route('/customers', methods=['POST'])
    def add_customer():
        try:
            data = request.get_json()
            
            required_fields = ['name', 'email', 'phone_number']
            if not all(key in data for key in required_fields):
                return jsonify({"error": f"Missing required fields: {required_fields}"}), 400
                
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO customers 
                (title, name, gender, phone_number, image, email)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                data.get('title', 'Mr'),
                data['name'],
                data.get('gender', 'M'),
                data['phone_number'],
                data.get('image'),
                data['email']
            ))
            conn.commit()
            
            
            customer_id = cursor.lastrowid
            
            
            customer = Customer.from_dict({
                'id': customer_id,
                'title': data.get('title', 'Mr'),
                'name': data['name'],
                'gender': data.get('gender', 'M'),
                'phone_number': data['phone_number'],
                'image': data.get('image'),
                'email': data['email']
            })
            
            return jsonify(customer.to_dict()), 201
            
        except mysql.connector.IntegrityError as e:
            return handle_error(e, "Email already exists", 400)
        except Exception as e:
            return handle_error(e)

    
    @api_blueprint.route('/customers/<int:customer_id>', methods=['GET'])
    def get_customer(customer_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
            
            customer = cursor.fetchone()
            if not customer:
                return jsonify({"error": "Customer not found"}), 404
                
            
            cursor.execute("SELECT * FROM addresses WHERE customer_id = %s", (customer_id,))
            addresses = cursor.fetchall()
            
            result = Customer.from_dict(customer).to_dict()
            
            
            if addresses:
                result['addresses'] = addresses
            
            return jsonify(result), 200
            
        except Exception as e:
            return handle_error(e)
    
    @api_blueprint.route('/customers/<int:customer_id>', methods=['PUT'])
    def update_customer(customer_id):
        try:
            data = request.get_json()
            
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
            customer = cursor.fetchone()
            
            if not customer:
                return jsonify({"error": "Customer not found"}), 404
                
            update_fields = []
            update_values = []
            
            if 'title' in data:
                update_fields.append("title = %s")
                update_values.append(data['title'])
            
            if 'name' in data:
                update_fields.append("name = %s")
                update_values.append(data['name'])
                
            if 'gender' in data:
                update_fields.append("gender = %s")
                update_values.append(data['gender'])
            
            if 'phone_number' in data:
                update_fields.append("phone_number = %s")
                update_values.append(data['phone_number'])
            
            if 'image' in data:
                update_fields.append("image = %s")
                update_values.append(data['image'])
                
            if 'email' in data:
                update_fields.append("email = %s")
                update_values.append(data['email'])
                
            if not update_fields:
                return jsonify({"error": "No fields to update"}), 400
                
            query = "UPDATE customers SET " + ", ".join(update_fields) + " WHERE id = %s"
            update_values.append(customer_id)
            
            cursor.execute(query, update_values)
            conn.commit()
            
            cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
            updated = cursor.fetchone()
            
            return jsonify(Customer.from_dict(updated).to_dict()), 200
            
        except mysql.connector.IntegrityError as e:
            return handle_error(e, "Email already exists", 400)
        except Exception as e:
            return handle_error(e)
    
    @api_blueprint.route('/customers/<int:customer_id>', methods=['DELETE'])
    def delete_customer(customer_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            
            cursor.execute("DELETE FROM addresses WHERE customer_id = %s", (customer_id,))
            
            
            cursor.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
            
            if cursor.rowcount == 0:
                return jsonify({"error": "Customer not found"}), 404
                
            conn.commit()
            return jsonify({"message": "Customer deleted"}), 200
            
        except Exception as e:
            conn.rollback()
            return handle_error(e)