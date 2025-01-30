from db import DatabaseConnection

class PagoModel:
    '''Modelo para interactuar con los pagos de planes y actividades'''

    @staticmethod
    def registrar_pago_plan(id_socio, id_plan):
        '''Metodo para registrar el pago del plan de un socio'''
        query = '''INSERT INTO pagos_planes(ID_socio, plan) VALUE (%s, %s)'''
        params = (id_socio, id_plan)
        try:
            DatabaseConnection.execute_query(query, params)
            return {"success": True}  
        except Exception as e:
            return {"error": str(e)} 
        
    @staticmethod
    def activar_socio(id_socio, dias_mes, gracia, gracia_restante):
        '''Activa al socio y carga la cantidad de dias habilitados en el mes'''
        gracia_habilitar = gracia - (gracia - gracia_restante)
        query = '''UPDATE socios
                    SET activo = True, dias_habilitado = %s, dias_gracia = %s
                    WHERE id_socio = %s'''
        params = (dias_mes, gracia_habilitar, id_socio)
        try:
            DatabaseConnection.execute_query(query, params)
            return {"success": True}  
        except Exception as e:
            return {"error": str(e)}
        
    @staticmethod
    def buscar_plan(id_socio):
        '''Obtiene el id del plan , los dias de habilitacion y de gracia de un usuario'''
        query = '''SELECT s.plan_id, p.dias_mes, p.dias_gracia FROM socios s
                    INNER JOIN planes p ON s.plan_id = p.id_plan
                    WHERE id_socio = %s'''
        params = (id_socio,)
        try:
            return DatabaseConnection.fetch_one(query, params)
        except Exception as e:
            return {'error': str(e)}
        
    @staticmethod
    def buscar_socio(id_user):
        '''Obtiene el id, los dias de gracia y si esta activo de un socio por el id de usuario'''
        query = '''SELECT id_socio, dias_gracia, activo FROM socios
                WHERE id_user = %s'''
        params = (id_user,)
        try:
            return DatabaseConnection.fetch_one(query, params)
        except Exception as e:
            return {'error': str(e)}
        
    @staticmethod
    def obtener_gracia(id_socio):
        '''Obtiene los dias de gracia de un socio'''
        query = '''SELECT dias_gracia FROM socios
                WHERE id_socio = %s'''
        params = (id_socio,)
        try:
            return DatabaseConnection.fetch_one(query, params)
        except Exception as e:
            return {'error': str(e)}
        
    @staticmethod
    def verificar_vencimiento():
        """ Desactiva a los socios que ya no tienen días habilitados ni días de gracia """
        query = """
            UPDATE socios 
            SET activo = 0 
            WHERE dias_habilitado = 0 AND dias_gracia = 0 AND activo = 1
        """
        try:
            DatabaseConnection.execute_query(query)
            return {"success": "Se actualizaron los socios vencidos"}
        except Exception as e:
            return {"error": str(e)}
        
    @staticmethod
    def obtener_pagos_por_socio(id_socio):
        """ Obtiene el historial de pagos de un socio """
        query = """
            SELECT p.id_pago_plan, p.fecha_pago, p.plan, pl.nombre AS plan_nombre
            FROM pagos_planes p
            JOIN socios s ON p.ID_socio = s.id_socio
            JOIN planes pl ON p.plan = pl.id_plan
            WHERE s.id_socio = %s
            ORDER BY p.fecha_pago DESC;
        """
        return DatabaseConnection.fetch_all(query, (id_socio,))

    @staticmethod
    def inscripto(id_socio, id_act):
        '''Metodo booleano para saber si un socio esta inscripto en una actividad'''
        query = 'SELECT * from inscripciones WHERE socios_ID = %s AND actividad_id = %s'
        params = (id_socio, id_act)
        try:
            resultado = DatabaseConnection.fetch_one(query, params)
            return resultado is not None
        except Exception as e:
            print(f"Error al verificar inscripción: {e}")
            return False

    @staticmethod
    def registrar_pago_actividad(id_socio, id_act):
        '''Metodo para registrar el pago de una actividad de un socio'''
        query = '''INSERT INTO pagos_actividades(socio, actividad) VALUE (%s, %s)'''
        params = (id_socio, id_act)
        try:
            DatabaseConnection.execute_query(query, params)
            return {"success": True}  
        except Exception as e:
            return {"error": str(e)} 
        
    @staticmethod
    def primer_pago(id_socio, id_plan):
        '''Metodo booleano para saber si es el primer pago del socio'''
        query = 'SELECT * FROM pagos_planes WHERE ID_socio = %s AND plan = %s'
        params = (id_socio, id_plan)
        try:
            resultado = DatabaseConnection.fetch_one(query, params)
            return resultado is not None
        except Exception as e:
            print(f"Error al verificar pagos: {e}")
            return False