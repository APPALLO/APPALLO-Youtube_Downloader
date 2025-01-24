from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QPushButton, QMessageBox,
                            QFrame, QGraphicsDropShadowEffect, QApplication,
                            QSizePolicy, QGraphicsOpacityEffect, QScrollArea)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer, QSize, QRect, QEvent, QAbstractAnimation
from PyQt5.QtGui import (QColor, QFont, QPalette, QIcon, QPixmap, QResizeEvent, 
                        QPainter, QFontDatabase, QLinearGradient)
from src.utils.validators import validate_email, validate_password, validate_username

class RegisterView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # Boyut oranları
        self.base_width = 600
        self.base_height = 700
        self.scale_factor = 1.0
        
        # Sürükleme için değişkenler
        self.drag_position = None
        self.dragging = False
        
        # Input alanlarını oluştur
        self.username_input = QLineEdit()
        self.email_input = QLineEdit()
        self.password_input = QLineEdit()
        self.confirm_password_input = QLineEdit()
        
        # Font yükleme
        QFontDatabase.addApplicationFont("resources/fonts/Segoe UI.ttf")
        
        # Pencere özellikleri
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Stil ayarla
        self.setStyleSheet('''
            RegisterView {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #E3F2FD,
                    stop:0.5 #BBDEFB,
                    stop:1 #90CAF9);
            }
        ''')
        
        # Minimum pencere boyutu
        self.setMinimumSize(400, 600)
        
        # UI oluştur
        self.init_ui()
        
        # Event filter'ları kur
        self.username_input.installEventFilter(self)
        self.email_input.installEventFilter(self)
        self.password_input.installEventFilter(self)
        self.confirm_password_input.installEventFilter(self)
        
        # Animasyonlar için hazırlık
        self.setup_animations()

    def calculate_scale_factor(self):
        """Pencere boyutuna göre ölçekleme faktörünü hesaplar"""
        width_scale = self.width() / self.base_width
        height_scale = self.height() / self.base_height
        self.scale_factor = min(width_scale, height_scale)
        return self.scale_factor

    def scaled_size(self, size):
        """Verilen boyutu ölçekler"""
        return int(size * self.scale_factor)

    def update_styles(self):
        """Tüm elemanların stillerini günceller"""
        scale = self.calculate_scale_factor()
        font_size = self.scaled_size(15)
        padding = self.scaled_size(14)
        border_radius = self.scaled_size(15)
        
        # Input alanları için stil
        input_style = f'''
            QLineEdit {{
                padding: {padding}px {int(padding*1.3)}px;
                border: 2px solid #E0E0E0;
                border-radius: {border_radius}px;
                font-size: {font_size}px;
                font-family: "Segoe UI";
                background-color: #F5F5F5;
                color: #424242;
                min-height: {self.scaled_size(25)}px;
            }}
        '''
        
        # Input alanlarına stili uygula
        for input_widget in [self.username_input, self.email_input, 
                           self.password_input, self.confirm_password_input]:
            input_widget.setStyleSheet(input_style)
            input_widget.setFixedHeight(self.scaled_size(50))
        
        # Başlık için stil
        self.title_label.setStyleSheet(f'''
            font-size: {self.scaled_size(28)}px;
            color: #1565C0;
            font-weight: bold;
            font-family: "Segoe UI";
            margin-top: {self.scaled_size(10)}px;
        ''')
        
        # Alt başlık için stil
        self.subtitle_label.setStyleSheet(f'''
            font-size: {self.scaled_size(16)}px;
            color: #546E7A;
            font-family: "Segoe UI";
            margin-bottom: {self.scaled_size(20)}px;
        ''')
        
        # Kayıt butonu için stil
        self.register_button.setFixedSize(
            self.scaled_size(320),
            self.scaled_size(55)
        )
        self.register_button.setStyleSheet(f'''
            QPushButton#registerButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2196F3, stop:1 #1976D2);
                color: white;
                border: none;
                border-radius: {self.scaled_size(15)}px;
                font-size: {self.scaled_size(16)}px;
                font-weight: bold;
                font-family: "Segoe UI";
                padding: {self.scaled_size(10)}px;
            }}
            QPushButton#registerButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1E88E5, stop:1 #1565C0);
            }}
            QPushButton#registerButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1976D2, stop:1 #0D47A1);
                padding-top: {self.scaled_size(12)}px;
            }}
            QPushButton#registerButton:disabled {{
                background: #BDBDBD;
                color: rgba(255, 255, 255, 0.7);
            }}
        ''')
        
        # Logo boyutunu güncelle
        logo_size = self.scaled_size(80)
        if hasattr(self, 'logo_label'):
            logo_pixmap = QPixmap('resources/icons/youtube.png')
            if not logo_pixmap.isNull():
                scaled_pixmap = logo_pixmap.scaled(
                    logo_size, logo_size,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.logo_label.setPixmap(scaled_pixmap)

    def mousePressEvent(self, event):
        """Pencereyi sürüklemek için tıklama pozisyonunu kaydet"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.parent.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        """Pencereyi sürükle"""
        if event.buttons() == Qt.LeftButton and self.dragging:
            self.parent.move(event.globalPos() - self.drag_position)
            event.accept()
            
    def mouseReleaseEvent(self, event):
        """Sürüklemeyi bitir"""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()
            
    def eventFilter(self, obj, event):
        """Enter tuşu ile kayıt olma ve input alanları için hover efekti"""
        if obj == self.confirm_password_input and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return and self.register_button.isEnabled():
                self.register()
                return True
        elif event.type() == QEvent.Enter:
            if obj in [self.username_input, self.email_input, self.password_input, self.confirm_password_input]:
                self.add_input_shadow(obj)
        elif event.type() == QEvent.Leave:
            if obj in [self.username_input, self.email_input, self.password_input, self.confirm_password_input]:
                self.remove_input_shadow(obj)
        return super().eventFilter(obj, event)
        
    def add_input_fields(self, layout):
        """Input alanlarını ekler"""
        input_fields = [
            ('Kullanıcı Adı', self.username_input, 'Kullanıcı adınızı girin'),
            ('E-posta', self.email_input, 'E-posta adresinizi girin'),
            ('Şifre', self.password_input, 'Şifrenizi girin'),
            ('Şifre Tekrar', self.confirm_password_input, 'Şifrenizi tekrar girin')
        ]
        
        for label_text, input_widget, placeholder in input_fields:
            container = QFrame()
            container_layout = QVBoxLayout(container)
            container_layout.setSpacing(6)
            container_layout.setContentsMargins(0, 0, 0, 0)
            
            # Label
            label = QLabel(label_text)
            label.setStyleSheet(f'''
                font-size: {self.scaled_size(14)}px;
                font-weight: bold;
                color: #37474F;
                font-family: "Segoe UI";
                margin-bottom: {self.scaled_size(4)}px;
                padding-left: {self.scaled_size(2)}px;
            ''')
            
            # Input widget ayarları
            input_widget.setPlaceholderText(placeholder)
            if input_widget in [self.password_input, self.confirm_password_input]:
                input_widget.setEchoMode(QLineEdit.Password)
            
            # Input boyutları ve stili
            input_height = self.scaled_size(45)
            input_widget.setFixedHeight(input_height)
            
            # Padding değerleri
            h_padding = self.scaled_size(15)
            v_padding = self.scaled_size(12)
            border_radius = self.scaled_size(10)
            font_size = self.scaled_size(14)
            placeholder_size = self.scaled_size(13)
            
            input_widget.setStyleSheet(f'''
                QLineEdit {{
                    padding: {v_padding}px {h_padding}px;
                    border: 2px solid #E0E0E0;
                    border-radius: {border_radius}px;
                    font-size: {font_size}px;
                    font-family: "Segoe UI";
                    background-color: #F5F5F5;
                    color: #424242;
                }}
                QLineEdit:hover {{
                    border-color: #90CAF9;
                    background-color: #FAFAFA;
                }}
                QLineEdit:focus {{
                    border-color: #2196F3;
                    background-color: #FFFFFF;
                    color: #1565C0;
                }}
                QLineEdit::placeholder {{
                    color: #9E9E9E;
                    font-size: {placeholder_size}px;
                }}
            ''')
            
            # Validasyon bağlantısı
            input_widget.textChanged.connect(self.validate_inputs)
            
            container_layout.addWidget(label)
            container_layout.addWidget(input_widget)
            layout.addWidget(container)

    def add_buttons(self, layout):
        """Butonları ekler"""
        # Kayıt butonu
        self.register_button = QPushButton('Kayıt Ol')
        self.register_button.setObjectName('registerButton')
        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.clicked.connect(self.register)
        self.register_button.setEnabled(False)
        self.register_button.setFixedSize(280, 45)
        self.register_button.setStyleSheet('''
            QPushButton#registerButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2196F3, stop:1 #1976D2);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 15px;
                font-weight: bold;
                font-family: "Segoe UI";
            }
            QPushButton#registerButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1E88E5, stop:1 #1565C0);
            }
            QPushButton#registerButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1976D2, stop:1 #0D47A1);
                padding-top: 2px;
            }
            QPushButton#registerButton:disabled {
                background: #BDBDBD;
                color: rgba(255, 255, 255, 0.7);
            }
        ''')
        
        # Giriş butonu
        self.login_button = QPushButton('Zaten hesabınız var mı? Giriş yapın')
        self.login_button.setObjectName('loginButton')
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self.show_login)
        self.login_button.setStyleSheet('''
            QPushButton#loginButton {
                background: transparent;
                color: #1976D2;
                border: none;
                font-size: 13px;
                font-family: "Segoe UI";
                padding: 5px;
            }
            QPushButton#loginButton:hover {
                color: #1565C0;
                text-decoration: underline;
            }
            QPushButton#loginButton:pressed {
                color: #0D47A1;
            }
        ''')
        
        layout.addWidget(self.register_button)
        layout.addWidget(self.login_button)

    def setup_animations(self):
        """Animasyonları hazırlar"""
        # Pozisyon animasyonu
        self.pos_anim = QPropertyAnimation(self.register_frame, b'pos')
        self.pos_anim.setDuration(800)
        self.pos_anim.setEasingCurve(QEasingCurve.OutBack)
        
        # Opaklık animasyonu
        self.opacity_effect = QGraphicsOpacityEffect(self.register_frame)
        self.register_frame.setGraphicsEffect(self.opacity_effect)
        self.opacity_anim = QPropertyAnimation(self.opacity_effect, b'opacity')
        self.opacity_anim.setDuration(800)
        self.opacity_anim.setStartValue(0)
        self.opacity_anim.setEndValue(1)
        self.opacity_anim.setEasingCurve(QEasingCurve.InOutQuad)

    def validate_inputs(self):
        """Giriş alanlarını kontrol eder"""
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        
        # Validasyon kuralları
        username_valid, username_error = validate_username(username)
        email_valid = validate_email(email)
        password_valid, password_error = validate_password(password)
        confirm_valid = password == confirm_password and len(confirm_password) > 0
        
        # Kayıt butonunu etkinleştir/devre dışı bırak
        is_valid = (username_valid and email_valid and 
                   password_valid and confirm_valid)
        
        self.register_button.setEnabled(is_valid)
        
        # Input stilleri güncelle
        input_fields = [
            (self.username_input, username_valid, username_error if not username_valid and username else None),
            (self.email_input, email_valid, "Geçersiz e-posta adresi" if not email_valid and email else None),
            (self.password_input, password_valid, password_error if not password_valid and password else None),
            (self.confirm_password_input, confirm_valid, "Şifreler eşleşmiyor" if not confirm_valid and confirm_password else None)
        ]
        
        for input_field, is_valid, error_text in input_fields:
            if input_field.text().strip():
                style = f'''
                    QLineEdit {{
                        padding: 14px 18px;
                        border: 2px solid {('#2196F3' if is_valid else '#EF5350')};
                        border-radius: 15px;
                        font-size: 15px;
                        font-family: "Segoe UI";
                        background-color: {('white' if is_valid else '#FFF3F3')};
                        color: {('#1565C0' if is_valid else '#D32F2F')};
                    }}
                    QLineEdit:hover {{
                        border-color: {('#1E88E5' if is_valid else '#E53935')};
                    }}
                    QLineEdit:focus {{
                        border-color: {('#1565C0' if is_valid else '#D32F2F')};
                        background-color: white;
                    }}
                '''
                input_field.setStyleSheet(style)
                
                if error_text:
                    input_field.setToolTip(error_text)
                else:
                    input_field.setToolTip("")
            else:
                self.remove_input_shadow(input_field)

    def register(self):
        """Kayıt işlemini gerçekleştirir"""
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        
        # Validasyon kontrolleri
        username_valid, username_error = validate_username(username)
        email_valid = validate_email(email)
        password_valid, password_error = validate_password(password)
        confirm_valid = password == confirm_password
        
        if not all([username, email, password, confirm_password]):
            self.show_error_message('Lütfen tüm alanları doldurun!')
            self.show_error_animation()
            return
            
        if not username_valid:
            self.show_error_message(username_error)
            self.show_error_animation()
            return
            
        if not email_valid:
            self.show_error_message('Geçerli bir e-posta adresi girin!')
            self.show_error_animation()
            return
            
        if not password_valid:
            self.show_error_message(password_error)
            self.show_error_animation()
            return
            
        if not confirm_valid:
            self.show_error_message('Şifreler eşleşmiyor!')
            self.show_error_animation()
            return
            
        # Kayıt butonunu devre dışı bırak ve yükleniyor göster
        self.register_button.setEnabled(False)
        self.register_button.setText('Kayıt yapılıyor...')
        QApplication.processEvents()
        
        try:
            if self.parent.register(username, email, password):
                self.show_success_message()
                self.show_login()
            else:
                self.show_error_animation()
                self.show_error_message('Bu kullanıcı adı veya e-posta zaten kullanımda!')
        except Exception as e:
            self.show_error_message(f'Kayıt olurken bir hata oluştu: {str(e)}')
            self.show_error_animation()
        finally:
            # Kayıt butonunu tekrar etkinleştir
            self.register_button.setText('Kayıt Ol')
            self.register_button.setEnabled(True)

    def show_login(self):
        """Giriş ekranını gösterir"""
        # Input alanlarını temizle
        self.username_input.clear()
        self.email_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
        
        # Giriş ekranını göster
        if self.parent:
            # Önce bu ekranı gizle
            self.hide()
            
            # Giriş ekranını göster
            login_view = self.parent.show_login()
            if login_view:
                # Pencere boyutunu ayarla
                login_view.adjustSize()
                
                # Ana pencere merkezini al
                parent_center = self.parent.geometry().center()
                
                # Pencereyi ana pencere merkezine göre konumlandır
                geometry = login_view.geometry()
                geometry.moveCenter(parent_center)
                login_view.setGeometry(geometry)

    def show_error_animation(self):
        """Hata durumunda sallama animasyonu"""
        # Sallama animasyonu
        pos_anim = QPropertyAnimation(self.register_frame, b'pos')
        pos_anim.setDuration(50)
        pos_anim.setLoopCount(6)
        
        original_pos = self.register_frame.pos()
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
        
        pos_anim.start()

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
        """Başarılı kayıt mesajı"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText('Kayıt başarıyla tamamlandı!')
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

    def showEvent(self, event):
        """Widget gösterildiğinde animasyonları başlatır"""
        super().showEvent(event)
        QTimer.singleShot(100, self.start_animations)

    def start_animations(self):
        """Tüm animasyonları başlatır"""
        # Pozisyon animasyonu
        current_pos = self.register_frame.pos()
        start_pos = current_pos + QPoint(0, 50)
        self.pos_anim.setStartValue(start_pos)
        self.pos_anim.setEndValue(current_pos)
        
        # Animasyonları başlat
        self.pos_anim.start()
        self.opacity_anim.start()

    def hideEvent(self, event):
        """Widget gizlendiğinde çağrılır"""
        super().hideEvent(event)
        # Gizlendiğinde tüm input alanlarını temizle
        self.username_input.clear()
        self.email_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()

    def resizeEvent(self, event):
        """Pencere boyutu değiştiğinde çağrılır"""
        super().resizeEvent(event)
        
        # Ölçekleme faktörünü güncelle
        self.calculate_scale_factor()
        
        # Register frame genişliğini güncelle
        available_width = self.width() - self.scaled_size(80)
        frame_width = min(self.scaled_size(800), max(self.scaled_size(400), int(available_width * 0.8)))
        self.register_frame.setFixedWidth(frame_width)
        
        # Register frame'i ortala
        frame_x = (self.width() - self.register_frame.width()) // 2
        frame_y = (self.height() - self.register_frame.height()) // 2
        self.register_frame.move(frame_x, frame_y)
        
        # Tüm stilleri güncelle
        self.update_styles()
        
        # Layout boşluklarını güncelle
        self.update_layout_spacing()

    def update_layout_spacing(self):
        """Layout boşluklarını günceller"""
        # Ana layout
        main_layout = self.layout()
        main_layout.setContentsMargins(
            self.scaled_size(40),
            self.scaled_size(40),
            self.scaled_size(40),
            self.scaled_size(40)
        )
        
        # Register frame layout
        register_layout = self.register_frame.layout()
        register_layout.setSpacing(self.scaled_size(30))
        register_layout.setContentsMargins(
            self.scaled_size(50),
            self.scaled_size(50),
            self.scaled_size(50),
            self.scaled_size(50)
        )
        
        # Form container layout
        form_container = self.findChild(QFrame, "form_container")
        if form_container:
            form_layout = form_container.layout()
            form_layout.setSpacing(self.scaled_size(25))
            form_layout.setContentsMargins(
                self.scaled_size(20),
                0,
                self.scaled_size(20),
                0
            )
        
        # Buttons container layout
        buttons_container = self.findChild(QFrame, "buttons_container")
        if buttons_container:
            buttons_layout = buttons_container.layout()
            buttons_layout.setSpacing(self.scaled_size(15))
            buttons_layout.setContentsMargins(
                0,
                self.scaled_size(30),
                0,
                0
            )

    def add_input_shadow(self, widget):
        """Input alanına hover gölgesi ekle"""
        # Padding değerleri
        h_padding = self.scaled_size(15)
        v_padding = self.scaled_size(12)
        border_radius = self.scaled_size(10)
        font_size = self.scaled_size(14)
        placeholder_size = self.scaled_size(13)
        
        widget.setStyleSheet(f'''
            QLineEdit {{
                padding: {v_padding}px {h_padding}px;
                border: 2px solid #90CAF9;
                border-radius: {border_radius}px;
                font-size: {font_size}px;
                font-family: "Segoe UI";
                background-color: #FAFAFA;
                color: #1565C0;
            }}
            QLineEdit:hover {{
                border-color: #64B5F6;
                background-color: #FFFFFF;
            }}
            QLineEdit:focus {{
                border-color: #42A5F5;
                background-color: #FFFFFF;
            }}
            QLineEdit::placeholder {{
                color: #90A4AE;
                font-size: {placeholder_size}px;
            }}
        ''')

    def remove_input_shadow(self, widget):
        """Input alanından hover gölgesini kaldır"""
        # Padding değerleri
        h_padding = self.scaled_size(15)
        v_padding = self.scaled_size(12)
        border_radius = self.scaled_size(10)
        font_size = self.scaled_size(14)
        placeholder_size = self.scaled_size(13)
        
        widget.setStyleSheet(f'''
            QLineEdit {{
                padding: {v_padding}px {h_padding}px;
                border: 2px solid #E0E0E0;
                border-radius: {border_radius}px;
                font-size: {font_size}px;
                font-family: "Segoe UI";
                background-color: #F5F5F5;
                color: #424242;
            }}
            QLineEdit:hover {{
                border-color: #90CAF9;
                background-color: #FAFAFA;
            }}
            QLineEdit:focus {{
                border-color: #2196F3;
                background-color: #FFFFFF;
                color: #1565C0;
            }}
            QLineEdit::placeholder {{
                color: #9E9E9E;
                font-size: {placeholder_size}px;
            }}
        ''')

    def init_ui(self):
        """Kayıt ekranı arayüzünü oluşturur"""
        # Ana layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Register frame
        self.register_frame = QFrame()
        self.register_frame.setObjectName('registerFrame')
        self.register_frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.register_frame.setFixedWidth(450)
        
        # Gölge efekti ekle
        shadow = QGraphicsDropShadowEffect(self.register_frame)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 4)
        self.register_frame.setGraphicsEffect(shadow)
        
        self.register_frame.setStyleSheet('''
            QFrame#registerFrame {
                background: rgba(255, 255, 255, 0.98);
                border-radius: 25px;
                border: 1px solid rgba(255, 255, 255, 0.5);
            }
        ''')
        
        # Register frame layout
        register_layout = QVBoxLayout(self.register_frame)
        register_layout.setSpacing(25)
        register_layout.setContentsMargins(40, 40, 40, 40)
        
        # Logo ve başlık container'ı
        header_container = QFrame()
        header_layout = QVBoxLayout(header_container)
        header_layout.setSpacing(15)
        header_layout.setContentsMargins(0, 0, 0, 20)
        header_layout.setAlignment(Qt.AlignCenter)
        
        # Logo
        self.logo_label = QLabel()
        logo_pixmap = QPixmap('resources/icons/youtube.png')
        if not logo_pixmap.isNull():
            scaled_pixmap = logo_pixmap.scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(scaled_pixmap)
            self.logo_label.setAlignment(Qt.AlignCenter)
        
        # Başlık ve alt başlık oluştur
        self.title_label = QLabel('Hesap Oluştur')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('''
            font-size: 26px;
            color: #1565C0;
            font-weight: bold;
            font-family: "Segoe UI";
            margin-top: 10px;
        ''')
        
        self.subtitle_label = QLabel('YouTube İndirme\nUygulamasına Hoş Geldiniz')
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setStyleSheet('''
            font-size: 15px;
            color: #546E7A;
            font-family: "Segoe UI";
            margin-bottom: 10px;
        ''')
        
        # Başlık ve alt başlık ekle
        header_layout.addWidget(self.logo_label)
        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.subtitle_label)
        
        # Form container
        form_container = QFrame()
        form_container.setObjectName("form_container")
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(10, 0, 10, 0)
        
        # Input alanlarını ekle
        self.add_input_fields(form_layout)
        
        # Butonlar container'ı
        buttons_container = QFrame()
        buttons_container.setObjectName("buttons_container")
        buttons_layout = QVBoxLayout(buttons_container)
        buttons_layout.setSpacing(12)
        buttons_layout.setContentsMargins(0, 20, 0, 0)
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        # Butonları ekle
        self.add_buttons(buttons_layout)
        
        # Layout'ları birleştir
        register_layout.addWidget(header_container)
        register_layout.addWidget(form_container, 1)
        register_layout.addWidget(buttons_container)
        
        # Ana layout'a register frame'i ekle
        main_layout.addWidget(self.register_frame, alignment=Qt.AlignCenter) 