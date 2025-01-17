from flask import jsonify, request
from models.plan_model import PlanModel

class PlanController:
    """
    Controlador para manejar las operaciones relacionadas con los planes.
    """

    @staticmethod
    def listar_planes():
        """ Obtiene la lista de todos los planes. """
        planes = PlanModel.listar_planes()
        if 'error' in planes:
            return jsonify({'mensaje': 'Error al obtener los planes', 'error': planes['error']}), 500
        return jsonify({'planes': planes}), 200

    @staticmethod
    def crear_plan():
        """ Crea un nuevo plan. """
        data = request.get_json()
        nombre = data.get('nombre')
        precio = data.get('precio')
        descripcion = data.get('descripcion')

        # Validación de datos
        if not nombre or not precio or not descripcion:
            return jsonify({'mensaje': 'Faltan datos'}), 400

        resultado = PlanModel.crear_plan(nombre, precio, descripcion)
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

        # Validación de datos
        if not nombre or not precio or not descripcion:
            return jsonify({'mensaje': 'Faltan datos'}), 400

        resultado = PlanModel.actualizar_plan(id_plan, nombre, precio, descripcion)

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
        return jsonify({'plan': plan}), 200

