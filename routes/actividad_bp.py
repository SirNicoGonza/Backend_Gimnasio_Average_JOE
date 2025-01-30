from flask import Blueprint
from controllers.actividad_controller import ActividadController

# Crear el Blueprint
actividad_bp = Blueprint('actividad_bp', __name__)

actividad_bp.route('/', methods=['GET'])(ActividadController.listar_actividades)
actividad_bp.route('/', methods=['POST'])(ActividadController.crear_actividad)
actividad_bp.route('/<int:id_act>', methods=['PUT'])(ActividadController.actualizar_actividad)
actividad_bp.route('/<int:id_act>', methods=['DELETE'])(ActividadController.eliminar_actividad)
actividad_bp.route('/<int:id_act>', methods=['GET'])(ActividadController.obtener_actividad_por_id)
actividad_bp.route('/<string:dia>', methods=['GET'])(ActividadController.obtener_actividad_por_dia)
actividad_bp.route('/inscripcion/<int:id_act>', methods=['POST'])(ActividadController.inscripcion_actividad)
actividad_bp.route('/actxsocio', methods=['GET'])(ActividadController.obtener_actividades_por_socio)
actividad_bp.route('/actxsocio/<int:id_socio>', methods=['GET'])(ActividadController.obtener_actividades_por_id_socio)
actividad_bp.route('/inscripcion/<int:id_act>', methods=['DELETE'])(ActividadController.cancelar_inscripcion)
actividad_bp.route('/inscripcion/<int:id_act>', methods=['PATCH'])(ActividadController.renovar_inscripcion)