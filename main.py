import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt
from src.views.login_view import LoginView
from src.views.register_view import RegisterView
from src.views.main_view import MainView
from src.database.database import Database
from src.controllers.auth_controller import AuthController
from src.controllers.download_controller import DownloadController
from src.utils.file_utils import ensure_dir

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_app()
        
    def init_app(self):
        """Uygulama başlangıç ayarlarını yapar"""
        # Pencere ayarları
        self.setWindowTitle('YouTube İndirme Uygulaması')
        self.setGeometry(100, 100, 800, 700)
        self.setMinimumSize(800, 700)
        
        # Kullanıcı bilgisi
        self.current_user = None
        
        # Veritabanı ve kontrolcüler
        self.init_database()
        self.init_controllers()
        
        # Arayüz bileşenleri
        self.init_ui()
        
        # İndirme dizinini oluştur
        downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'YouTube Downloads')
        ensure_dir(downloads_dir)
    
    def init_database(self):
        """Veritabanı bağlantısını başlatır"""
        self.db = Database()
        self.db.create_tables()
    
    def init_controllers(self):
        """Kontrolcüleri başlatır"""
        self.auth_controller = AuthController(self.db)
        self.download_controller = DownloadController(self.db)
    
    def init_ui(self):
        """Arayüz bileşenlerini oluşturur"""
        # Ana widget container'ı
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        # Görünümleri oluştur
        self.login_view = LoginView(self)
        self.register_view = RegisterView(self)
        self.main_view = MainView(self)
        
        # Görünümleri stack'e ekle
        self.central_widget.addWidget(self.login_view)
        self.central_widget.addWidget(self.register_view)
        self.central_widget.addWidget(self.main_view)
        
        # Başlangıç görünümünü ayarla
        self.show_login()
    
    def show_login(self):
        """Giriş ekranını gösterir"""
        self.current_user = None
        self.central_widget.setCurrentWidget(self.login_view)
    
    def show_register(self):
        """Kayıt ekranını gösterir"""
        self.central_widget.setCurrentWidget(self.register_view)
    
    def show_main(self):
        """Ana ekranı gösterir"""
        self.central_widget.setCurrentWidget(self.main_view)
        self.main_view.update_user_info()
        self.main_view.update_downloads_table()
    
    def login(self, username, password):
        """Kullanıcı girişi yapar"""
        user = self.auth_controller.login(username, password)
        if user:
            self.current_user = user.to_dict()
            self.show_main()
            return True
        return False
    
    def register(self, username, password, email):
        """Yeni kullanıcı kaydeder"""
        return self.auth_controller.register(username, password, email)
    
    def logout(self):
        """Kullanıcı çıkışı yapar"""
        self.current_user = None
        self.show_login()

if __name__ == '__main__':
    # Yüksek DPI desteği
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Uygulamayı başlat
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())