import bcrypt
from src.models.user import User

class AuthController:
    def __init__(self, db):
        self.db = db

    def register(self, username, password, email):
        """Yeni kullanıcı kaydeder"""
        try:
            # Şifreyi hashle
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Kullanıcıyı veritabanına kaydet
            cursor = self.db.conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, password, email)
                VALUES (?, ?, ?)
            ''', (username, hashed, email))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Kayıt hatası: {e}")
            return False

    def login(self, username, password):
        """Kullanıcı girişi yapar"""
        try:
            cursor = self.db.conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            row = cursor.fetchone()
            
            if row and bcrypt.checkpw(password.encode('utf-8'), row['password']):
                return User.from_db_row(row)
            return None
        except Exception as e:
            print(f"Giriş hatası: {e}")
            return None

    def change_password(self, user_id, old_password, new_password):
        """Kullanıcı şifresini değiştirir"""
        try:
            cursor = self.db.conn.cursor()
            cursor.execute('SELECT password FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            
            if row and bcrypt.checkpw(old_password.encode('utf-8'), row['password']):
                hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute('UPDATE users SET password = ? WHERE id = ?', (hashed, user_id))
                self.db.conn.commit()
                return True
            return False
        except Exception as e:
            print(f"Şifre değiştirme hatası: {e}")
            return False 