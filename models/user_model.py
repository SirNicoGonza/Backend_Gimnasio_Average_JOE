from db import DatabaseConnection

class UserModel:
    """ Clase para el Model de user. Es para tener los métodos para new user, login y obtener perfil. """

    @staticmethod
    def crear_user(nombre, apellido, email, hash_password):
        """ Método para crear un nuevo usuario. Se necesitan nombre, apellido, email 
            y un password (una contraseña que ya debe estar encriptada).
        """
        query = "INSERT INTO users(firstname, lastname, email, passwords) VALUE (%s, %s, %s, %s);"
        params = (nombre, apellido, email, hash_password)

        try:
            DatabaseConnection.execute_query(query, params)
            return {'Usuario creado correctamente.'}
        except Exception as e:
            return {'error': str(e)}
        finally:
            DatabaseConnection.close_connection()

    @staticmethod
    def buscar_user(email):
        """ Método estático que busca un usuario por el email. """
        query = "SELECT id_user, firstname, lastname, email, passwords from users WHERE email= %s"
        params = (email,)

        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            user = cursor.fetchone()
            return user
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()

    @staticmethod
    def buscar_user_por_id(user_id):
        """ Método para buscar un usuario por su ID. """
        query = "SELECT id_user, firstname, lastname, email FROM users WHERE id_user = %s"
        params = (user_id,)

        try:
            user = DatabaseConnection.fetch_one(query, params)
            
            # Verifica que se encontró un usuario y devuelve un diccionario
            if user:
                return {
                    "id_user": user[0],
                    "firstname": user[1],
                    "lastname": user[2],
                    "email": user[3]
                }
            return None
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def es_empleado(user_id):
        """ Verifica si el usuario es un empleado (profesor). """
        query = "SELECT 1 FROM empleados WHERE user_id = %s"
        params = (user_id,)

        try:
            result = DatabaseConnection.fetch_one(query, params)
            return result is not None
        except Exception as e:
            return False  # Si ocurre un error, no consideramos al usuario como empleado

    @staticmethod
    def es_socio(user_id):
        """ Verifica si el usuario es un socio. """
        query = "SELECT 1 FROM socios WHERE id_user = %s"
        params = (user_id,)

        try:
            result = DatabaseConnection.fetch_one(query, params)
            return result is not None
        except Exception as e:
            return False  # Si ocurre un error, no consideramos al usuario como socio

    @staticmethod
    def obtener_gym_asignado(user_id):
        """ Obtiene el gimnasio asignado a un empleado. """
        query = "SELECT gym_asignado FROM empleados WHERE user_id = %s"
        params = (user_id,)

        try:
            result = DatabaseConnection.fetch_one(query, params)
            return result[0] if result else "No asignado"
        except Exception as e:
            return "Error al obtener gimnasio"

    @staticmethod
    def obtener_plan_socio(user_id):
        """ Obtiene el plan de un socio. """
        query = "SELECT p.nombre FROM socios s JOIN planes p ON s.plan_id = p.id_plan WHERE s.id_user = %s"
        params = (user_id,)

        try:
            result = DatabaseConnection.fetch_one(query, params)
            return result[0] if result else "Sin plan asignado"
        except Exception as e:
            return "Error al obtener plan"

    @staticmethod
    def obtener_estado_socio(user_id):
        """ Obtiene si el socio está activo. """
        query = "SELECT activo FROM socios WHERE id_user = %s"
        params = (user_id,)

        try:
            result = DatabaseConnection.fetch_one(query, params)
            return result[0] if result is not None else False
        except Exception as e:
            return False
        
    @staticmethod
    def asignar_socio(user_id):
        """Asigna el rol de socio al usuario."""
        query = "INSERT INTO socios (id_user, plan_id, activo) VALUES (%s, %s, %s)"
        params = (user_id, None, True)  # Inicialmente sin plan asignado, y marcado como activo

        try:
            DatabaseConnection.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Error al asignar socio: {e}")
            return False