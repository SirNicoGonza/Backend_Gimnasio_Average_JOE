from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from routes.user_bp import user_bp
from routes.plan_bp import plan_bp  # Importar el Blueprint de planes
from routes.actividad_bp import actividad_bp
from routes.pago_bp import pago_bp
from routes.asistencia_bp import asistencia_bp

def create_app():
    app = Flask(__name__)

    config = Config()
    app.config['JWT_SECRET_KEY'] = config.SECRET_KEY

    jwt = JWTManager(app)

    # Habilitar CORS para todas las rutas
    CORS(app, supports_credentials=True)

    # Registrar los Blueprints
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(plan_bp, url_prefix='/planes')  # Registrar las rutas para los planes
    app.register_blueprint(actividad_bp, url_prefix='/actividades')
    app.register_blueprint(pago_bp, url_prefix='/pagos')
    app.register_blueprint(asistencia_bp, url_prefix='/asistencias')

    @app.route('/')
    def home():
        return "API FUNCIONA.. SIUUUUUU!!!."

    if __name__ == '__main__':
        app.run()
    return app
