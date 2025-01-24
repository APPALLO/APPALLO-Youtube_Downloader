import sqlite3
import bcrypt
from pathlib import Path

class Database:
    def __init__(self):
        self.db_file = 'youtube_downloader.db'
        self.conn = None
        self.connect()

    def connect(self):
        """Veritabanına bağlantı oluşturur"""
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print(f"Veritabanı bağlantı hatası: {e}")

    def create_tables(self):
        """Gerekli tabloları oluşturur"""
        try:
            cursor = self.conn.cursor()
            
            # Kullanıcılar tablosu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # İndirilen dosyalar tablosu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS downloads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    download_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Tablo oluşturma hatası: {e}")

    def register_user(self, username, password, email):
        """Yeni kullanıcı kaydeder"""
        try:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, password, email)
                VALUES (?, ?, ?)
            ''', (username, hashed, email))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except sqlite3.Error as e:
            print(f"Kullanıcı kayıt hatası: {e}")
            return False

    def login_user(self, username, password):
        """Kullanıcı girişi kontrol eder"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                return dict(user)
            return None
        except sqlite3.Error as e:
            print(f"Giriş hatası: {e}")
            return None

    def add_download(self, user_id, title, url, file_path, file_type):
        """İndirilen dosyayı kaydeder"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO downloads (user_id, title, url, file_path, file_type)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, title, url, file_path, file_type))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"İndirme kayıt hatası: {e}")
            return False

    def get_user_downloads(self, user_id):
        """Kullanıcının indirdiği dosyaları listeler"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM downloads WHERE user_id = ?', (user_id,))
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"İndirme listesi hatası: {e}")
            return []

    def __del__(self):
        """Veritabanı bağlantısını kapatır"""
        if self.conn:
            self.conn.close() 