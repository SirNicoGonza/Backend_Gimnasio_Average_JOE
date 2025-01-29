import sys
import os

# Agregar la carpeta raíz del proyecto al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import DatabaseConnection
from models.user_model import UserModel
import pytest

@pytest.fixture
def db_connection():
    """Fixture para manejar la conexión a la base de datos."""
    db = DatabaseConnection.get_connection()
    yield db
    DatabaseConnection.close_connection()

@pytest.fixture
def test_user(db_connection):
    """Fixture para crear un usuario de prueba antes de cada test."""
    query = """
        INSERT INTO users (firstname, lastname, email, passwords)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE email=email
    """
    params = ("Test", "User", "test@example.com", "hashedpassword")
    DatabaseConnection.execute_query(query, params)
    user_id_tuple = DatabaseConnection.fetch_one("SELECT id_user FROM users WHERE email = %s", ("test@example.com",))
    user_id = user_id_tuple[0] if user_id_tuple else None
    yield user_id
    DatabaseConnection.execute_query("DELETE FROM socios WHERE id_user = %s", (user_id,))
    DatabaseConnection.execute_query("DELETE FROM users WHERE id_user = %s", (user_id,))


def test_asignar_socio_exitoso(test_user):
    """Prueba que un usuario existente pueda ser asignado como socio correctamente."""
    resultado = UserModel.asignar_socio(test_user)
    assert resultado, "El usuario no fue asignado como socio correctamente"
    
    query = "SELECT activo FROM socios WHERE id_user = %s"
    params = (test_user,)
    estado_tuple = DatabaseConnection.fetch_one(query, params)
    estado = estado_tuple[0] if estado_tuple else None
    
    assert estado is not None, "El usuario no se encuentra en la tabla socios"
    assert estado == 0, "El usuario no debería estar activo al asignarlo"
