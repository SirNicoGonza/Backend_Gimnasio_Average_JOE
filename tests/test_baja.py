import pytest
import sys
import os

# Agregar la carpeta raíz del proyecto al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import DatabaseConnection
from models.user_model import UserModel
from tests.utils import cleanup

@pytest.fixture(scope="module")
def db_connection():
    """Fixture para inicializar la base de datos de prueba."""
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


@pytest.fixture
def test_user(db_connection):
    """Crea un usuario de prueba antes de cada test y lo elimina después."""
    query = """
        INSERT INTO users (firstname, lastname, email, passwords)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE email=email
    """
    params = ("Test", "User", "test@example.com", "hashedpassword")
    
    DatabaseConnection.execute_query(query, params)
    user_id_tuple = DatabaseConnection.fetch_one("SELECT id_user FROM users WHERE email = %s", ("test@example.com",))
    user_id = user_id_tuple[0] if user_id_tuple else None

    # Insertar usuario en la tabla 'socios'
    query = "INSERT INTO socios (id_user, plan_id, activo) VALUES (%s, NULL, 0)"
    DatabaseConnection.execute_query(query, (user_id,))

    yield user_id  # Devuelve el ID del usuario para usarlo en los tests

    # Eliminar usuario después de la prueba
    DatabaseConnection.execute_query("DELETE FROM socios WHERE id_user = %s", (user_id,))
    DatabaseConnection.execute_query("DELETE FROM users WHERE id_user = %s", (user_id,))


def test_eliminar_socio(test_user):
    """Prueba que un socio pueda darse de baja correctamente."""
    resultado = UserModel.eliminar_socio(test_user)
    assert resultado.get("success"), "El socio no fue eliminado correctamente"

    query = "SELECT * FROM socios WHERE id_user = %s"
    params = (test_user,)
    socio = DatabaseConnection.fetch_one(query, params)

    assert socio is None, "El socio todavía existe en la base de datos"
