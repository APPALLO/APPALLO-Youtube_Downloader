import re

def validate_email(email):
    """E-posta adresini doğrular"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password):
    """Şifre karmaşıklığını kontrol eder"""
    if len(password) < 8:
        return False, "Şifre en az 8 karakter olmalıdır"
    
    if not any(c.isupper() for c in password):
        return False, "Şifre en az bir büyük harf içermelidir"
    
    if not any(c.islower() for c in password):
        return False, "Şifre en az bir küçük harf içermelidir"
    
    if not any(c.isdigit() for c in password):
        return False, "Şifre en az bir rakam içermelidir"
    
    return True, ""

def validate_username(username):
    """Kullanıcı adını doğrular"""
    if len(username) < 3:
        return False, "Kullanıcı adı en az 3 karakter olmalıdır"
    
    if not username.isalnum():
        return False, "Kullanıcı adı sadece harf ve rakam içermelidir"
    
    return True, ""

def validate_youtube_url(url):
    """YouTube URL'sini doğrular"""
    patterns = [
        r'^https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+',
        r'^https?://(?:www\.)?youtube\.com/v/[\w-]+',
        r'^https?://youtu\.be/[\w-]+',
        r'^https?://(?:www\.)?youtube\.com/embed/[\w-]+'
    ]
    
    return any(bool(re.match(pattern, url)) for pattern in patterns) 