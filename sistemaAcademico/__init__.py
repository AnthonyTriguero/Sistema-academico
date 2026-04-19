import pymysql
from pymysql.converters import conversions
from pymysql.constants import FIELD_TYPE
import datetime

# Instalar PyMySQL como MySQLdb
pymysql.install_as_MySQLdb()

# Configurar conversores personalizados para manejar datetime correctamente
def convert_datetime(obj):
    """Convierte strings de datetime a objetos datetime de Python."""
    if obj is None:
        return None
    if isinstance(obj, datetime.datetime):
        return obj
    if isinstance(obj, str):
        # Manejar valores inválidos de MySQL
        if obj in ('0000-00-00', '0000-00-00 00:00:00', '0000-00-00 00:00:00.000000'):
            return None
        
        # Intentar parsear diferentes formatos de datetime
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M:%S.%f',
            '%Y-%m-%d',
        ]
        for fmt in formats:
            try:
                return datetime.datetime.strptime(obj, fmt)
            except ValueError:
                continue
    return obj

def convert_date(obj):
    """Convierte strings de date a objetos date de Python."""
    if obj is None:
        return None
    if isinstance(obj, datetime.date):
        return obj
    if isinstance(obj, str):
        # Manejar valores inválidos de MySQL
        if obj in ('0000-00-00', '0000-00-00 00:00:00', '0000-00-00 00:00:00.000000'):
            return None
        
        try:
            return datetime.datetime.strptime(obj, '%Y-%m-%d').date()
        except ValueError:
            pass
    return obj

# Crear copia de conversiones por defecto
custom_conversions = conversions.copy()

# Agregar conversores personalizados para tipos de fecha/hora
custom_conversions[FIELD_TYPE.DATETIME] = convert_datetime
custom_conversions[FIELD_TYPE.TIMESTAMP] = convert_datetime
custom_conversions[FIELD_TYPE.DATE] = convert_date

# Aplicar conversores personalizados globalmente
pymysql.converters.conversions = custom_conversions
