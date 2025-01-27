from flask import jsonify
from models.pago_model import PagoModel

class PagoController:
    '''
    Controlador para manejar las operaciones relacionadas con los pagos
    de plan y de actividades de los socios
    '''

    @staticmethod
    def pago_plan(id_user):
        '''Registra el pago mensual, activa al socio y habilita los dias de gym'''
        socio = PagoModel.buscar_socio(id_user)
        if "error" in socio:
            return jsonify({'mensaje': 'El usuario ingresado no es un socio registrado'})
        plan = PagoModel.buscar_plan(id_user)
        if "error" in plan:  # Ahora se verifica si hay un error en el resultado
            return jsonify({'mensaje': 'El socio no esta registrado en ningun plan'}), 404
        pago = PagoModel.registrar_pago_plan(socio[0], plan[0])
        if 'error' in pago:
            return jsonify({'mensaje': 'Error al registrar el pago', 'error': pago['error']}), 500
        activar = PagoModel.activar_socio(id_user, plan[1], plan[2])
        if 'error' in activar:
            return jsonify({'mensaje': 'Error al activar al socio', 'error': pago['error']}), 500
        return jsonify({'mensaje': 'Pago registrado y socio activado exitosamente'}), 201
