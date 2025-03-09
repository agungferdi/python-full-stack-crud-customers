from .error_handler import handle_error
from flask import jsonify, request
from utils.database import get_db_connection
from models.address import Address
import mysql.connector

def register_address_routes(api_blueprint):
    
    @api_blueprint.route('/addresses', methods=['POST'])
    def add_address():
        try:
            data = request.get_json()
            required_fields = ['customer_id', 'address', 'district', 'city', 'province', 'postal_code']
            
            if not all(key in data for key in required_fields):
                return jsonify({"error": f"Missing required fields: {required_fields}"}), 400
                
            address = Address.from_dict(data)
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO addresses 
                (customer_id, address, district, city, province, postal_code)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                address.customer_id,
                address.address,
                address.district,
                address.city,
                address.province,
                address.postal_code
            ))
            conn.commit()
            
            
            address_id = cursor.lastrowid
            
            
            address.id = address_id
            
            return jsonify(address.to_dict()), 201
            
        except mysql.connector.IntegrityError as e:
            conn.rollback()
            return handle_error(e, "Invalid customer ID", 400)
        except Exception as e:
            conn.rollback()
            return handle_error(e)

    @api_blueprint.route('/addresses/<int:address_id>', methods=['GET'])
    def get_address(address_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM addresses WHERE id = %s", (address_id,))
            
            address = cursor.fetchone()
            if not address:
                return jsonify({"error": "Address not found"}), 404
                
            return jsonify(Address.from_dict(address).to_dict()), 200
            
        except Exception as e:
            return handle_error(e)
    
    @api_blueprint.route('/addresses/<int:address_id>', methods=['PUT'])
    def update_address(address_id):
        try:
            data = request.get_json()
            
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            
            cursor.execute("SELECT * FROM addresses WHERE id = %s", (address_id,))
            current_address = cursor.fetchone()
            
            if not current_address:
                return jsonify({"error": "Address not found"}), 404
            
            
            update_fields = []
            values = []
            
            if 'address' in data:
                update_fields.append("address = %s")
                values.append(data['address'])
                
            if 'district' in data:
                update_fields.append("district = %s")
                values.append(data['district'])
                
            if 'city' in data:
                update_fields.append("city = %s")
                values.append(data['city'])
                
            if 'province' in data:
                update_fields.append("province = %s")
                values.append(data['province'])
                
            if 'postal_code' in data:
                update_fields.append("postal_code = %s")
                values.append(data['postal_code'])
            
            if not update_fields:
                return jsonify({"error": "No fields to update"}), 400
                
            
            values.append(address_id)
            
            
            query = "UPDATE addresses SET " + ", ".join(update_fields) + " WHERE id = %s"
            cursor.execute(query, values)
            
            conn.commit()
            
            
            cursor.execute("SELECT * FROM addresses WHERE id = %s", (address_id,))
            updated_address = cursor.fetchone()
            
            return jsonify(Address.from_dict(updated_address).to_dict()), 200
            
        except Exception as e:
            conn.rollback()
            return handle_error(e)

    @api_blueprint.route('/addresses/<int:address_id>', methods=['DELETE'])
    def delete_address(address_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM addresses WHERE id = %s", (address_id,))
            
            if cursor.rowcount == 0:
                return jsonify({"error": "Address not found"}), 404
            
            conn.commit()
            return jsonify({"message": "Address deleted"}), 200
            
        except Exception as e:
            conn.rollback()
            return handle_error(e)
    
    @api_blueprint.route('/customers/<int:customer_id>/addresses', methods=['GET'])
    def list_addresses(customer_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM addresses WHERE customer_id = %s", (customer_id,))
            
            addresses = [Address.from_dict(row).to_dict() for row in cursor.fetchall()]
            return jsonify(addresses), 200
            
        except Exception as e:
            return handle_error(e)