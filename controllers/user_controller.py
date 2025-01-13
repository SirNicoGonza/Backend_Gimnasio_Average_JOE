from flask import jsonify
import bcrypt
from models.user_model import UserModel

class UserController:
    """ Clase controlador de Usarios
    """

    @staticmethod
    def registrar_nuevo(data):
        """ Metodo estatico para crear un nuevo usuario. Recibe un json y de alli toma los datos.
        """
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        email = data.get('email')
        password = data.get('password')

        #Se verifica si los datos estan completos
        if not nombre or not apellido or not email or not password:
            return jsonify({'mensaje': 'Faltan datos'}), 400
        
        #aqui va para verificar si ya existe un usuario

        #Se encripta el password
        password_bytes = password.encode('utf-8')
        hash_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

        # Verificar la contraseña
        #bcrypt.checkpw(password, hashed_password)  # Devuelve True si coincide

        #Se crea el userario
        if UserModel.crear_user(nombre, apellido, email, hash_password):
            return jsonify({'mensaje': 'Usuario creado exitosamente'}), 201