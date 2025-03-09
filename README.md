# Customer API - RESTful Backend Service

A comprehensive RESTful API service for customer and address management, featuring full CRUD operations, data validation, and extensive test coverage.

## Features

- **Customer Management**: Create, read, update, and delete customer records
- **Address Management**: Associate multiple addresses with each customer
- **Image Support**: Upload and retrieve customer profile images
- **Data Validation**: Prevent duplicate emails and enforce required fields
- **RESTful Design**: Following REST principles with appropriate HTTP verbs and status codes
- **Comprehensive Test Suite**: Automated tests for all API endpoints

## Tech Stack

- **Flask**: Lightweight web framework for API development
- **MySQL**: Relational database for data storage
- **Docker**: Containerization for consistent development and deployment
- **Docker Compose**: Multi-container Docker applications
- **Pytest**: Testing framework for automated tests

## API Endpoints

### Customer Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/customers` | List all customers |
| POST | `/api/customers` | Create a new customer |
| GET | `/api/customers/{id}` | Get customer details by ID |
| PUT | `/api/customers/{id}` | Update customer details |
| DELETE | `/api/customers/{id}` | Delete a customer |

### Address Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/customers/{customer_id}/addresses` | List customer's addresses |
| POST | `/api/addresses` | Add a new address |
| GET | `/api/addresses/{id}` | Get address details by ID |
| PUT | `/api/addresses/{id}` | Update address details |
| DELETE | `/api/addresses/{id}` | Delete an address |

## Data Models

### Customer

```json
{
  "id": 1,
  "title": "Mr",
  "name": "Agung Ferdiansyah",
  "gender": "M",
  "phone_number": "08123456789",
  "image": "profile.jpg",
  "email": "agung@example.com",
  "created_at": "2025-03-09 12:00:00",
  "updated_at": "2025-03-09 12:00:00",
  "addresses": []
}
```

### Address

```json
{
  "id": 1,
  "customer_id": 1,
  "address": "condong street",
  "district": "gading",
  "city": "probolinggo",
  "province": "jawa timur",
  "postal_code": "12345",
  "created_at": "2025-03-09 12:00:00",
  "updated_at": "2025-03-09 12:00:00"
}
```

## Setup and Installation

### Prerequisites

- Docker and Docker Compose
- Git

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/customer_api.git
   cd customer_api
   ```

2. Start the Docker containers:
   ```bash
   docker-compose up -d
   ```

3. The API will be available at `http://localhost:5000/api`

### Running Tests

```bash
# Run all tests
docker exec -it customer_api-web-1 bash -c "cd /app && python -m pytest -v"

# Run customer tests only
docker exec -it customer_api-web-1 bash -c "cd /app && python -m pytest tests/test_customers.py -v"

# Run address tests only
docker exec -it customer_api-web-1 bash -c "cd /app && python -m pytest tests/test_addresses.py -v"
```

After running tests, sample data will be available in the database that you can interact with via the API.

## Project Structure

```
customer_api/
├── app.py                  # Main application entry point
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker build instructions
├── models/                 # Data models
│   ├── customer.py
│   └── address.py
├── routes/                 # API route handlers
│   ├── customer_routes.py
│   └── address_routes.py
├── tests/                  # Test suites
│   ├── test_customers.py
│   └── test_addresses.py
├── utils/                  # Utility functions
│   └── database.py
└── migrations/             # Database schema migrations
    └── init_db.sql
```

## API Usage Examples with Postman

### 1. Create a New Customer

