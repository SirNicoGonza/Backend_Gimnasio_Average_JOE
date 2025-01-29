import sys
import os
import pytest

# Agregar la carpeta raíz del proyecto al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import DatabaseConnection
from tests.utils import cleanup

@pytest.fixture(scope="module")
def db_connection():
    """Inicializa la base de datos para las pruebas."""
    db = DatabaseConnection.get_connection()
    yield db
    DatabaseConnection.close_connection()

@pytest.fixture(autouse=True)
def setup(db_connection):
    """Limpia la base de datos antes y después de cada prueba."""
    with db_connection as conn:
        cleanup(conn)  # Restablece la BD de prueba
    yield
    with db_connection as conn:
        cleanup(conn)
