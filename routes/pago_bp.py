from flask import Blueprint
from controllers.pago_controller import PagoController

# Crear el Blueprint
pago_bp = Blueprint('pago_bp', __name__)

# Rutas
pago_bp.route('/<int:id_user>', methods=['POST'])(PagoController.pago_plan)

@pago_bp.route('/socio', methods=['GET'])
def obtener_pagos_socio():
    """ Endpoint para que un socio vea su historial de pagos """
    return PagoController.obtener_pagos_socio()
