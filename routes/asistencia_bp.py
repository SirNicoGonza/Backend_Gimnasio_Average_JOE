from flask import Blueprint
from controllers.asistencia_controller import AsistenciaController

# Crear el Blueprint
asistencia_bp = Blueprint('asistencia_bp', __name__)

asistencia_bp.route('/', methods=['POST'])(AsistenciaController.registrar_asistencia)