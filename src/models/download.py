class Download:
    def __init__(self, id=None, user_id=None, title=None, url=None, file_path=None, 
                 file_type=None, download_date=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.url = url
        self.file_path = file_path
        self.file_type = file_type
        self.download_date = download_date

    @staticmethod
    def from_db_row(row):
        """Veritabanı satırından Download nesnesi oluşturur"""
        if not row:
            return None
        return Download(
            id=row['id'],
            user_id=row['user_id'],
            title=row['title'],
            url=row['url'],
            file_path=row['file_path'],
            file_type=row['file_type'],
            download_date=row['download_date']
        )

    def to_dict(self):
        """Download nesnesini sözlüğe dönüştürür"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'url': self.url,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'download_date': self.download_date
        } 