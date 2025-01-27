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
    def activar_socio(id_user, dias_mes, gracia):
        '''Activa al socio y carga la cantidad de dias habilitados en el mes'''
        query = '''UPDATE socios
                    SET activo = True, dias_habilitado = %s, dias_gracia = %s
                    WHERE id_user = %s'''
        params = (dias_mes, gracia, id_user)
        try:
            DatabaseConnection.execute_query(query, params)
            return {"success": True}  
        except Exception as e:
            return {"error": str(e)}
        
    @staticmethod
    def buscar_plan(id_user):
        '''Obtiene el id del plan , los dias de habilitacion y de gracia de un usuario'''
        query = '''SELECT s.plan_id, p.dias_mes, p.dias_gracia FROM socios s
                    INNER JOIN planes p ON s.plan_id = p.id_plan
                    WHERE id_user = %s'''
        params = (id_user,)
        try:
            return DatabaseConnection.fetch_one(query, params)
        except Exception as e:
            return {'error': str(e)}
        
    @staticmethod
    def buscar_socio(id_user):
        '''Obtiene el id de socio por el id de usuario'''
        query = '''SELECT id_socio FROM socios
                WHERE id_user = %s'''
        params = (id_user,)
        try:
            return DatabaseConnection.fetch_one(query, params)
        except Exception as e:
            return {'error': str(e)}