import os
from src.models.download import Download

class DownloadController:
    def __init__(self, db):
        self.db = db

    def add_download(self, user_id, title, url, file_path, file_type):
        """Yeni indirme kaydı ekler"""
        try:
            cursor = self.db.conn.cursor()
            cursor.execute('''
                INSERT INTO downloads (user_id, title, url, file_path, file_type)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, title, url, file_path, file_type))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"İndirme kayıt hatası: {e}")
            return False

    def get_user_downloads(self, user_id):
        """Kullanıcının indirmelerini listeler"""
        try:
            cursor = self.db.conn.cursor()
            cursor.execute('SELECT * FROM downloads WHERE user_id = ? ORDER BY download_date DESC', (user_id,))
            return [Download.from_db_row(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"İndirme listesi hatası: {e}")
            return []

    def delete_download(self, download_id, user_id):
        """İndirme kaydını siler"""
        try:
            cursor = self.db.conn.cursor()
            cursor.execute('DELETE FROM downloads WHERE id = ? AND user_id = ?', (download_id, user_id))
            self.db.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"İndirme silme hatası: {e}")
            return False

    def get_download_stats(self, user_id):
        """Kullanıcının indirme istatistiklerini getirir"""
        try:
            cursor = self.db.conn.cursor()
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_downloads,
                    COUNT(CASE WHEN file_type = 'video' THEN 1 END) as video_count,
                    COUNT(CASE WHEN file_type = 'audio' THEN 1 END) as audio_count
                FROM downloads 
                WHERE user_id = ?
            ''', (user_id,))
            return dict(cursor.fetchone())
        except Exception as e:
            print(f"İstatistik hatası: {e}")
            return {
                'total_downloads': 0,
                'video_count': 0,
                'audio_count': 0
            } 