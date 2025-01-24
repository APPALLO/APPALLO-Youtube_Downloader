class User:
    def __init__(self, id=None, username=None, email=None, password=None, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at

    @staticmethod
    def from_db_row(row):
        """Veritabanı satırından User nesnesi oluşturur"""
        if not row:
            return None
        return User(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            password=row['password'],
            created_at=row['created_at']
        )

    def to_dict(self):
        """User nesnesini sözlüğe dönüştürür"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at
        } 