class Customer:
    def __init__(self, id=None, title=None, name=None, gender=None, phone_number=None, image=None, email=None, created_at=None, updated_at=None):
        self.id = id
        self.title = title
        self.name = name
        self.gender = gender
        self.phone_number = phone_number
        self.image = image
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def from_dict(data):
        return Customer(
            id=data.get('id'),
            title=data.get('title'),
            name=data.get('name'),
            gender=data.get('gender'),
            phone_number=data.get('phone_number'),
            image=data.get('image'),
            email=data.get('email'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def to_dict(self):
        """Convert Customer object to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'name': self.name,
            'gender': self.gender,
            'phone_number': self.phone_number,
            'image': self.image,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }