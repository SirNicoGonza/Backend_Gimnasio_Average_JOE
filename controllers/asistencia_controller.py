from flask import jsonify, request
from models.asistencia_model import AsistenciaModel

class AsistenciaController:
    '''
    Controlador para gestionar las asistencias de los socios
    '''

    @staticmethod
    def registrar_asistencia():
        '''Registra una asistencia del socio'''
        data = request.get_json()
        id_socio = data.get('id_socio')
        id_actividad = data.get('id_actividad') #Puede ser None
        tipo_asistencia = 'actividad' if id_actividad else 'plan'

        if not id_socio:
            return jsonify({'mensaje': 'Faltan datos'}), 400
        
        resultado = AsistenciaModel.registrar_asistencia(id_socio, id_actividad, tipo_asistencia)
        if "error" in resultado:  # Ahora se verifica si hay un error en el resultado
            return jsonify({'mensaje': 'Error al registrar la asistencia', 'error': resultado['error']}), 500
        if tipo_asistencia == 'plan':
            dias = AsistenciaModel.obtener_dias_hab(id_socio)
            if dias[0]:
                decrementar = AsistenciaModel.decrementar_dias_plan(id_socio, dias[0])
                if "error" in decrementar:  # Ahora se verifica si hay un error en el resultado
                        return jsonify({'mensaje': 'Error al decrementar los dias disponibles', 'error': decrementar['error']}), 500
            elif dias[1]:
                decrementar = AsistenciaModel.decrementar_dias_gracia(id_socio, dias[1])
                if "error" in decrementar:  # Ahora se verifica si hay un error en el resultado
                    return jsonify({'mensaje': 'Error al decrementar los dias de gracia', 'error': decrementar['error']}), 500
            else:
                return jsonify({'mensaje': 'Estado deudor. Debe pagar la cuota para habilitar los dias'})
            if dias[1] == 1:
                deshabilitar = AsistenciaModel.deshabilitar_socio(id_socio)
                if "error" in deshabilitar:  # Ahora se verifica si hay un error en el resultado
                    return jsonify({'mensaje': 'Error al deshabilitar al socio', 'error': deshabilitar['error']}), 500
                print('Socio deshabilitado hasta nuevo pago')
            if dias[0] == 1:
                print('Cuota vencida, solo le quedan disponibles los dias de gracia')
            return jsonify({'mensaje': 'Asistencia registrada exitosamente'}), 201
        else:
            dias = AsistenciaModel.obtener_dias_act(id_socio, id_actividad)
            if dias[0]:
                decrementar = AsistenciaModel.decrementar_dias_actividad(id_socio, id_actividad, dias[0])
                if "error" in decrementar:  # Ahora se verifica si hay un error en el resultado
                    return jsonify({'mensaje': 'Error al decrementar los dias de la actividad', 'error': decrementar['error']}), 500
            else:
                return jsonify({'mensaje': 'No tiene mas sesiones disponibles. Debe renovar'})
            if dias[0] == 1:
                deshabilitar = AsistenciaModel.deshabilitar_inscripcion(id_socio, id_actividad)
                if "error" in deshabilitar:  # Ahora se verifica si hay un error en el resultado
                    return jsonify({'mensaje': 'Error al deshabilitar al socio', 'error': deshabilitar['error']}), 500
                print('Actividad deshabilitada hasta nuevo pago')
            return jsonify({'mensaje': 'Asistencia registrada exitosamente'}), 201