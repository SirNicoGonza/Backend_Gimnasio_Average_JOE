from flask import Blueprint, request
from controllers.user_controller import UserController

#Se crea el 'blueprint'
user_bp = Blueprint('user_bp', __name__ )

#registros de las rutas
@user_bp.route('/registro', methods= ['POST'], strict_slashes=False)
def registro():
    #Se toman los datos
    data= request.get_json()

    #se llama la funcion para registrar el nuevo user
    return UserController.registrar_nuevo(data)


@user_bp.route('/login', methods=['POST'], strict_slashes=False)
def login():
    data = request.get_json()
    return UserController.login(data)

@user_bp.route('/profile', methods=['GET'])
def obtener_profile():
    """ Ruta para obtener el perfil de un usuario por su ID. """
    return UserController.obtener_profile()

@user_bp.route('/', defaults={'id_user': None}, methods=['DELETE'])
@user_bp.route('/<int:id_user>', methods=['DELETE'])
def eliminar_socio(id_user):
    
    return UserController.eliminar_socio(id_user)

@user_bp.route('/socios', methods=['GET'])
def listar_socios():
    """Ruta para listar a todos los socios"""
    return UserController.listar_socios()