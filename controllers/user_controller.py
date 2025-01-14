from flask import jsonify
import bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta
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

        #Se crea el userario
        if UserModel.crear_user(nombre, apellido, email, hash_password):
            return jsonify({'mensaje': 'Usuario creado exitosamente'}), 201
        
    @staticmethod
    def login(data):
        """ Metodo estatico para buscar un usuario en la base, verifica que las credenciales seas las correctas
            si lo es, inicia sesion.
        """
        email= data.get('email')
        password= data.get('password')

        user= UserModel.buscar_user(email)

        #Se hace la verificacion de la contraseña
        if not bcrypt.checkpw(password.encode('utf-8'), user['passwords'].encode('utf-8')):
            return {"error": "Contraseña incorrecta"}, 401
        
        token = create_access_token(identity=user['id_user'], expires_delta=timedelta(hours=12))
        return jsonify({'token': token}), 200