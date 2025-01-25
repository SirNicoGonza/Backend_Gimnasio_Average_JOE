from flask_jwt_extended import jwt_required
from flask import jsonify, request
from models.actividad_model import ActividadModel
from controllers.user_controller import UserController
from datetime import datetime

class ActividadController:
    '''
    Controlador para manejar las operaciones relacionadas con las actividades
    '''

    @staticmethod
    def crear_actividad():
        '''Crea una nueva actividad'''
        data = request.get_json()
        nombre = data.get('nombre')
        instructor = data.get('instructor')
        precio = data.get('precio')
        hora = data.get('hora')
        dia = data.get('dia')
        cupo_max = data.get('cupo_max')

        #Validacion de datos
        if not nombre or not instructor or not precio or not hora or not dia or not cupo_max:
            return jsonify({'mensaje': 'Faltan datos'}), 400
        
        resultado = ActividadModel.crear_actividad(nombre, instructor, precio, hora, dia, cupo_max)
        if "error" in resultado:  # Ahora se verifica si hay un error en el resultado
            return jsonify({'mensaje': 'Error al crear la actividad', 'error': resultado['error']}), 500
        return jsonify({'mensaje': 'Actividad creada exitosamente'}), 201
    
    @staticmethod
    def listar_actividades():
        '''Obtiene la lista de todas las actividades'''
        list_act = []
        actividades = ActividadModel.listar_actividades()
        if 'error' in actividades:
            return jsonify({'mensaje': 'Error al obtener las actividades', 'error': actividades['error']}), 500
        for i in range(len(actividades)):
            dict_act = dict()
            dict_act['id_actividad'] = actividades[i][0]
            dict_act['actividad_name'] = actividades[i][1]
            dict_act['instructor'] = actividades[i][2]
            dict_act['precio'] = actividades[i][3]
            dict_act['hora'] = actividades[i][4]
            dict_act['dia'] = actividades[i][5]
            dict_act['cupo_max'] = actividades[i][6]
            list_act.append(dict_act)

        return jsonify({'actividades': list_act}), 200
    
    @staticmethod
    def actualizar_actividad(id_act):
        '''Actualiza una actividad existente'''
        data = request.get_json()
        nombre = data.get('nombre')
        instructor = data.get('instructor')
        precio = data.get('precio')
        hora = data.get('hora')
        dia = data.get('dia')
        cupo_max = data.get('cupo_max')

        #Validacion de datos
        if not nombre or not instructor or not precio or not hora or not dia or not cupo_max:
            return jsonify({'mensaje': 'Faltan datos'}), 400
        
        resultado = ActividadModel.actualizar_actividad(id_act, nombre, instructor, precio, hora, dia, cupo_max)

        # Manejo de errores
        if 'error' in resultado:
            return jsonify({'mensaje': 'Error al actualizar la actividad', 'error': resultado['error']}), 400

        # Éxito
        if resultado.get('success'):
            return jsonify({'mensaje': 'Actividad actualizada exitosamente'}), 200

        # Caso inesperado (por si ocurre algo fuera de los escenarios previstos)
        return jsonify({'mensaje': 'Ocurrió un error inesperado.'}), 500
    
    @staticmethod
    def eliminar_actividad(id_act):
        '''Elimina una actividad por su id'''
        resultado = ActividadModel.eliminar_actividad(id_act)

        # Manejo de errores
        if 'error' in resultado:
            return jsonify({'mensaje': 'Error al eliminar la actividad', 'error': resultado['error']}), 400

        # Éxito
        if resultado.get('success'):
            return jsonify({'mensaje': 'Actividad eliminada exitosamente'}), 200

        # Caso inesperado (por si ocurre algo fuera de los escenarios previstos)
        return jsonify({'mensaje': 'Ocurrió un error inesperado.'}), 500
    
    @staticmethod
    def obtener_actividad_por_id(id_act):
        '''Obtiene una actividad por su id'''
        dict_act = dict()
        actividad = ActividadModel.obtener_actividad_por_id(id_act)
        
        # Si el resultado es None, significa que no se encontró la actividad
        if actividad is None:
            return jsonify({'mensaje': 'Actividad no encontrada'}), 404

        # Si ocurre un error en la consulta 
        if isinstance(actividad, dict) and 'error' in actividad:
            return jsonify({'mensaje': 'Error al obtener la actividad', 'error': actividad['error']}), 500

        # Respuesta exitosa
        dict_act['id_actividad'] = actividad[0]
        dict_act['actividad_name'] = actividad[1]
        dict_act['instructor'] = actividad[2]
        dict_act['precio'] = actividad[3]
        dict_act['hora'] = actividad[4]
        dict_act['dia'] = actividad[5]
        dict_act['cupo_max'] = actividad[6]
        return jsonify({'actividad': dict_act}), 200
    
    @staticmethod
    def obtener_actividad_por_fecha(fecha):
        '''Obtiene todas las actividades de una fecha determinada'''
        list_act = []
        fecha_valida = datetime.strptime(fecha, '%Y-%m-%d')
        actividades = ActividadModel.obtener_actividad_por_fecha(fecha_valida)

        if not actividades:
            return jsonify({'mensaje': 'No hay actividades para la fecha consultada'}), 404

        # Si ocurre un error en la consulta
        if 'error' in actividades:
            return jsonify({'mensaje': 'Error al obtener las actividades', 'error': actividades['error']}), 500

        # Respuesta exitosa
        for i in range(len(actividades)):
            dict_act = dict()
            dict_act['id_actividad'] = actividades[i][0]
            dict_act['actividad_name'] = actividades[i][1]
            dict_act['instructor'] = actividades[i][2]
            dict_act['precio'] = actividades[i][3]
            dict_act['hora'] = actividades[i][4]
            dict_act['dia'] = actividades[i][5]
            dict_act['cupo_max'] = actividades[i][6]
            list_act.append(dict_act)

        return jsonify({'actividades': list_act}), 200
    
    @staticmethod
    @jwt_required()
    def inscripcion_actividad(id_act):
        '''Se registra la inscripcion de un socio a una actividad'''
        user, rol = UserController.obtener_id()

        # Verificar que el rol sea "socio"
        if rol != 'socio':
            return jsonify({"error": "Acceso denegado, solo los socios pueden acceder a esta información"}), 403
        
        response_profile, _ = UserController.obtener_profile()
        profile = response_profile.get_json()
        print(profile)
        if profile['profile']['plan'] != 'Sin plan asignado':
            resultado = ActividadModel.inscripcion_actividad(user, id_act)
            if "error" in resultado:  # Ahora se verifica si hay un error en el resultado
                return jsonify({'mensaje': 'Error al registrar la inscripcion', 'error': resultado['error']}), 500
            return jsonify({'mensaje': 'Inscripción registrada exitosamente'}), 201
        return jsonify({"error": "Debe tener un plan asignado para inscribirse en actividades extras"}), 403

    @staticmethod
    @jwt_required()
    def obtener_actividades_por_socio():
        '''Obtiene las actividades de un socio por su id'''
        list_act = []
        user, rol = UserController.obtener_id()

        # Verificar que el rol sea "socio"
        if rol != 'socio':
            return jsonify({"error": "Acceso denegado, solo los socios pueden acceder a esta información"}), 403
        
        actividades = ActividadModel.obtener_actividades_por_socio(user)

        if not actividades:
            return jsonify({'mensaje': 'No hay actividades asociadas para este socio'}), 404

        # Si ocurre un error en la consulta
        if 'error' in actividades:
            return jsonify({'mensaje': 'Error al obtener las actividades', 'error': actividades['error']}), 500

        # Respuesta exitosa
        for i in range(len(actividades)):
            dict_act = dict()
            dict_act['id_actividad'] = actividades[i][0]
            dict_act['actividad_name'] = actividades[i][1]
            dict_act['instructor'] = actividades[i][2]
            dict_act['precio'] = actividades[i][3]
            dict_act['hora'] = actividades[i][4]
            dict_act['dia'] = actividades[i][5]
            dict_act['cupo_max'] = actividades[i][6]
            list_act.append(dict_act)

        return jsonify({'actividades': list_act}), 200