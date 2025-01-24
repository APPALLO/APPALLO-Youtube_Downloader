from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QPushButton, QMessageBox,
                            QFrame, QGraphicsDropShadowEffect, QApplication,
                            QSizePolicy, QGraphicsOpacityEffect)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer, QSize, QRect, QEvent
from PyQt5.QtGui import (QColor, QFont, QPalette, QIcon, QPixmap, QResizeEvent, 
                        QPainter, QFontDatabase, QLinearGradient)

class LoginView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # Font yükleme
        QFontDatabase.addApplicationFont("resources/fonts/Segoe UI.ttf")
        
        # Pencere özellikleri
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAutoFillBackground(True)
        
        # Arka plan rengi
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#f5f5f5'))
        self.setPalette(palette)
        
        # Minimum boyut
        self.setMinimumSize(400, 600)
        
        # UI oluştur
        self.init_ui()
        
        # Enter tuşu için event filter'ı UI oluşturulduktan sonra kur
        self.username_input.installEventFilter(self)
        self.password_input.installEventFilter(self)
        
    def paintEvent(self, event):
        """Arka plan gradyanı çiz"""
        painter = QPainter()
        if painter.begin(self):
            try:
                painter.setRenderHint(QPainter.Antialiasing)
                
                gradient = QLinearGradient(0, 0, self.width(), self.height())
                gradient.setColorAt(0, QColor('#f5f5f5'))
                gradient.setColorAt(1, QColor('#e3f2fd'))
                
                painter.fillRect(self.rect(), gradient)
            finally:
                painter.end()
        
    def mousePressEvent(self, event):
        """Pencereyi sürüklemek için tıklama pozisyonunu kaydet"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        """Pencereyi sürükle"""
        if event.buttons() == Qt.LeftButton:
            self.parent.move(event.globalPos() - self.drag_position)
            event.accept()
            
    def eventFilter(self, obj, event):
        """Enter tuşu ile giriş yapma ve input alanları için hover efekti"""
        if obj == self.password_input and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return and self.login_button.isEnabled():
                self.login()
                return True
        elif event.type() == QEvent.Enter:
            if obj in [self.username_input, self.password_input]:
                self.add_input_shadow(obj)
        elif event.type() == QEvent.Leave:
            if obj in [self.username_input, self.password_input]:
                self.remove_input_shadow(obj)
        return super().eventFilter(obj, event)
        
    def add_input_shadow(self, widget):
        """Input alanına hover gölgesi ekle"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(33, 150, 243, 50))
        shadow.setOffset(0, 0)
        widget.setGraphicsEffect(shadow)
        
    def remove_input_shadow(self, widget):
        """Input alanından hover gölgesini kaldır"""
        widget.setGraphicsEffect(None)
        
    def init_ui(self):
        """Giriş ekranı arayüzünü oluşturur"""
        # Ana layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Login container frame
        self.login_frame = QFrame()
        self.login_frame.setObjectName('loginFrame')
        self.login_frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.login_frame.setFixedSize(400, 600)
        self.login_frame.setStyleSheet('''
            QFrame#loginFrame {
                background: white;
                border-radius: 20px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
        ''')
        
        # Login frame layout
        login_layout = QVBoxLayout(self.login_frame)
        login_layout.setSpacing(25)
        login_layout.setContentsMargins(40, 40, 40, 40)
        
        # Container widget for effects
        self.effect_container = QWidget()
        self.effect_container.setLayout(QVBoxLayout())
        self.effect_container.layout().setContentsMargins(0, 0, 0, 0)
        self.effect_container.layout().addWidget(self.login_frame)
        
        # Add shadow effect to container
        shadow = QGraphicsDropShadowEffect(self.effect_container)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 5)
        self.effect_container.setGraphicsEffect(shadow)
        
        # Logo ve başlık container'ı
        header_container = QFrame()
        header_layout = QVBoxLayout(header_container)
        header_layout.setSpacing(15)
        header_layout.setAlignment(Qt.AlignCenter)
        
        # Logo
        self.logo_label = QLabel()
        logo_pixmap = QPixmap('resources/icons/youtube.png')
        if not logo_pixmap.isNull():
            self.logo_label.original_pixmap = logo_pixmap
            scaled_pixmap = logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(scaled_pixmap)
            self.logo_label.setAlignment(Qt.AlignCenter)
        
        # Başlık
        self.title_label = QLabel('YouTube İndirme')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('''
            font-size: 28px;
            color: #1976D2;
            font-weight: bold;
            font-family: "Segoe UI";
            margin-top: 10px;
        ''')
        
        # Alt başlık
        self.subtitle_label = QLabel('Hoş Geldiniz')
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet('''
            font-size: 16px;
            color: #757575;
            font-family: "Segoe UI";
            margin-bottom: 20px;
        ''')
        
        header_layout.addWidget(self.logo_label)
        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.subtitle_label)
        
        # Form container
        form_container = QFrame()
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(20)
        
        # Kullanıcı adı
        username_container = QFrame()
        username_layout = QVBoxLayout(username_container)
        username_layout.setSpacing(8)
        
        username_label = QLabel('Kullanıcı Adı')
        username_label.setStyleSheet('''
            font-size: 14px;
            font-weight: bold;
            color: #424242;
            font-family: "Segoe UI";
        ''')
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Kullanıcı adınızı girin')
        self.username_input.textChanged.connect(self.validate_inputs)
        self.username_input.setStyleSheet('''
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-size: 14px;
                font-family: "Segoe UI";
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
                background-color: white;
            }
        ''')
        
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        
        # Şifre
        password_container = QFrame()
        password_layout = QVBoxLayout(password_container)
        password_layout.setSpacing(8)
        
        password_label = QLabel('Şifre')
        password_label.setStyleSheet('''
            font-size: 14px;
            font-weight: bold;
            color: #424242;
            font-family: "Segoe UI";
        ''')
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Şifrenizi girin')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.textChanged.connect(self.validate_inputs)
        self.password_input.setStyleSheet('''
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-size: 14px;
                font-family: "Segoe UI";
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
                background-color: white;
            }
        ''')
        
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        
        form_layout.addWidget(username_container)
        form_layout.addWidget(password_container)
        
        # Butonlar container'ı
        buttons_container = QFrame()
        buttons_layout = QVBoxLayout(buttons_container)
        buttons_layout.setSpacing(15)
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        self.login_button = QPushButton('Giriş Yap')
        self.login_button.setObjectName('loginButton')
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self.login)
        self.login_button.setEnabled(False)
        self.login_button.setFixedSize(320, 45)
        self.login_button.setStyleSheet('''
            QPushButton#loginButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2196F3, stop:1 #1976D2);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
                font-family: "Segoe UI";
            }
            QPushButton#loginButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1976D2, stop:1 #1565C0);
            }
            QPushButton#loginButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1565C0, stop:1 #0D47A1);
            }
            QPushButton#loginButton:disabled {
                background: #BDBDBD;
                color: rgba(255, 255, 255, 0.7);
            }
        ''')
        
        self.register_button = QPushButton('Hesabınız yok mu? Kayıt olun')
        self.register_button.setObjectName('registerButton')
        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.clicked.connect(self.show_register)
        self.register_button.setStyleSheet('''
            QPushButton#registerButton {
                background: transparent;
                color: #2196F3;
                border: none;
                font-size: 14px;
                font-family: "Segoe UI";
            }
            QPushButton#registerButton:hover {
                color: #1976D2;
                text-decoration: underline;
            }
        ''')
        
        buttons_layout.addWidget(self.login_button)
        buttons_layout.addWidget(self.register_button)
        
        # Layout'ları birleştir
        login_layout.addWidget(header_container)
        login_layout.addWidget(form_container)
        login_layout.addWidget(buttons_container)
        
        # Add container to main layout instead of frame
        main_layout.addWidget(self.effect_container, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)
        
        # Animasyonlar için hazırlık
        self.setup_animations()

    def apply_styles(self):
        """Stil ayarlarını uygular"""
        self.login_frame.setStyleSheet('''
            QFrame#loginFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ffffff, stop:1 #f8f9fa);
                border-radius: 20px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
            QLabel {
                color: #424242;
                font-family: "Segoe UI", Arial;
            }
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-size: 14px;
                font-family: "Segoe UI", Arial;
                background-color: #f8f9fa;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
                background-color: white;
            }
            QLineEdit:hover {
                border: 2px solid #90caf9;
                background-color: #fafafa;
            }
            QPushButton {
                padding: 12px;
                border-radius: 10px;
                font-size: 14px;
                font-family: "Segoe UI", Arial;
                font-weight: bold;
                min-width: 140px;
            }
            QPushButton#loginButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2196F3, stop:1 #1976D2);
                color: white;
                border: none;
            }
            QPushButton#loginButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1976D2, stop:1 #1565C0);
            }
            QPushButton#loginButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1565C0, stop:1 #0D47A1);
                padding-top: 14px;
                padding-bottom: 10px;
            }
            QPushButton#loginButton:disabled {
                background: #9E9E9E;
                color: rgba(255, 255, 255, 0.7);
            }
            QPushButton#registerButton {
                background: transparent;
                color: #2196F3;
                border: none;
                font-weight: normal;
                text-decoration: underline;
            }
            QPushButton#registerButton:hover {
                color: #1976D2;
                text-decoration: none;
            }
            QPushButton#registerButton:pressed {
                color: #0D47A1;
            }
        ''')
        
        # Frame gölge efekti
        frame_shadow = QGraphicsDropShadowEffect()
        frame_shadow.setBlurRadius(40)
        frame_shadow.setColor(QColor(0, 0, 0, 30))
        frame_shadow.setOffset(0, 5)
        self.login_frame.setGraphicsEffect(frame_shadow)

    def setup_animations(self):
        """Giriş animasyonlarını hazırlar"""
        # Pozisyon animasyonu
        self.pos_anim = QPropertyAnimation(self.effect_container, b'pos')
        self.pos_anim.setDuration(1000)
        self.pos_anim.setStartValue(self.effect_container.pos() + QPoint(0, 50))
        self.pos_anim.setEndValue(self.effect_container.pos())
        self.pos_anim.setEasingCurve(QEasingCurve.OutBack)

    def showEvent(self, event):
        """Widget gösterildiğinde animasyonları başlatır ve pencereyi ortalar"""
        super().showEvent(event)
        
        # Pencereyi ekranın ortasına konumlandır
        if self.parent:
            # Önce pencere boyutunu ayarla
            self.adjustSize()
            
            # Ana pencere merkezini al
            parent_center = self.parent.geometry().center()
            
            # Pencereyi ana pencere merkezine göre konumlandır
            geometry = self.geometry()
            geometry.moveCenter(parent_center)
            self.setGeometry(geometry)
        
        # Animasyonları başlat
        QTimer.singleShot(100, self.start_animations)
        self.username_input.setFocus()

    def resizeEvent(self, event):
        """Pencere boyutu değiştiğinde çağrılır"""
        super().resizeEvent(event)
        
        # Effect container'ı ortala
        container_pos = self.effect_container.pos()
        self.effect_container.move(
            (self.width() - self.effect_container.width()) // 2,
            (self.height() - self.effect_container.height()) // 2
        )

    def start_animations(self):
        """Animasyonları başlatır"""
        self.pos_anim.start()
            
    def validate_inputs(self):
        """Giriş alanlarını kontrol eder"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        # En az 3 karakter kontrolü
        is_valid = len(username) >= 3 and len(password) >= 3
        self.login_button.setEnabled(is_valid)
        
        # Input stilleri güncelle
        for input_field, text in [(self.username_input, username), (self.password_input, password)]:
            input_field.setStyleSheet(f'''
                QLineEdit {{
                    padding: 12px;
                    border: 2px solid {('#2196F3' if len(text) >= 3 else '#e0e0e0')};
                    border-radius: 10px;
                    font-size: 14px;
                    font-family: "Segoe UI";
                    background-color: {('white' if len(text) >= 3 else '#f5f5f5')};
                }}
                QLineEdit:focus {{
                    border: 2px solid #2196F3;
                    background-color: white;
                }}
            ''')

    def login(self):
        """Giriş işlemini gerçekleştirir"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            self.show_error_message('Lütfen tüm alanları doldurun!')
            return
        
        # Giriş butonunu devre dışı bırak
        self.login_button.setEnabled(False)
        self.login_button.setText('Giriş yapılıyor...')
        QApplication.processEvents()
        
        try:
            if self.parent.login(username, password):
                self.show_success_message()
            else:
                self.show_error_animation()
                self.show_error_message('Kullanıcı adı veya şifre hatalı!')
                self.password_input.clear()
                self.password_input.setFocus()
        except Exception as e:
            self.show_error_message(f'Giriş yapılırken bir hata oluştu: {str(e)}')
        finally:
            # Giriş butonunu tekrar etkinleştir
            self.login_button.setText('Giriş Yap')
            self.login_button.setEnabled(True)

    def show_register(self):
        """Kayıt ekranını gösterir"""
        self.username_input.clear()
        self.password_input.clear()
        self.parent.show_register()

    def show_error_animation(self):
        """Hata durumunda sallama animasyonu"""
        # Sallama animasyonu
        pos_anim = QPropertyAnimation(self.effect_container, b'pos')
        pos_anim.setDuration(50)
        pos_anim.setLoopCount(6)
        
        original_pos = self.effect_container.pos()
        shake_offset = 10
        
        keyframes = [
            (0.0, original_pos),
            (0.1, original_pos + QPoint(shake_offset, 0)),
            (0.2, original_pos + QPoint(-shake_offset, 0)),
            (0.3, original_pos + QPoint(shake_offset, 0)),
            (0.4, original_pos + QPoint(-shake_offset, 0)),
            (0.5, original_pos + QPoint(shake_offset, 0)),
            (1.0, original_pos)
        ]
        
        for frame, pos in keyframes:
            pos_anim.setKeyValueAt(frame, pos)
        
        # Kırmızı yanıp sönme efekti
        original_style = self.login_frame.styleSheet()
        error_style = '''
            QFrame#loginFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #fff5f5, stop:1 #ffebee);
                border-radius: 20px;
                border: 2px solid #ef5350;
            }
        '''
        
        self.login_frame.setStyleSheet(error_style)
        pos_anim.start()
        
        # 500ms sonra normal stile geri dön
        QTimer.singleShot(500, lambda: self.login_frame.setStyleSheet(original_style))

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
                font-family: "Segoe UI";
                min-width: 300px;
            }
            QPushButton {
                padding: 8px 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f44336, stop:1 #d32f2f);
                color: white;
                border-radius: 6px;
                border: none;
                font-family: "Segoe UI";
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

    def show_success_message(self):
        """Başarılı giriş mesajı"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText('Giriş Başarılı!')
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
                font-family: "Segoe UI";
                min-width: 300px;
            }
            QPushButton {
                padding: 8px 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4CAF50, stop:1 #388E3C);
                color: white;
                border-radius: 6px;
                border: none;
                font-family: "Segoe UI";
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