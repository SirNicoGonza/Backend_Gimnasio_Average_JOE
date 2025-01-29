import pytest
import sys
import os

# Agregar la carpeta raíz del proyecto al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import DatabaseConnection
from models.user_model import UserModel
from tests.utils import cleanup  # Función para limpiar la BD después de cada test

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

    yield user_id  # Devuelve el ID del usuario para usarlo en los tests

    # Eliminar usuario después de la prueba
    DatabaseConnection.execute_query("DELETE FROM socios WHERE id_user = %s", (user_id,))
    DatabaseConnection.execute_query("DELETE FROM users WHERE id_user = %s", (user_id,))


@pytest.mark.parametrize(
    "user_id, expected_message",
    [
        (None, "El usuario no existe"),  # Usuario no existente
        (-1, "El usuario no existe"),  # ID inválido
        ("string", "El usuario no existe"),  # Tipo de dato incorrecto
    ]
)
def test_asignar_socio_errores(user_id, expected_message):
    """Prueba que la asignación de socio maneja errores correctamente."""
    resultado = UserModel.asignar_socio(user_id)
    assert resultado == expected_message, f"Error en test con user_id={user_id}"


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


def test_asignar_socio_ya_existente(test_user):
    """Prueba que no se pueda volver a asignar un usuario como socio si ya lo es."""
    resultado_1 = UserModel.asignar_socio(test_user)
    assert resultado_1, "El usuario no fue asignado correctamente la primera vez."

    # Intentamos asignarlo nuevamente
    resultado_2 = UserModel.asignar_socio(test_user)

    # La segunda asignación debería fallar o devolver un mensaje de advertencia
    assert resultado_2 == "El usuario ya es socio", "El sistema debería evitar la doble asignación."


def test_socio_se_guarda_correctamente(test_user):
    """Prueba de integración: Verifica que el usuario se guarde correctamente en la base de datos después de ser asignado como socio."""
    UserModel.asignar_socio(test_user)

    query = "SELECT id_user FROM socios WHERE id_user = %s"
    params = (test_user,)
    resultado = DatabaseConnection.fetch_one(query, params)

    assert resultado is not None, "El usuario no fue guardado en la tabla socios"
    assert resultado[0] == test_user, "El ID del usuario guardado en socios no coincide"


def test_limpieza_de_pruebas(test_user):
    """Prueba de integración: Verifica que los datos de prueba sean eliminados correctamente después del test."""
    UserModel.asignar_socio(test_user)

    # Eliminamos el usuario de la tabla socios y users (simulando la limpieza post-test)
    DatabaseConnection.execute_query("DELETE FROM socios WHERE id_user = %s", (test_user,))
    DatabaseConnection.execute_query("DELETE FROM users WHERE id_user = %s", (test_user,))

    # Verificamos que el usuario ya no esté en la tabla `socios`
    query_socio = "SELECT id_user FROM socios WHERE id_user = %s"
    query_user = "SELECT id_user FROM users WHERE id_user = %s"

    resultado_socio = DatabaseConnection.fetch_one(query_socio, (test_user,))
    resultado_user = DatabaseConnection.fetch_one(query_user, (test_user,))

    assert resultado_socio is None, "El usuario sigue presente en la tabla socios después de la limpieza"
    assert resultado_user is None, "El usuario sigue presente en la tabla users después de la limpieza"
