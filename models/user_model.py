from db import DatabaseConnection

class UserModel:
    """ Clase para el Model de user. Es  para tener los metodos para new user y login.
    """

    @staticmethod
    def crear_user(nombre, apellido, email, hash_password):
        """ Metodo para crear un nuevo usuario. Se necesitan nombre, apellido, email 
            y un password(una contraseña que ya debe estar encriptada).
        """
        query= "INSERT INTO users(firstname, lastname, email, passwords) VALUE (%s, %s, %s, %s);"
        params= (nombre, apellido, email, hash_password)

        try:
            DatabaseConnection.execute_query(query, params)
            return {'Usuario creado correctamente.'}
        except Exception as e:
            return {'error': str(e)}
        finally:
            DatabaseConnection.close_connection()

    @staticmethod
    def buscar_user(email):
        """ Metodo estatico que busca por el email al usuario.
        """
        query= "SELECT id_user, firstname, lastname, email, passwords from users WHERE email= %s"
        params= (email,)

        try:
            conn= DatabaseConnection.get_connection()
            cursor= conn.cursor(dictionary=True)
            cursor.execute(query, params)
            user= cursor.fetchone()
            return user
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()