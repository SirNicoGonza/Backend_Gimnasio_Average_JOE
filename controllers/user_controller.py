from flask import jsonify
import bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import timedelta
from models.user_model import UserModel

class UserController:
    """ Clase controlador de Usarios
    """

    @staticmethod
    def obtener_id():
        '''Obtiene el id de usuario desde el token'''
        user_id = get_jwt_identity()
        if UserModel.es_empleado(user_id):
            return (user_id, 'empleado')
        elif UserModel.es_socio(user_id):
            return (user_id, 'socio')

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
        hash_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')

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
        try:
            if not bcrypt.checkpw(password.encode('utf-8'), user['passwords'].encode('utf-8')):
                return jsonify({"error": "Contraseña incorrecta"}), 401
        except ValueError:
            pass_bytes = user['passwords'].encode('utf-8')
            hash_password = bcrypt.hashpw(pass_bytes, bcrypt.gensalt()).decode('utf-8')
            UserModel.encryptar(user['id_user'], hash_password)

        # Crear el token
        token = create_access_token(identity=str(user['id_user']), expires_delta=timedelta(hours=12))

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
    @jwt_required()
    def obtener_profile():
        """ Método para obtener el perfil de un usuario por su ID. """
        user_id, rol = UserController.obtener_id()
        user = UserModel.buscar_user_por_id(user_id)

        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Verificar si el usuario es un empleado (profesor)
        if rol == 'empleado':
            profile = {
                "id_user": user['id_user'],
                "firstname": user['firstname'],
                "lastname": user['lastname'],
                "email": user['email'],
                "role": rol,  # Rol de empleado
                "gym_asignado": UserModel.obtener_gym_asignado(user_id)
            }
        # Verificar si el usuario es un socio
        elif rol == 'socio':
            profile = {
                "id_user": user['id_user'],
                "firstname": user['firstname'],
                "lastname": user['lastname'],
                "email": user['email'],
                "role": rol,  # Rol de socio
                "plan": UserModel.obtener_plan_socio(user_id),
                "activo": UserModel.obtener_estado_socio(user_id)
            }
        else:
            return jsonify({"error": "Rol desconocido"}), 400  # En caso de que no sea ni socio ni empleado

        return jsonify({"profile": profile}), 200

    @staticmethod
    @jwt_required()
    def eliminar_socio(id_user = None):
        '''Metodo para dar de baja a un socio'''
        if id_user is None:
            user_id, rol = UserController.obtener_id()
            if rol == 'socio':
                resultado = UserModel.eliminar_socio(user_id)

                # Manejo de errores
                if 'error' in resultado:
                    return jsonify({'mensaje': 'Error al eliminar el socio', 'error': resultado['error']}), 400

                # Éxito
                if resultado.get('success'):
                    return jsonify({'mensaje': 'Socio eliminado exitosamente'}), 200

                # Caso inesperado (por si ocurre algo fuera de los escenarios previstos)
                return jsonify({'mensaje': 'Ocurrió un error inesperado.'}), 500
            return jsonify({'mensaje': 'Como empleado no puedes eliminarte del sistema'})
        
        if UserModel.es_socio(id_user):
            resultado = UserModel.eliminar_socio(id_user)

            # Manejo de errores
            if 'error' in resultado:
                return jsonify({'mensaje': 'Error al eliminar el socio', 'error': resultado['error']}), 400

            # Éxito
            if resultado.get('success'):
                return jsonify({'mensaje': 'Socio eliminado exitosamente'}), 200
      
            # Caso inesperado (por si ocurre algo fuera de los escenarios previstos)
            return jsonify({'mensaje': 'Ocurrió un error inesperado.'}), 500
        return jsonify({'mensaje': 'Como empleado no puedes eliminarte del sistema'})
    
    @staticmethod
    def listar_socios():
        '''Obtiene una lista de todos los socios'''
        list_socios = []
        socios = UserModel.listar_socios()
        if 'error' in socios:
            return jsonify({'mensaje': 'Error al obtener los socios', 'error': socios['error']}), 500
        for i in range(len(socios)):
            dict_soc = dict()
            dict_soc['id_socio'] = socios[i][0]
            dict_soc['activo'] = 'si' if socios[i][1] == 1 else 'no'
            dict_soc['nombre'] = socios[i][2]
            dict_soc['apellido'] = socios[i][3]
            dict_soc['email'] = socios[i][4]
            dict_soc['plan'] = socios[i][5]
            list_socios.append(dict_soc)

        return jsonify({'actividades': list_socios}), 200