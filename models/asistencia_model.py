from db import DatabaseConnection
from .pago_model import PagoModel

class AsistenciaModel:
    '''
    Modelo para gestionar las asistencias del plan basico y de las actividades
    '''

    @staticmethod
    def registrar_asistencia(id_socio, id_act, tipo_asistencia):
        '''Metodo que registra la asistencia y decrementa las sesiones habilitadas'''
        query = '''INSERT INTO asistencias(id_socio, id_actividad, tipo_asistencia)
                    VALUE (%s, %s, %s);'''
        params = (id_socio, id_act, tipo_asistencia)
        try:
            DatabaseConnection.execute_query(query, params)
            return {"success": True}  
        except Exception as e:
            return {"error": str(e)}
        
    @staticmethod
    def decrementar_dias_plan(id_socio, dias_hab):
        '''Metodo que decrementa la cantidad de dias habilitados por mes para el plan'''
        dias = dias_hab - 1
        query = '''UPDATE socios SET dias_habilitado = %s
                    WHERE id_socio = %s'''
        params = (dias, id_socio)
        try:
            DatabaseConnection.execute_query(query, params)
            return {"success": True}  
        except Exception as e:
            return {"error": str(e)}
        
    @staticmethod
    def decrementar_dias_gracia(id_socio, dias_gracia):
        '''Metodo que decrementa la cantidad de dias habilitados por mes para el plan'''
        dias = dias_gracia - 1
        query = '''UPDATE socios SET dias_gracia = %s
                    WHERE id_socio = %s'''
        params = (dias, id_socio)
        try:
            DatabaseConnection.execute_query(query, params)
            return {"success": True}  
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def obtener_dias_hab(id_socio):
        '''Obtiene los dias habilitados y los dias de gracia del plan de un socio'''
        query = '''SELECT dias_habilitado, dias_gracia FROM socios
                WHERE id_socio = %s'''
        params = (id_socio,)
        try:
            return DatabaseConnection.fetch_one(query, params)
        except Exception as e:
            return {'error': str(e)}
        
    @staticmethod
    def deshabilitar_socio(id_socio):
        '''Deshabilita al socio por moroso'''
        query = '''UPDATE socios SET activo = False
                    WHERE id_socio = %s'''
        params = (id_socio,)
        try:
            DatabaseConnection.execute_query(query, params)
            return {"success": True}  
        except Exception as e:
            return {"error": str(e)}
        
    @staticmethod
    def obtener_dias_act(id_socio, id_act):
        '''Obtiene los dias habilitados de una actividad de un socio'''
        query = '''SELECT sesiones_disp FROM inscripciones
                WHERE socios_ID = %s AND actividad_id = %s'''
        params = (id_socio, id_act)
        try:
            return DatabaseConnection.fetch_one(query, params)
        except Exception as e:
            return {'error': str(e)}
        
    @staticmethod
    def decrementar_dias_actividad(id_socio, id_act, dias_act):
        '''Metodo que decrementa la cantidad de dias habilitados por mes para el plan'''
        dias = dias_act - 1
        query = '''UPDATE inscripciones SET sesiones_disp = %s
                    WHERE socios_ID = %s AND actividad_id = %s'''
        params = (dias, id_socio, id_act)
        try:
            DatabaseConnection.execute_query(query, params)
            return {"success": True}  
        except Exception as e:
            return {"error": str(e)}
        
    @staticmethod
    def deshabilitar_inscripcion(id_socio, id_act):
        '''Deshabilita la actividad hasta nuevo pago'''
        query = '''UPDATE inscripciones SET estado = False
                    WHERE socios_ID = %s AND actividad_id = %s'''
        params = (id_socio, id_act)
        try:
            DatabaseConnection.execute_query(query, params)
            return {"success": True}  
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def obtener_asistencias_por_socio(id_socio):
        socio = PagoModel.buscar_socio(id_socio)
        """Obtiene todas las asistencias de un socio."""
        query = '''SELECT id_asistencia, fecha_hora, id_actividad, tipo_asistencia FROM asistencias
                WHERE id_socio = %s ORDER BY fecha_hora DESC'''
        params = (socio[0],)
        try:
            return DatabaseConnection.fetch_all(query, params)
        except Exception as e:
            return {"error": str(e)}
