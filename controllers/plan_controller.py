from flask import jsonify, request
from flask_jwt_extended import jwt_required
from models.plan_model import PlanModel
from controllers.user_controller import UserController

class PlanController:
    """
    Controlador para manejar las operaciones relacionadas con los planes.
    """

    @staticmethod
    def listar_planes():
        """ Obtiene la lista de todos los planes. """
        list_plan = []
        planes = PlanModel.listar_planes()
        if 'error' in planes:
            return jsonify({'mensaje': 'Error al obtener los planes', 'error': planes['error']}), 500
        for i in range(len(planes)):
            dict_plan = dict()
            dict_plan['id_plan'] = planes[i][0]
            dict_plan['nombre'] = planes[i][1]
            dict_plan['precio'] = planes[i][2]
            dict_plan['descripcion'] = planes[i][3]
            dict_plan['dias al mes'] = planes[i][4]
            dict_plan['dias de gracia'] = planes[i][5]
            list_plan.append(dict_plan)

        return jsonify({'planes': list_plan}), 200

    @staticmethod
    def crear_plan():
        """ Crea un nuevo plan. """
        data = request.get_json()
        nombre = data.get('nombre')
        precio = data.get('precio')
        descripcion = data.get('descripcion')
        dias_mes = data.get('dias_mes')
        gracia = data.get('gracia')

        # Validación de datos
        if not nombre or not precio or not descripcion or not dias_mes or not gracia:
            return jsonify({'mensaje': 'Faltan datos'}), 400

        resultado = PlanModel.crear_plan(nombre, precio, descripcion, dias_mes, gracia)
        if "error" in resultado:  # Ahora se verifica si hay un error en el resultado
            return jsonify({'mensaje': 'Error al crear el plan', 'error': resultado['error']}), 500
        return jsonify({'mensaje': 'Plan creado exitosamente'}), 201

    @staticmethod
    def actualizar_plan(id_plan):
        """
		Actualiza un plan existente.
		"""
        data = request.get_json()
        nombre = data.get('nombre')
        precio = data.get('precio')
        descripcion = data.get('descripcion')
        dias_mes = data.get('dias_mes')
        gracia = data.get('gracia')

        # Validación de datos
        if not nombre or not precio or not descripcion or not dias_mes or not gracia:
            return jsonify({'mensaje': 'Faltan datos'}), 400

        resultado = PlanModel.actualizar_plan(id_plan, nombre, precio, descripcion, dias_mes, gracia)

        # Manejo de errores
        if 'error' in resultado:
            return jsonify({'mensaje': 'Error al actualizar el plan', 'error': resultado['error']}), 400

        # Éxito
        if resultado.get('success'):
            return jsonify({'mensaje': 'Plan actualizado exitosamente'}), 200

        # Caso inesperado (por si ocurre algo fuera de los escenarios previstos)
        return jsonify({'mensaje': 'Ocurrió un error inesperado.'}), 500


    @staticmethod
    def eliminar_plan(id_plan):
        """
        Elimina un plan por su ID.
        """
        resultado = PlanModel.eliminar_plan(id_plan)

        # Manejo de errores
        if 'error' in resultado:
            return jsonify({'mensaje': 'Error al eliminar el plan', 'error': resultado['error']}), 400

        # Éxito
        if resultado.get('success'):
            return jsonify({'mensaje': 'Plan eliminado exitosamente'}), 200

        # Caso inesperado (por si ocurre algo fuera de los escenarios previstos)
        return jsonify({'mensaje': 'Ocurrió un error inesperado.'}), 500


    @staticmethod
    def obtener_plan(id_plan):
        """ Obtiene un plan por su ID. """
        plan = PlanModel.obtener_plan_por_id(id_plan)
        
        # Si el resultado es None, significa que no se encontró el plan
        if plan is None:
            return jsonify({'mensaje': 'Plan no encontrado'}), 404

        # Si ocurre un error en la consulta (plan contiene un 'error')
        if isinstance(plan, dict) and 'error' in plan:
            return jsonify({'mensaje': 'Error al obtener el plan', 'error': plan['error']}), 500

        # Respuesta exitosa
        dict_plan = dict()
        dict_plan['id_plan'] = plan[0]
        dict_plan['nombre'] = plan[1]
        dict_plan['precio'] = plan[2]
        dict_plan['descripcion'] = plan[3]
        dict_plan['dias al mes'] = plan[4]
        dict_plan['dias de gracia'] = plan[5]
        return jsonify({'plan': dict_plan}), 200
    
    @staticmethod
    @jwt_required()
    def obtener_mi_plan():
        '''Obtiene el plan del socio logueado'''
        user, rol = UserController.obtener_id()


        # Verificar que el rol sea "socio"
        if rol != 'socio':
            return jsonify({"error": "Acceso denegado, solo los socios pueden acceder a esta información"}), 403
        
        plan = PlanModel.obtener_mi_plan(user)

        if not plan:
            return jsonify({'mensaje': 'Aun no tiene un plan registrado'}), 404

        # Si ocurre un error en la consulta
        if 'error' in plan:
            return jsonify({'mensaje': 'Error al obtener su plan', 'error': plan['error']}), 500

        # Respuesta exitosa
        dict_plan = dict()
        dict_plan['id_plan'] = plan[0]
        dict_plan['nombre'] = plan[1]
        dict_plan['precio'] = plan[2]
        dict_plan['descripcion'] = plan[3]
        dict_plan['dias al mes'] = plan[4]
        dict_plan['dias de gracia'] = plan[5]
        return jsonify({'plan': dict_plan}), 200
    
    @staticmethod
    @jwt_required()
    def inscripcion_plan(id_plan):
        '''Registra la inscripcion base a un plan mensual'''
        user, rol = UserController.obtener_id()

        # Verificar que el rol sea "socio"
        if rol != 'socio':
            return jsonify({"error": "Acceso denegado, solo los socios pueden acceder a esta información"}), 403
        
        resultado = PlanModel.inscripcion_plan(user, id_plan)
        if "error" in resultado:  # Ahora se verifica si hay un error en el resultado
            return jsonify({'mensaje': 'Error al registrar la inscripcion', 'error': resultado['error']}), 500
        return jsonify({'mensaje': 'Inscripción registrada. Recuerde que para ser socio activo debe pagar la cuota mensual'}), 201