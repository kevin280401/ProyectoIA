import re
from urllib.parse import urlparse
from datetime import datetime, timedelta
import jwt

# Validación básica de URLs
def is_valid_url(url):
    """
    Verifica si una URL tiene un formato válido.
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # Protocolo http, https o ftp
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # Dominio
        r'localhost|'  # Localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # IP (v4)
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # IP (v6)
        r'(?::\d+)?'  # Puerto opcional
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    
    return re.match(regex, url) is not None

# Parsear el dominio de una URL
def get_domain_from_url(url):
    """
    Extrae el dominio de una URL.
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc

# Formatear fecha en un formato legible
def format_date(date, format="%Y-%m-%d %H:%M:%S"):
    """
    Formatea una fecha en una cadena legible.
    """
    return date.strftime(format)

# Generar un token JWT (por ejemplo, para autenticación o enlaces compartidos)
def generate_jwt_token(data, secret, expiration_minutes=30):
    """
    Genera un token JWT con un tiempo de expiración.
    """
    expiration = datetime.utcnow() + timedelta(minutes=expiration_minutes)
    data.update({"exp": expiration})
    return jwt.encode(data, secret, algorithm="HS256")

# Verificar un token JWT
def verify_jwt_token(token, secret):
    """
    Verifica la validez de un token JWT.
    """
    try:
        decoded_token = jwt.decode(token, secret, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

# Validar si una cadena de texto está vacía o es nula
def is_empty_string(value):
    """
    Verifica si una cadena de texto es vacía o None.
    """
    return value is None or value.strip() == ""

# Función auxiliar para truncar texto largo
def truncate_text(text, max_length=100):
    """
    Trunca un texto a la longitud especificada y añade '...' al final si excede.
    """
    if len(text) > max_length:
        return text[:max_length] + '...'
    return text
