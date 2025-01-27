from flask import Blueprint
from controllers.plan_controller import PlanController

# Crear el Blueprint
plan_bp = Blueprint('plan_bp', __name__)

# Rutas para empleados (CRUD completo de planes)
plan_bp.route('/', methods=['GET'])(PlanController.listar_planes)
plan_bp.route('/', methods=['POST'])(PlanController.crear_plan)
plan_bp.route('/<int:id_plan>', methods=['PUT'])(PlanController.actualizar_plan)
plan_bp.route('/<int:id_plan>', methods=['DELETE'])(PlanController.eliminar_plan)
plan_bp.route('/<int:id_plan>', methods=['GET'])(PlanController.obtener_plan)
plan_bp.route('/mi_plan', methods=['GET'])(PlanController.obtener_mi_plan)
plan_bp.route('/inscripcion/<int:id_plan>', methods=['PATCH'])(PlanController.inscripcion_plan)



# Nota: Si se necesita una lógica específica para que los socios cambien su plan,
# puede agregarse un método PATCH en el controlador y definir la ruta aquí.
