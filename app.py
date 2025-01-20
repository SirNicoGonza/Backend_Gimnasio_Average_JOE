from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from routes.user_bp import user_bp

def create_app():
    app= Flask(__name__)

    config= Config()
    app.config['JWT_SECRET_KEY'] = config.SECRET_KEY

    jwt = JWTManager(app)

    #Habilitar CORS para todas las rutas
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

    #Se registran los blueprint
    app.register_blueprint(user_bp, url_prefix= '/user')

    @app.route('/')
    def home():
        return "API FUNCIONA.. SIUUUUUU!!!."

    if __name__ == '__main__':
        app.run()
    return app