from datetime import timedelta, date
from decimal import Decimal

def convertir_valores_para_json(obj):
    """
    Funcion que convierte los datos de tipo DECIMAL, TIME y TIMEDELTA a str para poder tranformar el objeto obj 
    a JSON
    """
    if isinstance(obj, (tuple, list)):
        # Si es una tupla o lista, convertir cada elemento
        return [convertir_valores_para_json(item) for item in obj]
    elif isinstance(obj, timedelta):
        return str(obj)  # Convertir timedelta a cadena
    elif isinstance(obj, date):
        return obj.isoformat()  # Convertir date a cadena (formato YYYY-MM-DD)
    elif isinstance(obj, Decimal):
        return float(obj)  # Convertir Decimal a float
    else:
        # Si es un tipo básico (int, float, str, bool), devolverlo tal cual
        return obj
    