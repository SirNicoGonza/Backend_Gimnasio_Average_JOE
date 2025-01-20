from flask import Blueprint, request
from controllers.user_controller import UserController

#Se crea el 'blueprint'
user_bp = Blueprint('user_bp', __name__ )

#registros de las rutas
@user_bp.route('/registro', methods= ['POST'] , strict_slashes= False)
def registro():
    #Se toman los datos
    data= request.get_json()

    #se llama la funcion para registrar el nuevo user
    return UserController.registrar_nuevo(data)


@user_bp.route('/login', methods=['POST'] , strict_slashes= False)
def login():
    data = request.get_json()
    return UserController.login(data)

@user_bp.route('/profile/<int:user_id>', methods=['GET'])
def obtener_profile(user_id):
    """ Ruta para obtener el perfil de un usuario por su ID. """
    return UserController.obtener_profile(user_id)
