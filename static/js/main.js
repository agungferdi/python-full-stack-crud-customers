const API_URL = 'http://localhost:8000/api';
let customerDetailsModal;
let addressModal;
let currentCustomerId;

document.addEventListener('DOMContentLoaded', function() {
    fetchCustomers();
    setupEventListeners();
    customerDetailsModal = new bootstrap.Modal(document.getElementById('customerDetailsModal'));
    addressModal = new bootstrap.Modal(document.getElementById('addressModal'));
});

function setupEventListeners() {
    document.getElementById('customerForm').addEventListener('submit', handleFormSubmit);
    document.getElementById('cancelBtn').addEventListener('click', function() {
        document.getElementById('formSection').style.display = 'none';
    });
    document.getElementById('addAddressBtn').addEventListener('click', showAddressModal);
    document.getElementById('saveAddressBtn').addEventListener('click', saveAddress);
    document.querySelector('header button').addEventListener('click', showAddForm);
}

function showAddForm() {
    const formSection = document.getElementById('formSection');
    formSection.style.display = 'block';
    
    // Reset form without hiding it
    document.getElementById('customerForm').reset();
    document.getElementById('customerId').value = '';
    document.getElementById('formTitle').textContent = 'Add New Customer';
    document.getElementById('submitBtn').innerHTML = '<i class="bi bi-save me-2"></i>Add Customer';
    document.getElementById('cancelBtn').classList.remove('d-none');
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function fetchCustomers() {
    try {
        const response = await fetch(`${API_URL}/customers`);
        if (!response.ok) throw new Error('Failed to fetch customers');
        const customers = await response.json();
        displayCustomers(customers);
    } catch (error) {
        console.error('Error fetching customers:', error);
        showAlert(`Error loading customers: ${error.message}`, 'danger');
    }
}

function displayCustomers(customers) {
    const listContainer = document.getElementById('customersList');
    listContainer.innerHTML = '';
    
    if (customers.length === 0) {
        listContainer.innerHTML = '<div class="col-12 text-center py-4">No customers found.</div>';
        return;
    }
    
    customers.forEach(customer => {
        const card = document.createElement('div');
        card.className = 'col-md-4 mb-4';
        card.innerHTML = `
            <div class="card customer-card h-100">
                <img src="${customer.image || 'https://via.placeholder.com/300'}" 
                     class="card-img-top" alt="${customer.name}">
                <div class="card-body">
                    <h5 class="card-title">${customer.title} ${customer.name}</h5>
                    <p class="card-text text-muted mb-1">
                        <i class="bi bi-envelope me-1"></i>${customer.email}
                    </p>
                    <p class="card-text text-muted">
                        <i class="bi bi-phone me-1"></i>${customer.phone_number}
                    </p>
                    <div class="d-flex gap-2 justify-content-end">
                        <button class="btn btn-sm btn-outline-primary view-btn" 
                            data-id="${customer.id}">View</button>
                        <button class="btn btn-sm btn-outline-success edit-btn" 
                            data-id="${customer.id}">Edit</button>
                        <button class="btn btn-sm btn-outline-danger delete-btn" 
                            data-id="${customer.id}">Delete</button>
                    </div>
                </div>
            </div>
        `;
        listContainer.appendChild(card);
        
        card.querySelector('.view-btn').addEventListener('click', () => viewCustomer(customer.id));
        card.querySelector('.edit-btn').addEventListener('click', () => editCustomer(customer.id));
        card.querySelector('.delete-btn').addEventListener('click', () => deleteCustomer(customer.id));
    });
}

async function viewCustomer(id) {
    try {
        currentCustomerId = id;
        const response = await fetch(`${API_URL}/customers/${id}`);
        if (!response.ok) throw new Error('Failed to fetch customer details');
        const customer = await response.json();
        
        const modalBody = document.getElementById('customerDetailsBody');
        let addressesHtml = '';
        
        if (customer.addresses && customer.addresses.length > 0) {
            addressesHtml = `
                <h6 class="mt-4">Addresses</h6>
                <ul class="list-group">
                    ${customer.addresses.map(addr => `
                        <li class="list-group-item">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <p class="mb-1">${addr.address}</p>
                                    <small class="text-muted">
                                        ${addr.district}, ${addr.city}<br>
                                        ${addr.province} ${addr.postal_code}
                                    </small>
                                </div>
                                <div class="btn-group">
                                    <button class="btn btn-sm btn-outline-secondary edit-address-btn" 
                                        data-id="${addr.id}">
                                        <i class="bi bi-pencil"></i>
                                    </button>
                                    <button class="btn btn-sm btn-outline-danger delete-address-btn" 
                                        data-id="${addr.id}">
                                        <i class="bi bi-trash"></i>
                                    </button>
                                </div>
                            </div>
                        </li>
                    `).join('')}
                </ul>
            `;
        } else {
            addressesHtml = '<div class="alert alert-info mt-3">No addresses found</div>';
        }
        
        modalBody.innerHTML = `
            <div class="row">
                <div class="col-md-4 text-center">
                    <img src="${customer.image || 'https://via.placeholder.com/300'}" 
                         class="img-fluid rounded mb-3" alt="${customer.name}">
                    <h4>${customer.title} ${customer.name}</h4>
                </div>
                <div class="col-md-8">
                    <div class="mb-3">
                        <p class="mb-1"><i class="bi bi-gender-ambiguous me-2"></i>${customer.gender === 'M' ? 'Male' : 'Female'}</p>
                        <p class="mb-1"><i class="bi bi-envelope me-2"></i>${customer.email}</p>
                        <p><i class="bi bi-phone me-2"></i>${customer.phone_number}</p>
                    </div>
                    ${addressesHtml}
                </div>
            </div>
        `;
        
        // Add address button listeners
        document.querySelectorAll('.edit-address-btn').forEach(btn => {
            btn.addEventListener('click', () => editAddress(btn.dataset.id));
        });
        document.querySelectorAll('.delete-address-btn').forEach(btn => {
            btn.addEventListener('click', () => deleteAddress(btn.dataset.id));
        });
        
        customerDetailsModal.show();
    } catch (error) {
        console.error('Error fetching customer details:', error);
        showAlert('Failed to load customer details', 'danger');
    }
}

async function editCustomer(id) {
    try {
        const response = await fetch(`${API_URL}/customers/${id}`);
        if (!response.ok) throw new Error('Failed to fetch customer');
        const customer = await response.json();
        
        document.getElementById('customerId').value = customer.id;
        document.getElementById('title').value = customer.title;
        document.getElementById('name').value = customer.name;
        document.getElementById('gender').value = customer.gender;
        document.getElementById('phoneNumber').value = customer.phone_number;
        document.getElementById('email').value = customer.email;
        document.getElementById('image').value = customer.image || '';
        
        document.getElementById('formTitle').textContent = 'Edit Customer';
        document.getElementById('submitBtn').innerHTML = '<i class="bi bi-save me-2"></i>Update Customer';
        document.getElementById('cancelBtn').classList.remove('d-none');
        document.getElementById('formSection').style.display = 'block';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (error) {
        console.error('Error fetching customer for edit:', error);
        showAlert('Failed to load customer for editing', 'danger');
    }
}

async function deleteCustomer(id) {
    if (!confirm('Are you sure you want to delete this customer?')) return;
    
    try {
        const response = await fetch(`${API_URL}/customers/${id}`, { method: 'DELETE' });
        if (!response.ok) throw new Error('Failed to delete customer');
        showAlert('Customer deleted successfully', 'success');
        fetchCustomers();
    } catch (error) {
        console.error('Error deleting customer:', error);
        showAlert(`Failed to delete customer: ${error.message}`, 'danger');
    }
}

function showAddressModal() {
    document.getElementById('addressCustomerId').value = currentCustomerId;
    document.getElementById('addressForm').reset();
    document.getElementById('addressId').value = '';
    document.querySelector('#addressModal .modal-title').textContent = 'Add New Address';
    customerDetailsModal.hide();
    addressModal.show();
}

async function saveAddress() {
    const addressData = {
        customer_id: parseInt(document.getElementById('addressCustomerId').value),
        address: document.getElementById('addressInput').value,
        district: document.getElementById('districtInput').value,
        city: document.getElementById('cityInput').value,
        province: document.getElementById('provinceInput').value,
        postal_code: document.getElementById('postalCodeInput').value
    };
    
    const addressId = document.getElementById('addressId').value;
    const url = addressId ? `${API_URL}/addresses/${addressId}` : `${API_URL}/addresses`;
    const method = addressId ? 'PUT' : 'POST';
    
    try {
        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(addressData)
        });
        
        if (!response.ok) throw new Error(`Failed to ${addressId ? 'update' : 'add'} address`);
        
        showAlert(`Address ${addressId ? 'updated' : 'added'} successfully`, 'success');
        addressModal.hide();
        document.getElementById('addressForm').reset();
        viewCustomer(currentCustomerId);
    } catch (error) {
        console.error('Error saving address:', error);
        showAlert(`Failed to save address: ${error.message}`, 'danger');
    }
}

