import pytest
import sys
import os

# Agregar la carpeta raíz del proyecto al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import DatabaseConnection
from models.pago_model import PagoModel
from tests.utils import cleanup

@pytest.fixture
def test_user(db_connection):
    """Crea un usuario de prueba antes de cada test y lo elimina después."""
    query = """
        INSERT INTO users (firstname, lastname, email, passwords)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE email=email
    """
    params = ("Pago", "Test", "testpago@example.com", "hashedpassword")
    DatabaseConnection.execute_query(query, params)

    user_id_tuple = DatabaseConnection.fetch_one("SELECT id_user FROM users WHERE email = %s", ("testpago@example.com",))
    user_id = user_id_tuple[0] if user_id_tuple else None

    # Insertar usuario en la tabla 'socios'
    query = "INSERT INTO socios (id_user, plan_id, activo, dias_habilitado, dias_gracia) VALUES (%s, NULL, 0, 0, 0)"
    DatabaseConnection.execute_query(query, (user_id,))

    # Activar el usuario como socio con un plan
    PagoModel.activar_socio(user_id, 30, 5)

    yield user_id  # Devuelve el ID del usuario para usarlo en los tests

    # Eliminar usuario después de la prueba
    DatabaseConnection.execute_query("DELETE FROM socios WHERE id_user = %s", (user_id,))
    DatabaseConnection.execute_query("DELETE FROM users WHERE id_user = %s", (user_id,))


def test_vencimiento_cuota(test_user):
    """Verifica que un socio se inhabilite cuando la cuota vence."""
    query = "SELECT id_socio FROM socios WHERE id_user = %s"
    id_socio_tuple = DatabaseConnection.fetch_one(query, (test_user,))
    id_socio = id_socio_tuple[0] if id_socio_tuple else None

    # Registrar un pago
    PagoModel.registrar_pago_plan(id_socio, None)

    # Simular el paso del tiempo restando días habilitados hasta 0
    query = "UPDATE socios SET dias_habilitado = 0, dias_gracia = 0 WHERE id_user = %s"
    DatabaseConnection.execute_query(query, (test_user,))

    # Ejecutar la lógica de vencimiento
    resultado = PagoModel.verificar_vencimiento()

    # Verificar si el usuario se ha desactivado
    query = "SELECT activo FROM socios WHERE id_user = %s"
    socio_activo_tuple = DatabaseConnection.fetch_one(query, (test_user,))
    socio_activo = socio_activo_tuple[0] if socio_activo_tuple else None

    assert socio_activo == 0, "El usuario aún está activo después de que la cuota venciera"
