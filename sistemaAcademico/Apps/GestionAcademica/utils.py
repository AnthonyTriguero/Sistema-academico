"""
Utilidades de seguridad para el sistema académico.
"""
import hashlib
import logging
from django.contrib.auth.hashers import make_password, check_password

logger = logging.getLogger(__name__)


def hash_password(raw_password):
    """
    Genera un hash seguro de la contraseña usando PBKDF2 de Django.
    Reemplaza el uso inseguro de SHA1.
    """
    return make_password(raw_password)


def verify_password(raw_password, hashed_password):
    """
    Verifica una contraseña contra su hash.
    Soporta tanto el nuevo formato PBKDF2 como el legacy SHA1
    para permitir migración gradual.
    """
    # Intentar verificar con el hasher de Django (PBKDF2)
    if check_password(raw_password, hashed_password):
        return True

    # Fallback: verificar contra SHA1 legacy (para usuarios no migrados)
    h = hashlib.new("sha1")
    h.update(str.encode(raw_password))
    if h.hexdigest() == hashed_password:
        logger.warning("Usuario autenticado con SHA1 legacy. Necesita migración de contraseña.")
        return True

    return False


def needs_password_migration(hashed_password):
    """
    Detecta si una contraseña usa el formato SHA1 legacy
    y necesita ser migrada a PBKDF2.
    """
    # Los hashes SHA1 son hexadecimales de 40 caracteres
    # Los hashes PBKDF2 de Django empiezan con 'pbkdf2_sha256$'
    return (
        len(hashed_password) == 40
        and all(c in '0123456789abcdef' for c in hashed_password)
    )
