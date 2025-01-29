import unittest
import sys
import os

# Aseguramos que la raíz del proyecto está en el PATH de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import DatabaseConnection
from models.pago_model import PagoModel

class TestGestionCuota(unittest.TestCase):
    """ Test para verificar la gestión del vencimiento de la cuota """
    
    def setUp(self):
        """ Configuración antes de cada test """
        self.db = DatabaseConnection.get_connection()
        self.cursor = self.db.cursor()

        # Crear un usuario de prueba
        self.test_email = "testpago@example.com"
        self.test_user_id = None

        self.cursor.execute("""
            INSERT INTO users (firstname, lastname, email, passwords)
            VALUES ('Pago', 'Test', %s, 'hashedpassword')
            ON DUPLICATE KEY UPDATE email=email
        """, (self.test_email,))
        self.db.commit()

        # Obtener el ID del usuario
        self.cursor.execute("SELECT id_user FROM users WHERE email = %s", (self.test_email,))
        self.test_user_id = self.cursor.fetchone()[0]

        # 🔹 Insertar el usuario en la tabla 'socios' antes de activarlo
        self.cursor.execute("INSERT INTO socios (id_user, plan_id, activo, dias_habilitado, dias_gracia) VALUES (%s, NULL, 0, 0, 0)", (self.test_user_id,))
        self.db.commit()

        # Activar el usuario como socio
        PagoModel.activar_socio(self.test_user_id, 30, 5)

        # Verificar que el usuario se creó correctamente
        self.cursor.execute("SELECT * FROM socios WHERE id_user = %s", (self.test_user_id,))
        print("Datos del socio en la BD después de insertarlo:", self.cursor.fetchone())

    def test_vencimiento_cuota(self):
        """ Verifica que un socio se inhabilite cuando la cuota vence """

        # Obtener id_socio para registrar el pago correctamente
        self.cursor.execute("SELECT id_socio FROM socios WHERE id_user = %s", (self.test_user_id,))
        id_socio = self.cursor.fetchone()[0]

        # Registrar un pago para activar la lógica de vencimiento
        PagoModel.registrar_pago_plan(id_socio, None)

        # Imprimir estado antes de la verificación de vencimiento
        self.cursor.execute("SELECT activo FROM socios WHERE id_user = %s", (self.test_user_id,))
        print("Estado antes de verificar vencimiento:", self.cursor.fetchone())

        # Simular el paso del tiempo restando días habilitados hasta 0
        self.cursor.execute("UPDATE socios SET dias_habilitado = 0, dias_gracia = 0 WHERE id_user = %s", (self.test_user_id,))
        self.db.commit()

        # Ejecutar la lógica de vencimiento y ver el resultado
        resultado = PagoModel.verificar_vencimiento()
        print("Resultado de verificar_vencimiento:", resultado)

        # Verificar si el usuario se ha desactivado
        self.cursor.execute("SELECT activo FROM socios WHERE id_user = %s", (self.test_user_id,))
        socio_activo = self.cursor.fetchone()
        print("Estado después de verificar vencimiento:", socio_activo)
        self.assertEqual(socio_activo[0], 0, "El usuario aún está activo después de que la cuota venciera")

    def tearDown(self):
        """ Limpieza después de cada test """
        self.cursor.execute("DELETE FROM socios WHERE id_user = %s", (self.test_user_id,))
        self.cursor.execute("DELETE FROM users WHERE id_user = %s", (self.test_user_id,))
        self.db.commit()
        self.cursor.close()

if __name__ == "__main__":
    unittest.main()
