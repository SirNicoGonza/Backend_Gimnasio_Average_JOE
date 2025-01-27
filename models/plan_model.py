from db import DatabaseConnection

class PlanModel:
    """
    Modelo para interactuar con la tabla 'planes' en la base de datos.
    """

    @staticmethod
    def listar_planes():
        """ Obtiene la lista de todos los planes. """
        query = "SELECT * FROM planes;"
        try:
            return DatabaseConnection.fetch_all(query)
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def crear_plan(nombre, precio, descripcion, dias_mes, gracia):
        """ Crea un nuevo plan. """
        query = "INSERT INTO planes (nombre, precio, descripcion, dias_mes, dias_gracia) VALUES (%s, %s, %s, %s, %s);"
        params = (nombre, precio, descripcion, dias_mes, gracia)
        try:
            DatabaseConnection.execute_query(query, params)
            return {"success": True}  # Devuelve un diccionario para unificar el formato
        except Exception as e:
            return {"error": str(e)}  # Devuelve un diccionario con el error


    @staticmethod
    def actualizar_plan(id_plan, nombre, precio, descripcion, dias_mes, gracia):
        """
        Actualiza un plan existente.
        """
        query = """
            UPDATE planes 
            SET nombre = %s, precio = %s, descripcion = %s, dias_mes = %s, dias_gracia = %s
            WHERE id_plan = %s;
        """
        params = (nombre, precio, descripcion, dias_mes, gracia, id_plan)
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
        query = "SELECT * FROM planes WHERE id_plan = %s;"
        params = (id_plan,)
        try:
            return DatabaseConnection.fetch_one(query, params)
        except Exception as e:
            return {'error': str(e)}
        
    @staticmethod
    def obtener_mi_plan(id_user):
        '''Obtiene el plan del socio logueado'''
        query = '''SELECT * FROM planes p
                    LEFT JOIN socios s ON s.plan_id = p.id_plan
                    WHERE s.id_user = %s'''
        params = (id_user,)
        try:
            return DatabaseConnection.fetch_one(query, params)
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def inscripcion_plan(id_user, id_plan):
        '''Registra la inscripcion base a un plan mensual'''
        query = '''UPDATE socios
                    SET plan_id = %s
                    WHERE id_user = %s'''
        params = (id_plan, id_user)
        try:
            rows_affected = DatabaseConnection.execute_query(query, params)
            if rows_affected == 0:
                return {'error': 'No se encontró un plan con el ID proporcionado.'}
            return {'success': True}
        except Exception as e:
            return {'error': str(e)}