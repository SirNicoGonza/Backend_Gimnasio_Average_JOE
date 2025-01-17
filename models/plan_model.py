from db import DatabaseConnection

class PlanModel:
    """
    Modelo para interactuar con la tabla 'planes' en la base de datos.
    """

    @staticmethod
    def listar_planes():
        """ Obtiene la lista de todos los planes. """
        query = "SELECT id_plan, nombre, precio, descripcion FROM planes;"
        try:
            return DatabaseConnection.fetch_all(query)
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def crear_plan(nombre, precio, descripcion):
        """ Crea un nuevo plan. """
        query = "INSERT INTO planes (nombre, precio, descripcion) VALUES (%s, %s, %s);"
        params = (nombre, precio, descripcion)
        try:
            DatabaseConnection.execute_query(query, params)
            return {"success": True}  # Devuelve un diccionario para unificar el formato
        except Exception as e:
            return {"error": str(e)}  # Devuelve un diccionario con el error


    @staticmethod
    def actualizar_plan(id_plan, nombre, precio, descripcion):
        """
        Actualiza un plan existente.
        """
        query = """
            UPDATE planes 
            SET nombre = %s, precio = %s, descripcion = %s 
            WHERE id_plan = %s;
        """
        params = (nombre, precio, descripcion, id_plan)
        try:
            rows_affected = DatabaseConnection.execute_query(query, params)
            if rows_affected == 0:
                return {'error': 'No se encontró un plan con el ID proporcionado.'}
            return {'success': True}
        except Exception as e:
            return {'error': str(e)}


    @staticmethod
    def eliminar_plan(id_plan):
        """
        Elimina un plan por su ID.
        """
        query = "DELETE FROM planes WHERE id_plan = %s;"
        params = (id_plan,)
        try:
            rows_affected = DatabaseConnection.execute_query(query, params)
            if rows_affected == 0:
                return {'error': 'No se encontró un plan con el ID proporcionado.'}
            return {'success': True}
        except Exception as e:
            return {'error': str(e)}


    @staticmethod
    def obtener_plan_por_id(id_plan):
        """ Obtiene un plan por su ID. """
        query = "SELECT id_plan, nombre, precio, descripcion FROM planes WHERE id_plan = %s;"
        params = (id_plan,)
        try:
            return DatabaseConnection.fetch_one(query, params)
        except Exception as e:
            return {'error': str(e)}
