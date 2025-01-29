from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models.pago_model import PagoModel

class PagoController:
    '''
    Controlador para manejar las operaciones relacionadas con los pagos
    de plan y de actividades de los socios.
    '''

    @staticmethod
    def pago_plan(id_user):
        """Registra el pago mensual, activa al socio y habilita los días de gym"""
        socio = PagoModel.buscar_socio(id_user)
        if not socio:
            return jsonify({'mensaje': 'El usuario ingresado no es un socio registrado'}), 404
        
        plan = PagoModel.buscar_plan(id_user)
        if not plan:
            return jsonify({'mensaje': 'El socio no está registrado en ningún plan'}), 404
        
        pago = PagoModel.registrar_pago_plan(socio[0], plan[0])
        if 'error' in pago:
            return jsonify({'mensaje': 'Error al registrar el pago', 'error': pago['error']}), 500
        
        activar = PagoModel.activar_socio(id_user, plan[1], plan[2])
        if 'error' in activar:
            return jsonify({'mensaje': 'Error al activar al socio', 'error': activar['error']}), 500
        
        # Verificamos si hay socios vencidos y los cambia inactivo
        PagoModel.verificar_vencimiento()

        return jsonify({'mensaje': 'Pago registrado y socio activado exitosamente'}), 201
    
    @staticmethod
    def obtener_pagos_socio():
        """ Obtiene el historial de pagos del socio autenticado """

        # Verificar que el JWT está presente en la petición
        try:
            verify_jwt_in_request()  # Esto valida que haya un token válido en la solicitud
            id_user = get_jwt_identity()  # Extrae el id del usuario desde el token JWT
        except Exception as e:
            return jsonify({"error": "Token inválido o no proporcionado"}), 401

        # Buscar socio en la base de datos
        socio = PagoModel.buscar_socio(id_user)
        if not socio:
            return jsonify({"mensaje": "El usuario no está registrado como socio"}), 404

        # Obtener pagos
        pagos = PagoModel.obtener_pagos_por_socio(socio[0])
        if not pagos:
            return jsonify({"mensaje": "No se encontraron pagos"}), 404

        # Json pagos socio
        pagos_json = [
            {
                "id_pago": pago[0],
                "fecha_pago": pago[1],
                "id_plan": pago[2],
                "nombre_plan": pago[3]
            }
            for pago in pagos
        ]

        return jsonify({"pagos": pagos_json}), 200
