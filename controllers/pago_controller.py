from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models.pago_model import PagoModel
from models.actividad_model import ActividadModel
from .actividad_controller import ActividadController

class PagoController:
    '''
    Controlador para manejar las operaciones relacionadas con los pagos
    de plan y de actividades de los socios.
    '''

    @staticmethod
    def pago_plan(id_socio):
        """Registra el pago mensual, activa al socio y habilita los días de gym"""
        
        
        gracia = PagoModel.obtener_gracia(id_socio)
        
        plan = PagoModel.buscar_plan(id_socio)
        if not plan:
            return jsonify({'mensaje': 'El socio no está registrado en ningún plan'}), 404
        
        if PagoModel.primer_pago(id_socio, plan[0]):
            gracia_r = plan[2]
        else:
            gracia_r = gracia[0]
        
        pago = PagoModel.registrar_pago_plan(id_socio, plan[0])
        if 'error' in pago:
            return jsonify({'mensaje': 'Error al registrar el pago', 'error': pago['error']}), 500
        
        activar = PagoModel.activar_socio(id_socio, plan[1], plan[2], gracia_r)
        if 'error' in activar:
            return jsonify({'mensaje': 'Error al activar al socio', 'error': activar['error']}), 500
        
        # Verificamos si hay socios vencidos y los cambia inactivo
        PagoModel.verificar_vencimiento()

        return jsonify({'mensaje': 'Pago registrado y socio activado exitosamente'}), 201
    
    @staticmethod
    def pago_actividad(id_socio, id_act):
        '''Registra el pago de una actividad y habilita las sesiones mensuales'''
        if PagoModel.inscripto(id_socio, id_act):
            response, _ = ActividadController.obtener_actividad_por_id(id_act)
            actividad = response.get_json()
            print(actividad)
            pago = PagoModel.registrar_pago_actividad(id_socio, id_act)
            if 'error' in pago:
                return jsonify({'mensaje': 'Error al registrar el pago', 'error': pago['error']}), 500
            habilitar = ActividadModel.habilitar_sesiones(id_socio, id_act, actividad['actividad']['sesiones'])
            if 'error' in habilitar:
                return jsonify({'mensaje': 'Error al habilitar las sesiones', 'error': habilitar['error']}), 500
            return jsonify({'mensaje': 'Pago registrado y sesiones habilitadas exitosamente'}), 201
        return jsonify({'mensaje': 'No hay una inscripcion registrada con esos datos'}), 201
        
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
            return jsonify({"mensaje": "Aún no hay pagos registrados"}), 200

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
