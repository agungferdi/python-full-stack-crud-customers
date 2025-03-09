class Address:
    def __init__(self, id=None, customer_id=None, address=None, district=None, city=None, province=None, postal_code=None, created_at=None, updated_at=None):
        self.id = id
        self.customer_id = customer_id
        self.address = address
        self.district = district
        self.city = city
        self.province = province
        self.postal_code = postal_code
        self.created_at = created_at
        self.updated_at = updated_at
        
    @staticmethod
    def from_dict(data):
        return Address(
            id=data.get('id'),
            customer_id=data.get('customer_id'),
            address=data.get('address'),
            district=data.get('district'),
            city=data.get('city'),
            province=data.get('province'),
            postal_code=data.get('postal_code'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
        
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'address': self.address,
            'district': self.district,
            'city': self.city,
            'province': self.province,
            'postal_code': self.postal_code,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }