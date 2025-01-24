from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QComboBox, QProgressBar,
                             QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog,
                             QFrame, QGraphicsDropShadowEffect, QHeaderView, QStyle,
                             QGraphicsOpacityEffect, QMenu)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QPoint, QSize
from PyQt5.QtGui import QColor, QFont, QPalette, QIcon
import yt_dlp
import os
from src.utils.validators import validate_youtube_url
from src.utils.file_utils import get_file_size

class DownloadThread(QThread):
    progress = pyqtSignal(float)
    finished = pyqtSignal(bool, str)
    info = pyqtSignal(dict)

    def __init__(self, url, download_path, format_id='best'):
        super().__init__()
        self.url = url
        self.download_path = download_path
        self.format_id = format_id

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                if total > 0:
                    progress = (downloaded / total) * 100
                    self.progress.emit(progress)
            except:
                pass
        elif d['status'] == 'finished':
            self.progress.emit(100)

    def run(self):
        try:
            ydl_opts = {
                'format': self.format_id,
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'nocheckcertificate': True,
                'ignoreerrors': True,
                'no_color': True,
                'geo_bypass': True,
                'cookies': None,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
            }
            
            if self.format_id == 'bestaudio/best':
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                ydl_opts.update({
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                })
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                if info:
                    self.info.emit(info)
                    ydl.download([self.url])
                    self.finished.emit(True, '')
                else:
                    self.finished.emit(False, 'Video bilgileri alınamadı')
        except Exception as e:
            self.finished.emit(False, str(e))

