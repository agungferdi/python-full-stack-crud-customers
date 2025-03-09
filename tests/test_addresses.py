import pytest
import json
import os
import sys
import uuid  


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from app import app

@pytest.fixture
def client():
    """Test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def create_test_customer(client):
    """Helper function to create a test customer."""
    
    unique_id = str(uuid.uuid4())[:8]
    customer_data = {
        "name": "Agung Ferdiansyah",
        "email": f"agung{unique_id}@gmail.com",
        "phone_number": "08123456789",
        "title": "Mr",
        "gender": "M"
    }
    response = client.post('/api/customers', 
                         json=customer_data,
                         content_type='application/json')
    data = json.loads(response.data)
    
    
    if not data.get('id'):
        print("ID missing in response, searching by email...")
        get_response = client.get('/api/customers')
        customers = json.loads(get_response.data)
        for customer in customers:
            if customer['email'] == customer_data['email']:
                print(f"Found customer with id: {customer['id']}")
                return customer['id']
        
        return 1
    
    print(f"Created test customer with ID: {data.get('id')}")
    return data.get('id')
@pytest.fixture
def test_address(client):
    """Fixture that creates a customer with an address for testing."""
    # Create a customer first
    customer_id = create_test_customer(client)
    print(f"Using customer ID: {customer_id}")
    
    # Create an address for that customer
    address_data = {
        "customer_id": customer_id,  
        "address": "condong street",
        "district": "gading",
        "city": "probolinggo",
        "province": "jawa timur",
        "postal_code": "12345"
    }
    response = client.post('/api/addresses', 
                         json=address_data,
                         content_type='application/json')
    data = json.loads(response.data)
    address_id = data.get('id')
    print(f"Created test address with ID: {address_id}")
    
    return {
        'customer_id': customer_id,
        'address_id': address_id,
        'address_data': address_data
    }

def test_add_address(client):
    """Test adding a new address for a customer."""
    
    customer_id = create_test_customer(client)
    
    
    address_data = {
        "customer_id": customer_id,
        "address": "desa bermi",
        "district": "krucil",
        "city": "kraksaan",
        "province": "jawa barat",
        "postal_code": "3213"
    }
    response = client.post('/api/addresses',
                         json=address_data,
                         content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "id" in data
    assert data["address"] == address_data["address"]
    assert data["city"] == address_data["city"]
    assert data["customer_id"] == customer_id

def test_get_address(client, test_address):
    """Test retrieving a specific address."""
    address_id = test_address['address_id']
    
    response = client.get(f'/api/addresses/{address_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == address_id
    assert data["address"] == test_address["address_data"]["address"]
    assert data["city"] == test_address["address_data"]["city"]

def test_get_addresses_for_customer(client, test_address):
    """Test retrieving addresses for a customer."""
    customer_id = test_address['customer_id']
    
    response = client.get(f'/api/customers/{customer_id}/addresses')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    assert "address" in data[0]
    assert "city" in data[0]
    assert data[0]["customer_id"] == customer_id

def test_update_address(client, test_address):
    """Test updating an address."""
    address_id = test_address['address_id']
    
    
    updated_data = {
        "address": "jalan patimura 2",
        "district": "pakuniran",
        "city": "bekasi",
        "province": "jawa barat",
        "postal_code": "98023"
    }
    response = client.put(f'/api/addresses/{address_id}',
                        json=updated_data,
                        content_type='application/json')
    assert response.status_code == 200
    
    
    data = json.loads(response.data)
    assert data["address"] == updated_data["address"]
    assert data["district"] == updated_data["district"]
    
    
    response = client.get(f'/api/addresses/{address_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["address"] == updated_data["address"]
    assert data["district"] == updated_data["district"]

def test_delete_address(client, test_address):
    """Test deleting an address."""
    address_id = test_address['address_id']
    
    
    response = client.delete(f'/api/addresses/{address_id}')
    assert response.status_code == 200
    assert json.loads(response.data) == {"message": "Address deleted"}
    
    
    response = client.get(f'/api/addresses/{address_id}')
    assert response.status_code == 404
    assert "not found" in json.loads(response.data)["error"].lower()

def test_address_not_found(client):
    """Test accessing a non-existent address."""
    
    response = client.get('/api/addresses/99999')
    assert response.status_code == 404
    assert "not found" in json.loads(response.data)["error"].lower()

def test_missing_required_fields(client):
    """Test validation of required fields."""
    
    customer_id = create_test_customer(client)
    
    
    incomplete_data = {
        "customer_id": customer_id,
        "address": "jalan condong"
        
    }
    
    response = client.post('/api/addresses',
                         json=incomplete_data,
                         content_type='application/json')
    assert response.status_code == 400
    assert "missing required fields" in json.loads(response.data)["error"].lower()