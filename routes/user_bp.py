from flask import Blueprint, request
from controllers.user_controller import UserController

#Se crea el 'blueprint'
user_bp = Blueprint('user_bp', __name__ )

#registros de las rutas
@user_bp.route('/registro', methods= ['POST'])
def registro():
    #Se toman los datos
    data= request.get_json()

    #se llama la funcion para registrar el nuevo user
    return UserController.registrar_nuevo(data)