class MainView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.download_thread = None
        self.init_ui()
        
    def init_ui(self):
        """Ana ekran arayüzünü oluşturur"""
        # Ana layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Üst bilgi paneli
        info_panel = QFrame()
        info_panel.setObjectName('infoPanel')
        info_panel.setStyleSheet('''
            QFrame#infoPanel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2196F3, stop:1 #1976D2);
                border-radius: 15px;
                padding: 15px;
            }
        ''')
        
        info_layout = QHBoxLayout(info_panel)
        info_layout.setContentsMargins(20, 10, 20, 10)
        
        self.user_label = QLabel()
        self.user_label.setStyleSheet('color: white; font-size: 18px; font-weight: bold; font-family: "Segoe UI", Arial;')
        
        logout_button = QPushButton('Çıkış Yap')
        logout_button.setCursor(Qt.PointingHandCursor)
        logout_button.setStyleSheet('''
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.2);
                padding: 8px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                font-family: "Segoe UI", Arial;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                border: 2px solid rgba(255, 255, 255, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.3);
            }
        ''')
        logout_button.clicked.connect(self.logout)
        
        info_layout.addWidget(self.user_label)
        info_layout.addStretch()
        info_layout.addWidget(logout_button)
        
        main_layout.addWidget(info_panel)
        
        # İndirme paneli
        download_panel = QFrame()
        download_panel.setObjectName('downloadPanel')
        download_panel.setStyleSheet('''
            QFrame#downloadPanel {
                background-color: white;
                border-radius: 15px;
                border: 2px solid #e0e0e0;
            }
            QLabel {
                color: #424242;
                font-size: 14px;
                font-family: "Segoe UI", Arial;
                font-weight: bold;
            }
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                font-family: "Segoe UI", Arial;
                background-color: #f5f5f5;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
                background-color: white;
            }
            QLineEdit:hover {
                background-color: #fafafa;
            }
            QComboBox {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                font-family: "Segoe UI", Arial;
                background-color: #f5f5f5;
            }
            QComboBox:focus {
                border: 2px solid #2196F3;
                background-color: white;
            }
            QComboBox:hover {
                background-color: #fafafa;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox::down-arrow {
                image: url(resources/icons/down-arrow.png);
                width: 12px;
                height: 12px;
            }
            QPushButton {
                padding: 12px;
                border-radius: 8px;
                font-size: 14px;
                font-family: "Segoe UI", Arial;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton#downloadButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4CAF50, stop:1 #388E3C);
                color: white;
                border: none;
            }
            QPushButton#downloadButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #388E3C, stop:1 #2E7D32);
            }
            QPushButton#downloadButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2E7D32, stop:1 #1B5E20);
            }
            QPushButton#downloadButton:disabled {
                background: #9E9E9E;
            }
            QPushButton#browseButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2196F3, stop:1 #1976D2);
                color: white;
                border: none;
            }
            QPushButton#browseButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1976D2, stop:1 #1565C0);
            }
            QPushButton#browseButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1565C0, stop:1 #0D47A1);
            }
            QProgressBar {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                text-align: center;
                height: 25px;
                font-family: "Segoe UI", Arial;
                font-weight: bold;
                font-size: 12px;
                background-color: #f5f5f5;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4CAF50, stop:1 #388E3C);
                border-radius: 6px;
            }
        ''')
        
        download_layout = QVBoxLayout(download_panel)
        download_layout.setSpacing(20)
        download_layout.setContentsMargins(25, 25, 25, 25)
        
        # URL girişi
        url_layout = QHBoxLayout()
        url_label = QLabel('Video URL:')
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('YouTube video URL\'sini girin')
        self.url_input.textChanged.connect(self.validate_url)
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        download_layout.addLayout(url_layout)
        
        # İndirme seçenekleri
        options_layout = QHBoxLayout()
        options_layout.setSpacing(15)
        
        # Format seçimi
        format_layout = QVBoxLayout()
        format_label = QLabel('Format:')
        self.format_combo = QComboBox()
        self.format_combo.addItems(['Video (En İyi Kalite)', 'Sadece Ses (MP3)'])
        self.format_combo.setCursor(Qt.PointingHandCursor)
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        options_layout.addLayout(format_layout)
        
        # İndirme konumu
        path_layout = QVBoxLayout()
        path_label = QLabel('Konum:')
        path_input_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setReadOnly(True)
        browse_button = QPushButton('Gözat')
        browse_button.setObjectName('browseButton')
        browse_button.setCursor(Qt.PointingHandCursor)
        browse_button.clicked.connect(self.browse_path)
        path_input_layout.addWidget(self.path_input)
        path_input_layout.addWidget(browse_button)
        path_layout.addWidget(path_label)
        path_layout.addLayout(path_input_layout)
        options_layout.addLayout(path_layout)
        
        download_layout.addLayout(options_layout)
        
        # İndirme butonu ve progress bar
        download_layout_bottom = QHBoxLayout()
        download_layout_bottom.setSpacing(15)
        
        self.download_button = QPushButton('İndir')
        self.download_button.setObjectName('downloadButton')
        self.download_button.setCursor(Qt.PointingHandCursor)
        self.download_button.clicked.connect(self.start_download)
        self.download_button.setEnabled(False)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat('%p%')
        
        download_layout_bottom.addWidget(self.download_button)
        download_layout_bottom.addWidget(self.progress_bar)
        download_layout.addLayout(download_layout_bottom)
        
        main_layout.addWidget(download_panel)
        
        # İndirme listesi paneli
        list_panel = QFrame()
        list_panel.setObjectName('listPanel')
        list_panel.setStyleSheet('''
            QFrame#listPanel {
                background-color: white;
                border-radius: 15px;
                border: 2px solid #e0e0e0;
            }
            QLabel {
                color: #424242;
                font-family: "Segoe UI", Arial;
            }
            QTableWidget {
                border: none;
                gridline-color: #e0e0e0;
                font-family: "Segoe UI", Arial;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976D2;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 10px;
                border: none;
                border-right: 1px solid #e0e0e0;
                border-bottom: 2px solid #e0e0e0;
                font-weight: bold;
                color: #424242;
            }
            QHeaderView::section:hover {
                background-color: #eeeeee;
            }
            QScrollBar:vertical {
                border: none;
                background: #f5f5f5;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #bdbdbd;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9e9e9e;
            }
        ''')
        
        list_layout = QVBoxLayout(list_panel)
        list_layout.setContentsMargins(25, 25, 25, 25)
        list_layout.setSpacing(15)
        
        # İndirme listesi başlığı
        list_title = QLabel('İndirme Geçmişi')
        list_title.setStyleSheet('font-size: 20px; font-weight: bold; color: #424242; margin-bottom: 10px;')
        list_layout.addWidget(list_title)
        
        # İndirme listesi tablosu
        self.downloads_table = QTableWidget()
        self.downloads_table.setColumnCount(5)
        self.downloads_table.setHorizontalHeaderLabels(['Başlık', 'Format', 'Boyut', 'Durum', 'Tarih'])
        self.downloads_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.downloads_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.downloads_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.downloads_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.downloads_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.downloads_table.setAlternatingRowColors(True)
        self.downloads_table.setShowGrid(False)
        self.downloads_table.verticalHeader().setVisible(False)
        self.downloads_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.downloads_table.setSelectionMode(QTableWidget.SingleSelection)
        self.downloads_table.setStyleSheet('''
            QTableWidget {
                border: none;
                background-color: white;
                gridline-color: transparent;
                font-family: "Segoe UI", Arial;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #f0f0f0;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976D2;
            }
            QTableWidget::item:hover {
                background-color: #f5f5f5;
            }
            QHeaderView::section {
                background-color: white;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #e0e0e0;
                font-weight: bold;
                color: #424242;
                font-size: 13px;
            }
            QHeaderView::section:hover {
                background-color: #f5f5f5;
                border-bottom: 2px solid #2196F3;
            }
            QScrollBar:vertical {
                border: none;
                background: #f5f5f5;
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #bdbdbd;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9e9e9e;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        ''')
        
        # Sağ tık menüsü için context menu oluştur
        self.downloads_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.downloads_table.customContextMenuRequested.connect(self.show_context_menu)
        
        list_layout.addWidget(self.downloads_table)
        
        main_layout.addWidget(list_panel)
        
        # Gölge efektleri
        for panel in [info_panel, download_panel, list_panel]:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(30)
            shadow.setColor(QColor(0, 0, 0, 40))
            shadow.setOffset(0, 3)
            panel.setGraphicsEffect(shadow)
        
        self.setLayout(main_layout)
        
        # Varsayılan indirme konumu
        default_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'YouTube Downloads')
        self.path_input.setText(default_path)
        
        # Animasyonlar için hazırlık
        self.setup_animations()

    def setup_animations(self):
        """Panel animasyonlarını hazırlar"""
        for i, panel in enumerate(self.findChildren(QFrame)):
            # Pozisyon animasyonu
            pos_anim = QPropertyAnimation(panel, b'pos')
            pos_anim.setDuration(600 + i * 100)
            pos_anim.setStartValue(panel.pos() + QPoint(0, 50))
            pos_anim.setEndValue(panel.pos())
            pos_anim.setEasingCurve(QEasingCurve.OutBack)
            
            # Gölge efekti
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(30)
            shadow.setColor(QColor(0, 0, 0, 40))
            shadow.setOffset(0, 3)
            panel.setGraphicsEffect(shadow)
            
            panel.pos_anim = pos_anim

    def showEvent(self, event):
        """Widget gösterildiğinde animasyonları başlatır ve düzeni günceller"""
        super().showEvent(event)
        # Panellerin pozisyonlarını güncelle
        self.updateGeometry()
        self.adjustSize()
        
        # Animasyonları başlat
        for panel in self.findChildren(QFrame):
            if hasattr(panel, 'pos_anim'):
                panel.pos_anim.setStartValue(panel.pos() + QPoint(0, 50))
                panel.pos_anim.setEndValue(panel.pos())
                panel.pos_anim.start()

    def resizeEvent(self, event):
        """Pencere boyutu değiştiğinde düzeni günceller"""
        super().resizeEvent(event)
        # Tablo sütunlarını yeniden boyutlandır
        if hasattr(self, 'downloads_table'):
            header = self.downloads_table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.Stretch)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        # Panellerin pozisyonlarını güncelle
        for panel in self.findChildren(QFrame):
            if hasattr(panel, 'pos_anim'):
                panel.pos_anim.setEndValue(panel.pos())

    def validate_url(self):
        """URL'yi doğrular"""
        url = self.url_input.text().strip()
        is_valid = validate_youtube_url(url)
        
        self.url_input.setStyleSheet(f'''
            QLineEdit {{
                padding: 10px;
                border: 2px solid {('#4CAF50' if is_valid else '#e0e0e0')};
                border-radius: 5px;
                font-size: 14px;
            }}
        ''')
        
        self.download_button.setEnabled(is_valid)

    def browse_path(self):
        """İndirme konumu seçme dialog'unu açar"""
        path = QFileDialog.getExistingDirectory(
            self,
            'İndirme Konumu Seç',
            self.path_input.text(),
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if path:
            self.path_input.setText(path)

    def start_download(self):
        """İndirme işlemini başlatır"""
        url = self.url_input.text().strip()
        download_path = self.path_input.text()
        
        if not url:
            self.show_error_message('Lütfen bir URL girin!')
            return
            
        if not download_path:
            self.show_error_message('Lütfen indirme konumu seçin!')
            return
        
        # Format seçimi
        format_id = 'bestaudio/best' if self.format_combo.currentIndex() == 1 else 'best'
        
        # İndirme thread'ini başlat
        self.download_button.setEnabled(False)
        self.progress_bar.setValue(0)
        
        self.download_thread = DownloadThread(url, download_path, format_id)
        self.download_thread.progress.connect(self.update_progress)
        self.download_thread.finished.connect(self.download_finished)
        self.download_thread.info.connect(self.save_download_info)
        self.download_thread.start()

    def update_progress(self, progress):
        """İndirme ilerlemesini günceller"""
        self.progress_bar.setValue(int(progress))

    def download_finished(self, success, error):
        """İndirme tamamlandığında çağrılır"""
        self.download_button.setEnabled(True)
        
        if success:
            self.show_success_message('İndirme işlemi tamamlandı!')
            self.url_input.clear()
            self.update_downloads_table()
        else:
            self.show_error_message(f'İndirme başarısız: {error}')

    def save_download_info(self, info):
        """İndirme bilgilerini veritabanına kaydeder"""
        title = info.get('title', 'Bilinmeyen')
        url = self.url_input.text()
        file_path = self.path_input.text()
        file_type = 'audio' if self.format_combo.currentIndex() == 1 else 'video'
        
        self.parent.download_controller.add_download(
            self.parent.current_user['id'],
            title,
            url,
            file_path,
            file_type
        )

    def update_downloads_table(self):
        """İndirme listesini günceller"""
        if hasattr(self.parent, 'current_user') and self.parent.current_user:
            downloads = self.parent.download_controller.get_user_downloads(self.parent.current_user['id'])
            self.downloads_table.setRowCount(len(downloads))
            
            for i, download in enumerate(downloads):
                # Başlık
                title_item = QTableWidgetItem(download.title)
                title_item.setData(Qt.UserRole, download.id)
                self.downloads_table.setItem(i, 0, title_item)
                
                # Format
                format_item = QTableWidgetItem('Video' if download.file_type == 'video' else 'Ses')
                format_item.setTextAlignment(Qt.AlignCenter)
                self.downloads_table.setItem(i, 1, format_item)
                
                # Boyut
                size = get_file_size(os.path.join(download.file_path, f"{download.title}.{'mp4' if download.file_type == 'video' else 'mp3'}"))
                size_item = QTableWidgetItem(size)
                size_item.setTextAlignment(Qt.AlignCenter)
                self.downloads_table.setItem(i, 2, size_item)
                
                # Durum
                status_item = QTableWidgetItem('Tamamlandı')
                status_item.setForeground(QColor('#4CAF50'))
                status_item.setTextAlignment(Qt.AlignCenter)
                self.downloads_table.setItem(i, 3, status_item)
                
                # Tarih
                date_item = QTableWidgetItem(download.download_date)
                date_item.setTextAlignment(Qt.AlignCenter)
                self.downloads_table.setItem(i, 4, date_item)

    def update_user_info(self):
        """Kullanıcı bilgisini günceller ve ekranı yeniler"""
        if hasattr(self.parent, 'current_user') and self.parent.current_user:
            self.user_label.setText(f'Hoş geldin, {self.parent.current_user["username"]}!')
            # Ekranı yenile
            self.updateGeometry()
            self.adjustSize()
            self.update()

    def show_error_message(self, message):
        """Hata mesajı gösterir"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle('Hata')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet('''
            QMessageBox {
                background-color: white;
                border-radius: 10px;
            }
            QLabel {
                color: #424242;
                font-size: 14px;
                font-family: "Segoe UI", Arial;
                min-width: 300px;
            }
            QPushButton {
                padding: 8px 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f44336, stop:1 #d32f2f);
                color: white;
                border-radius: 6px;
                border: none;
                font-family: "Segoe UI", Arial;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #d32f2f, stop:1 #c62828);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #c62828, stop:1 #b71c1c);
            }
        ''')
        msg.exec_()

    def show_success_message(self, message):
        """Başarı mesajı gösterir"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle('Başarılı')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet('''
            QMessageBox {
                background-color: white;
                border-radius: 10px;
            }
            QLabel {
                color: #424242;
                font-size: 14px;
                font-family: "Segoe UI", Arial;
                min-width: 300px;
            }
            QPushButton {
                padding: 8px 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4CAF50, stop:1 #388E3C);
                color: white;
                border-radius: 6px;
                border: none;
                font-family: "Segoe UI", Arial;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #388E3C, stop:1 #2E7D32);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2E7D32, stop:1 #1B5E20);
            }
        ''')
        msg.exec_()

    def logout(self):
        """Çıkış yapar"""
        self.parent.logout()
        self.url_input.clear()
        self.progress_bar.setValue(0)
        self.downloads_table.setRowCount(0)

    def show_context_menu(self, position):
        """Sağ tık menüsünü gösterir"""
        menu = QMenu()
        menu.setStyleSheet('''
            QMenu {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 25px;
                border-radius: 4px;
                margin: 2px 5px;
                color: #424242;
                font-family: "Segoe UI", Arial;
            }
            QMenu::item:selected {
                background-color: #e3f2fd;
                color: #1976D2;
            }
            QMenu::separator {
                height: 1px;
                background-color: #e0e0e0;
                margin: 5px 15px;
            }
        ''')

        row = self.downloads_table.rowAt(position.y())
        if row >= 0:
            open_folder = menu.addAction('Klasörü Aç')
            open_folder.triggered.connect(lambda: self.open_download_folder(row))
            menu.addSeparator()
            delete_item = menu.addAction('Sil')
            delete_item.triggered.connect(lambda: self.delete_download(row))
            
            menu.exec_(self.downloads_table.viewport().mapToGlobal(position))

    def open_download_folder(self, row):
        """İndirilen dosyanın klasörünü açar"""
        file_path = self.downloads_table.item(row, 2).text()
        folder_path = os.path.dirname(file_path)
        os.startfile(folder_path)

    def delete_download(self, row):
        """İndirme kaydını siler"""
        reply = QMessageBox.question(
            self, 
            'Silme Onayı',
            'Bu indirme kaydını silmek istediğinize emin misiniz?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            download_id = self.downloads_table.item(row, 0).data(Qt.UserRole)
            if self.parent.download_controller.delete_download(download_id):
                self.downloads_table.removeRow(row)
                self.show_success_message('İndirme kaydı başarıyla silindi.')
            else:
                self.show_error_message('İndirme kaydı silinirken bir hata oluştu.')

    def show_login(self):
        """Giriş ekranını gösterir"""
        from src.views.login_view import LoginView
        
        # Giriş ekranını oluştur
        login_view = LoginView(self)
        
        # Pencere boyutunu ayarla
        login_view.adjustSize()
        
        # Ana pencere merkezini al
        parent_center = self.geometry().center()
        
        # Pencereyi ana pencere merkezine göre konumlandır
        geometry = login_view.geometry()
        geometry.moveCenter(parent_center)
        login_view.setGeometry(geometry)
        
        # Giriş ekranını göster
        login_view.show()
        
        return login_view 