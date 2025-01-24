import os
import shutil
from pathlib import Path

def ensure_dir(directory):
    """Dizinin var olduğundan emin olur"""
    Path(directory).mkdir(parents=True, exist_ok=True)

def get_safe_filename(filename):
    """Güvenli dosya adı oluşturur"""
    # Geçersiz karakterleri kaldır
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    
    # Boşlukları alt çizgi ile değiştir
    filename = filename.replace(' ', '_')
    
    # Uzunluğu sınırla
    max_length = 255 - len('.mp4')  # En uzun uzantı için yer bırak
    if len(filename) > max_length:
        filename = filename[:max_length]
    
    return filename

def get_file_size(file_path):
    """Dosya boyutunu okunabilir formatta döndürür"""
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def delete_file(file_path):
    """Dosyayı güvenli bir şekilde siler"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        print(f"Dosya silme hatası: {e}")
    return False

def move_file(src, dst):
    """Dosyayı taşır"""
    try:
        shutil.move(src, dst)
        return True
    except Exception as e:
        print(f"Dosya taşıma hatası: {e}")
        return False

def get_available_filename(directory, filename):
    """Benzersiz dosya adı oluşturur"""
    base, ext = os.path.splitext(filename)
    counter = 1
    result = filename
    
    while os.path.exists(os.path.join(directory, result)):
        result = f"{base}_{counter}{ext}"
        counter += 1
    
    return result 