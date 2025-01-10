from flask import Flask
from flask_cors import CORS

def create_app():
    app= Flask(__name__)

    #Habilitar CORS para todas las rutas
    CORS(app, supports_credentials=True)

    if __name__ == '__main__':
        app.run()
    return app