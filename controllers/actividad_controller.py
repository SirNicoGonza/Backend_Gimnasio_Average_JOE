from flask_jwt_extended import jwt_required
from flask import jsonify, request
from models.actividad_model import ActividadModel
from models.pago_model import PagoModel
from controllers.user_controller import UserController

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
        dias = data.get('dias')
        cupo_max = data.get('cupo_max')
        cupo_disp = data.get('cupo_disp')
        sesiones = data.get('sesiones')

        #Validacion de datos
        if not nombre or not instructor or not precio or not hora or not dias or not cupo_max or not cupo_disp or not sesiones:
            return jsonify({'mensaje': 'Faltan datos'}), 400
        
        resultado = ActividadModel.crear_actividad(nombre, instructor, precio, hora, dias, cupo_max, cupo_disp, sesiones)
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
            dict_act['dias'] = actividades[i][5]
            dict_act['cupo_max'] = actividades[i][6]
            dict_act['cupo_disp'] = actividades[i][7]
            dict_act['sesiones'] = actividades[i][8]
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
        dias = data.get('dias')
        cupo_max = data.get('cupo_max')
        cupo_disp = data.get('cupo_disp')
        sesiones = data.get('sesiones')

        #Validacion de datos
        if not nombre or not instructor or not precio or not hora or not dias or not cupo_max or not cupo_disp or not sesiones:
            return jsonify({'mensaje': 'Faltan datos'}), 400
        
        if not ActividadModel.obtener_actividad_por_id(id_act):
            return jsonify({'mensaje': 'No hay actividad registrada con ese id'})
        
        resultado = ActividadModel.actualizar_actividad(id_act, nombre, instructor, precio, hora, dias, cupo_max, cupo_disp, sesiones)

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
        dict_act['dias'] = actividad[5]
        dict_act['cupo_max'] = actividad[6]
        dict_act['cupo_disp'] = actividad[7]
        dict_act['sesiones'] = actividad[8]
        return jsonify({'actividad': dict_act}), 200
    
    @staticmethod
    def obtener_actividad_por_dia(dia):
        '''Obtiene todas las actividades de una fecha determinada'''
        list_act = []
        actividades = ActividadModel.obtener_actividad_por_dia(dia)

        if not actividades:
            return jsonify({'mensaje': 'No hay actividades para el dia consultado'}), 404

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
            dict_act['cupo_disp'] = actividades[i][7]
            dict_act['sesiones'] = actividades[i][8]
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
        
        actividad = ActividadModel.obtener_actividad_por_id(id_act)
        if not actividad:
            return jsonify({'mensaje': 'No hay actividad con el id consultado'}), 404
        
        if not actividad[7]:
            return jsonify({'mensaje': 'No quedan cupos disponibles para esta actividad'}), 403
        
        response, code = ActividadController.obtener_actividades_por_socio()
        actividades = response.get_json()
        if code == 200:
            print(code)
            for act in actividades['actividades']:
                if act['id_actividad'] == id_act:
                    return jsonify({'mensaje': 'Ya se encuentra inscripto en esta actividad'}), 403
        
        response_profile, _ = UserController.obtener_profile()
        profile = response_profile.get_json()
        if profile['profile']['plan'] != 'Sin plan asignado':
            socio = PagoModel.buscar_socio(user)
            if socio[2]:
                resultado = ActividadModel.inscripcion_actividad(socio[0], id_act)
                if "error" in resultado:  # Ahora se verifica si hay un error en el resultado
                    return jsonify({'mensaje': 'Error al registrar la inscripcion', 'error': resultado['error']}), 500
                desc_cupo = ActividadModel.descontar_cupo_disp(id_act, actividad[7])
                if "error" in desc_cupo:  # Ahora se verifica si hay un error en el resultado
                    return jsonify({'mensaje': 'Error al descontar el cupo disponible', 'error': resultado['error']}), 500
                if not (actividad[7]-1):
                    result = ActividadModel.deshabilitar_actividad(id_act)
                    if "error" in result:
                        return jsonify({'mensaje': 'Error al deshabilitar actividad por cupo completo', 'error': result['error']}), 500
                return jsonify({'mensaje': 'Inscripción registrada exitosamente'}), 201
            return jsonify({"error": "Debe ser socio activo para inscribirse en actividades extras"}), 403
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
            dict_act['cupo_disp'] = actividades[i][7]
            dict_act['sesiones'] = actividades[i][8]
            list_act.append(dict_act)

        return jsonify({'actividades': list_act}), 200
    
    @staticmethod
    @jwt_required()
    def cancelar_inscripcion(id_act):
        '''Cancela la inscripcion a una actividad'''
        user, rol = UserController.obtener_id()

        # Verificar que el rol sea "socio"
        if rol != 'socio':
            return jsonify({"error": "Acceso denegado, solo los socios pueden acceder a esta información"}), 403
        
        socio = PagoModel.buscar_socio(user)
        actividad = ActividadModel.obtener_actividad_por_id(id_act)

        resultado = ActividadModel.cancelar_inscripcion(socio[0], id_act)

        # Manejo de errores
        if 'error' in resultado:
            return jsonify({'mensaje': 'Error al eliminar la actividad', 'error': resultado['error']}), 400

        # Éxito
        if resultado.get('success'):
            if not actividad[9]:
                habilitar = ActividadModel.habilitar_actividad(id_act)
                if "error" in habilitar:
                    return jsonify({'mensaje': 'Error al habilitar actividad', 'error': habilitar['error']}), 500
            inc_cupo = ActividadModel.incremetar_cupo_disp(id_act, actividad[7])
            if "error" in inc_cupo:  # Ahora se verifica si hay un error en el resultado
                    return jsonify({'mensaje': 'Error al incrementar el cupo disponible', 'error': resultado['error']}), 500
            return jsonify({'mensaje': 'Inscripcion cancelada exitosamente'}), 200

        # Caso inesperado (por si ocurre algo fuera de los escenarios previstos)
        return jsonify({'mensaje': 'Ocurrió un error inesperado.'}), 500
    
    @staticmethod
    @jwt_required()
    def renovar_inscripcion(id_act):
        '''Se renueva la inscripcion de un socio a una actividad'''
        user, rol = UserController.obtener_id()

        # Verificar que el rol sea "socio"
        if rol != 'socio':
            return jsonify({"error": "Acceso denegado, solo los socios pueden acceder a esta información"}), 403
        
        actividad = ActividadModel.obtener_actividad_por_id(id_act)
        if not actividad:
            return jsonify({'mensaje': 'No hay actividad con el id consultado'}), 404
        
        if not actividad[7]:
            return jsonify({'mensaje': 'No quedan cupos disponibles para esta actividad'}), 403
        
        socio = PagoModel.buscar_socio(user)
        if socio[2]:
            resultado = ActividadModel.renovar_inscripcion(socio[0], id_act)
            if "error" in resultado:  # Ahora se verifica si hay un error en el resultado
                return jsonify({'mensaje': 'Error al registrar la inscripcion', 'error': resultado['error']}), 500
            desc_cupo = ActividadModel.descontar_cupo_disp(id_act, actividad[7])
            if "error" in desc_cupo:  # Ahora se verifica si hay un error en el resultado
                return jsonify({'mensaje': 'Error al descontar el cupo disponible', 'error': resultado['error']}), 500
            if not (actividad[7]-1):
                result = ActividadModel.deshabilitar_actividad(id_act)
                if "error" in result:
                    return jsonify({'mensaje': 'Error al deshabilitar actividad por cupo completo', 'error': result['error']}), 500
            return jsonify({'mensaje': 'Inscripción registrada exitosamente'}), 201
        return jsonify({"error": "Debe ser socio activo para inscribirse en actividades extras"}), 403
        
    @staticmethod
    def obtener_actividades_por_id_socio(id_socio):
        '''Obtiene las actividades de un socio por su id'''
        list_act = []
        
        actividades = ActividadModel.obtener_actividades_por_socio(id_socio)

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
            dict_act['cupo_disp'] = actividades[i][7]
            dict_act['sesiones'] = actividades[i][8]
            list_act.append(dict_act)

        return jsonify({'actividades': list_act}), 200