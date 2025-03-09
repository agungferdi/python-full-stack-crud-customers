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
    """Helper function to create a test customer with a unique email."""
    unique_id = str(uuid.uuid4())[:8]
    customer_data = {
        "name": "Agung ferdi",
        "email": f"agungf{unique_id}@gmail1.com",  
        "phone_number": "08123456789",
        "title": "Mr",
        "gender": "M"
    }
    response = client.post('/api/customers', 
                          json=customer_data,
                          content_type='application/json')
    data = json.loads(response.data)
    return data['id']

def test_list_customers(client):
    """Test listing customers."""
    response = client.get('/api/customers')
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)

def test_add_customer(client):
    """Test adding a new customer."""
    unique_id = str(uuid.uuid4())[:8]
    customer_data = {
        "name": "fandi",
        "email": f"fandi{unique_id}@example.com",  
        "phone_number": "08123532189",
        "title": "Mr",
        "gender": "M"
    }
    response = client.post('/api/customers',
                          json=customer_data,
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == customer_data['name']
    assert data['email'] == customer_data['email']
    assert 'id' in data

def test_add_customer_missing_fields(client):
    """Test validation of required fields."""
    incomplete_data = {
        "name": "agung"
        
    }
    response = client.post('/api/customers',
                          json=incomplete_data,
                          content_type='application/json')
    assert response.status_code == 400
    assert "missing required fields" in json.loads(response.data)["error"].lower()

def test_get_customer(client):
    """Test getting a specific customer by ID."""
    
    customer_id = create_test_customer(client)
    
    response = client.get(f'/api/customers/{customer_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == customer_id
    assert 'name' in data
    assert 'email' in data
    
def test_update_customer(client):
    """Test updating a customer."""
    
    customer_id = create_test_customer(client)
    
    
    unique_id = str(uuid.uuid4())[:8]
    
    
    update_data = {
        "name": "helmy",
        "email": f"helmy1{unique_id}@example.com",  
        "phone_number": "08981254321",
        "title": "Mrs",
        "gender": "F"
    }
    response = client.put(f'/api/customers/{customer_id}',
                        json=update_data,
                        content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == update_data['name']
    assert data['email'] == update_data['email']
    
    
    response = client.get(f'/api/customers/{customer_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == update_data['name']
    assert data['email'] == update_data['email']

def test_update_customer_partial(client):
    """Test partial update of a customer."""
    
    customer_id = create_test_customer(client)
    
    
    update_data = {
        "name": "Jane Smith"
    }
    response = client.put(f'/api/customers/{customer_id}',
                        json=update_data,
                        content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == update_data['name']
    
    
    response = client.get(f'/api/customers/{customer_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == update_data['name']
    assert 'email' in data  

def test_delete_customer(client):
    """Test deleting a customer."""
    
    customer_id = create_test_customer(client)
    
    response = client.delete(f'/api/customers/{customer_id}')
    assert response.status_code == 200
    message = json.loads(response.data)
    assert "deleted" in message["message"].lower()
    
    
    response = client.get(f'/api/customers/{customer_id}')
    assert response.status_code == 404

def test_customer_not_found(client):
    """Test getting a non-existent customer."""
    response = client.get('/api/customers/99999')
    assert response.status_code == 404
    assert "not found" in json.loads(response.data)["error"].lower()

def test_update_nonexistent_customer(client):
    """Test updating a non-existent customer."""
    update_data = {
        "name": "Jane Smith"
    }
    response = client.put('/api/customers/99999',
                        json=update_data,
                        content_type='application/json')
    assert response.status_code == 404
    assert "not found" in json.loads(response.data)["error"].lower()

def test_delete_nonexistent_customer(client):
    """Test deleting a non-existent customer."""
    response = client.delete('/api/customers/99999')
    assert response.status_code == 404
    assert "not found" in json.loads(response.data)["error"].lower()

def test_duplicate_email(client):
    """Test that we can't add two customers with the same email."""
    
    unique_id = str(uuid.uuid4())[:8]
    email = f"duplicate{unique_id}@example.com"
    
    customer_data = {
        "name": "John Doe",
        "email": email,
        "phone_number": "08123456789",
        "title": "Mr",
        "gender": "M"
    }
    
    
    response = client.post('/api/customers',
                          json=customer_data,
                          content_type='application/json')
    assert response.status_code == 201
    
    
    customer_data["name"] = "Different Name"
    response = client.post('/api/customers',
                          json=customer_data,
                          content_type='application/json')
    assert response.status_code == 400
    assert "email already exists" in json.loads(response.data)["error"].lower() or "duplicate" in json.loads(response.data)["error"].lower()