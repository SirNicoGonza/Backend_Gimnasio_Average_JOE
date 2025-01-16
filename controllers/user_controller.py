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
        """ Método estático para crear un nuevo usuario con el rol por defecto 'socio'. """
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'socio')  # Asignar 'socio' como rol por defecto

        # Verificar si los datos están completos
        if not nombre or not apellido or not email or not password:
            return jsonify({'mensaje': 'Faltan datos'}), 400

        # Validar si el rol es permitido
        if role not in ['empleado', 'socio']:
            return jsonify({'mensaje': 'Rol inválido. Debe ser "empleado" o "socio".'}), 400

        # Verificar si el email ya está registrado
        if UserModel.buscar_user(email):
            return jsonify({'mensaje': 'El email ya está registrado'}), 400

        # Encriptar la contraseña
        password_bytes = password.encode('utf-8')
        hash_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

        # Crear el usuario en la base de datos
        if not UserModel.crear_user(nombre, apellido, email, hash_password):
            return jsonify({'mensaje': 'Error al crear el usuario'}), 500

        # Asignar el rol al usuario
        user = UserModel.buscar_user(email)
        user_id = user['id_user']

        if role == 'empleado':
            if not UserModel.asignar_empleado(user_id):
                return jsonify({'mensaje': 'Error al asignar rol de empleado'}), 500
        elif role == 'socio':
            if not UserModel.asignar_socio(user_id):
                return jsonify({'mensaje': 'Error al asignar rol de socio'}), 500

        return jsonify({'mensaje': 'Usuario creado exitosamente con rol asignado'}), 201

        
    @staticmethod
    def login(data):
        """Método estático para autenticar un usuario y devolver su token y rol."""
        email = data.get('email')
        password = data.get('password')

        # Buscar el usuario por email
        user = UserModel.buscar_user(email)

        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Verificar la contraseña
        if not bcrypt.checkpw(password.encode('utf-8'), user['passwords'].encode('utf-8')):
            return jsonify({"error": "Contraseña incorrecta"}), 401

        # Crear el token
        token = create_access_token(identity=user['id_user'], expires_delta=timedelta(hours=12))

        # Determinar el rol del usuario
        if UserModel.es_empleado(user['id_user']):
            role = "empleado"
        elif UserModel.es_socio(user['id_user']):
            role = "socio"
        else:
            role = "desconocido"  # En caso de que no sea ni empleado ni socio

        # Respuesta
        return jsonify({
            "token": token,
            "role": role
        }), 200
    
    @staticmethod
    def obtener_profile(user_id):
        """ Método para obtener el perfil de un usuario por su ID. """
        user = UserModel.buscar_user_por_id(user_id)

        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Verificar si el usuario es un empleado (profesor)
        if UserModel.es_empleado(user_id):
            profile = {
                "id_user": user['id_user'],
                "firstname": user['firstname'],
                "lastname": user['lastname'],
                "email": user['email'],
                "role": "empleado",  # Rol de empleado
                "gym_asignado": UserModel.obtener_gym_asignado(user_id)
            }
        # Verificar si el usuario es un socio
        elif UserModel.es_socio(user_id):
            profile = {
                "id_user": user['id_user'],
                "firstname": user['firstname'],
                "lastname": user['lastname'],
                "email": user['email'],
                "role": "socio",  # Rol de socio
                "plan": UserModel.obtener_plan_socio(user_id),
                "activo": UserModel.obtener_estado_socio(user_id)
            }
        else:
            return jsonify({"error": "Rol desconocido"}), 400  # En caso de que no sea ni socio ni empleado

        return jsonify({"profile": profile}), 200