async function editAddress(id) {
    try {
        const response = await fetch(`${API_URL}/addresses/${id}`);
        if (!response.ok) throw new Error('Failed to fetch address');
        const address = await response.json();
        
        document.getElementById('addressCustomerId').value = address.customer_id;
        document.getElementById('addressId').value = address.id;
        document.getElementById('addressInput').value = address.address;
        document.getElementById('districtInput').value = address.district;
        document.getElementById('cityInput').value = address.city;
        document.getElementById('provinceInput').value = address.province;
        document.getElementById('postalCodeInput').value = address.postal_code;
        
        document.querySelector('#addressModal .modal-title').textContent = 'Edit Address';
        customerDetailsModal.hide();
        addressModal.show();
    } catch (error) {
        console.error('Error fetching address:', error);
        showAlert('Failed to load address for editing', 'danger');
    }
}

async function deleteAddress(id) {
    if (!confirm('Are you sure you want to delete this address?')) return;
    
    try {
        const response = await fetch(`${API_URL}/addresses/${id}`, { method: 'DELETE' });
        if (!response.ok) throw new Error('Failed to delete address');
        showAlert('Address deleted successfully', 'success');
        viewCustomer(currentCustomerId);
    } catch (error) {
        console.error('Error deleting address:', error);
        showAlert(`Failed to delete address: ${error.message}`, 'danger');
    }
}