![Create Customer](https://example.com/images/create_customer.png)

**Request:**
- Method: `POST`
- URL: `http://localhost:5000/api/customers`
- Headers: `Content-Type: application/json`
- Body:
```json
{
  "name": "Agung Ferdiansyah",
  "email": "agung@example.com",
  "phone_number": "08123456789",
  "title": "Mr",
  "gender": "M",
  "image": "http://example.com/profile.jpg"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Mr",
  "name": "Agung Ferdiansyah",
  "gender": "M",
  "phone_number": "08123456789",
  "image": "http://example.com/profile.jpg",
  "email": "agung@example.com",
  "created_at": "2025-03-09 12:30:45",
  "updated_at": "2025-03-09 12:30:45"
}
```

### 2. List All Customers

![List Customers](https://example.com/images/list_customers.png)

**Request:**
- Method: `GET`
- URL: `http://localhost:5000/api/customers`

**Response:**
```json
[
  {
    "id": 1,
    "title": "Mr",
    "name": "Agung Ferdiansyah",
    "gender": "M",
    "phone_number": "08123456789",
    "image": "http://example.com/profile.jpg",
    "email": "agung@example.com",
    "created_at": "2025-03-09 12:30:45",
    "updated_at": "2025-03-09 12:30:45"
  },
  {
    "id": 2,
    "title": "Mrs",
    "name": "Jane Smith",
    "gender": "F",
    "phone_number": "08987654321",
    "image": null,
    "email": "jane@example.com",
    "created_at": "2025-03-09 12:40:22",
    "updated_at": "2025-03-09 12:40:22"
  }
]
```

### 3. Add an Address to a Customer

![Add Address](https://example.com/images/add_address.png)

**Request:**
- Method: `POST`
- URL: `http://localhost:5000/api/addresses`
- Headers: `Content-Type: application/json`
- Body:
```json
{
  "customer_id": 1,
  "address": "condong street",
  "district": "gading",
  "city": "probolinggo",
  "province": "jawa timur",
  "postal_code": "12345"
}
```

**Response:**
```json
{
  "id": 1,
  "customer_id": 1,
  "address": "condong street",
  "district": "gading",
  "city": "probolinggo",
  "province": "jawa timur",
  "postal_code": "12345",
  "created_at": "2025-03-09 12:35:22",
  "updated_at": "2025-03-09 12:35:22"
}
```

### 4. Get Customer with Addresses

![Get Customer with Addresses](https://example.com/images/get_customer_with_addresses.png)

**Request:**
- Method: `GET`
- URL: `http://localhost:5000/api/customers/1`

**Response:**
```json
{
  "id": 1,
  "title": "Mr",
  "name": "Agung Ferdiansyah",
  "gender": "M",
  "phone_number": "08123456789",
  "image": "http://example.com/profile.jpg",
  "email": "agung@example.com",
  "created_at": "2025-03-09 12:30:45",
  "updated_at": "2025-03-09 12:30:45",
  "addresses": [
    {
      "id": 1,
      "customer_id": 1,
      "address": "condong street",
      "district": "gading",
      "city": "probolinggo",
      "province": "jawa timur",
      "postal_code": "12345",
      "created_at": "2025-03-09 12:35:22",
      "updated_at": "2025-03-09 12:35:22"
    }
  ]
}
```

### 5. Update a Customer

![Update Customer](https://example.com/images/update_customer.png)

**Request:**
- Method: `PUT`
- URL: `http://localhost:5000/api/customers/1`
- Headers: `Content-Type: application/json`
- Body:
```json
{
  "name": "Agung F. Muhammad",
  "image": "http://example.com/new_profile.jpg"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Mr",
  "name": "Agung F. Muhammad",
  "gender": "M",
  "phone_number": "08123456789",
  "image": "http://example.com/new_profile.jpg",
  "email": "agung@example.com",
  "created_at": "2025-03-09 12:30:45",
  "updated_at": "2025-03-09 12:50:15"
}
```

## Working with Test Data

After running the test suite, several customer and address records will be created in the database. Here's how to work with this data:

1. **View Test Data**: Use GET requests to list all customers and their addresses
   ```
   GET http://localhost:5000/api/customers
   ```

2. **Edit Existing Test Data**: Use the IDs from the test data to update records
   ```
   PUT http://localhost:5000/api/customers/{id}
   ```

3. **Add More Data**: Create additional customers and addresses as needed
   ```
   POST http://localhost:5000/api/customers
   POST http://localhost:5000/api/addresses
   ```

4. **Reset All Data**: To clear all test data and start fresh
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```

## Custom Image Support

The API supports custom images for customers via image URLs. To add or update a customer's image:

1. **When creating a customer**:
   ```json
   {
     "name": "Agung Ferdiansyah",
     "email": "agung@example.com",
     "phone_number": "08123456789",
     "title": "Mr",
     "gender": "M",
     "image": "https://example.com/profile.jpg"
   }
   ```

2. **When updating a customer**:
   ```json
   {
     "image": "https://example.com/new_profile.jpg"
   }
   ```

The image URL will be stored in the database and returned in customer responses.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Developed for the Technical Backend Engineering Test by Agung Ferdiansyah.