async function handleFormSubmit(event) {
    event.preventDefault();
    
    const customerData = {
        title: document.getElementById('title').value,
        name: document.getElementById('name').value,
        gender: document.getElementById('gender').value,
        phone_number: document.getElementById('phoneNumber').value,
        email: document.getElementById('email').value,
        image: document.getElementById('image').value || null
    };
    
    const customerId = document.getElementById('customerId').value;
    const url = customerId ? `${API_URL}/customers/${customerId}` : `${API_URL}/customers`;
    const method = customerId ? 'PUT' : 'POST';
    
    try {
        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(customerData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Operation failed');
        }
        
        showAlert(customerId ? 'Customer updated' : 'Customer added', 'success');
        resetForm();
        fetchCustomers();
    } catch (error) {
        console.error('Form submission error:', error);
        showAlert(`Operation failed: ${error.message}`, 'danger');
    }
}

function resetForm() {
    document.getElementById('customerForm').reset();
    document.getElementById('customerId').value = '';
    document.getElementById('formTitle').textContent = 'Add New Customer';
    document.getElementById('submitBtn').innerHTML = '<i class="bi bi-save me-2"></i>Add Customer';
    document.getElementById('cancelBtn').classList.add('d-none');
    document.getElementById('formSection').style.display = 'none';
}

function showAlert(message, type) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show fixed-top m-3`;
    alert.setAttribute('role', 'alert');
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.prepend(alert);
    setTimeout(() => alert.remove(), 3000);
}