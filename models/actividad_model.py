from db import DatabaseConnection
from utils.convertir_a_json import convertir_valores_para_json
from .pago_model import PagoModel

class ActividadModel:
    '''
    Modelo para interactuar con las tablas actividades e inscripciones en la base de datos
    '''

    @staticmethod
    def crear_actividad(nombre, instructor, precio, hora, dias, cupo_max, cupo_disp, sesiones):
        '''Crea una nueva actividad'''
        query = '''INSERT INTO actividades(actividad_name, instructor, precio, hora, dias, cupo_max, cupo_disp, sesiones) 
        VALUE (%s, %s, %s, %s, %s, %s, %s, %s);'''
        params = (nombre, instructor, precio, hora, dias, cupo_max, cupo_disp, sesiones)
        try:
            DatabaseConnection.execute_query(query, params)
            return {"success": True}  
        except Exception as e:
            return {"error": str(e)} 
        
    @staticmethod
    def listar_actividades():
        '''Obtiene la lista de todas las actividades'''
        query = 'SELECT * from actividades;'
        try:
            result= DatabaseConnection.fetch_all(query)
            result_formateado= convertir_valores_para_json(result)
            
            return result_formateado
        
        except Exception as e:
            return {'error': str(e)}
        
    @staticmethod
    def actualizar_actividad(id_act, nombre, instructor, precio, hora, dias, cupo_max, cupo_disp, sesiones):
        '''Actualizar una actividad existente'''
        query = '''UPDATE actividades
                    SET actividad_name = %s, instructor = %s, precio = %s, hora = %s, dias = %s, cupo_max = %s, cupo_disp = %s, sesiones = %s
                    WHERE id_actividad = %s;'''
        params = (nombre, instructor, precio, hora, dias, cupo_max, cupo_disp, sesiones, id_act)
        try:
            rows_affected = DatabaseConnection.execute_query(query, params)
            if rows_affected == 0:
                return {'error': 'No se encontró una actividad con el ID proporcionado.'}
            return {'success': True}
        except Exception as e:
            return {'error': str(e)}
        
    @staticmethod
    def eliminar_actividad(id_act):
        '''Elimina una actividad por su id'''
        query = 'DELETE FROM actividades WHERE id_actividad = %s;'
        params = (id_act,)
        try:
            rows_affected = DatabaseConnection.execute_query(query, params)
            if rows_affected == 0:
                return {'error': 'No se encontró una actividad con el ID proporcionado.'}
            return {'success': True}
        except Exception as e:
            return {'error': str(e)}
        
    @staticmethod
    def obtener_actividad_por_id(id_act):
        '''Obtiene una actividad por su ID'''
        query = 'SELECT * FROM actividades WHERE id_actividad = %s;'
        params = (id_act,)
        try:
            result= DatabaseConnection.fetch_one(query, params)
            result_formateado= convertir_valores_para_json(result)
            
            return result_formateado
        except Exception as e:
            return {'error': str(e)}
        
    @staticmethod
    def obtener_actividad_por_dia(dia):
        '''Obtiene actividades por fecha'''
        query = 'SELECT * FROM actividades WHERE dias LIKE %s;'
        params = (f"%{dia}%",)
        try:
            result= DatabaseConnection.fetch_all(query, params) 
            result_formateado= convertir_valores_para_json(result)
            
            return result_formateado 
        except Exception as e:
            return {'error': str(e)}
        
    @staticmethod
    def inscripcion_actividad(id_socio, id_act):
        query = 'INSERT INTO inscripciones(socios_ID, actividad_id) VALUE (%s, %s);'
        params = (id_socio, id_act)
        try:
            DatabaseConnection.execute_query(query, params)
            return {"success": True}  
        except Exception as e:
            return {"error": str(e)}
        
    @staticmethod
    def descontar_cupo_disp(id_act, cupo_disp):
        '''Cuando se genera una inscripcion, descuenta el cupo disponible de la actividad'''
        new_cupo_disp = cupo_disp - 1
        query = '''UPDATE actividades SET cupo_disp = %s
                    WHERE id_actividad = %s'''
        params = (new_cupo_disp, id_act)
        try:
            DatabaseConnection.execute_query(query, params)
            return {"success": True}  
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def obtener_actividades_por_socio(id_user):
        socio = PagoModel.buscar_socio(id_user)
        query = '''SELECT a.* FROM actividades a
                    JOIN inscripciones i ON a.id_actividad = i.actividad_id
                    WHERE socios_ID = %s;'''
        params = (socio[0],)
        try:
            result= DatabaseConnection.fetch_all(query, params) 
            result_formateado= convertir_valores_para_json(result)
            
            return result_formateado
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def obtener_actividades_por_id_socio(id_socio):
        query = '''SELECT a.* FROM actividades a
                    JOIN inscripciones i ON a.id_actividad = i.actividad_id
                    WHERE socios_ID = %s;'''
        params = (id_socio,)
        try:
            result= DatabaseConnection.fetch_all(query, params) 
            result_formateado= convertir_valores_para_json(result)
            
            return result_formateado
        except Exception as e:
            return {'error': str(e)}
        
        
    @staticmethod
    def deshabilitar_actividad(id_act):
        '''Deshabilita la actividad cuando se cubre el cupo maximo'''
        query = '''UPDATE actividades SET estado = False
                    WHERE id_actividad = %s'''
        params = (id_act,)
        try:
            DatabaseConnection.execute_query(query, params)
            return {"success": True}  
        except Exception as e:
            return {"error": str(e)}
        
    @staticmethod
    def habilitar_actividad(id_act):
        '''Habilita la actividad cuando vuelve a haber cupo disponible'''
        query = '''UPDATE actividades SET estado = True
                    WHERE id_actividad = %s'''
        params = (id_act,)
        try:
            DatabaseConnection.execute_query(query, params)
            return {"success": True}  
        except Exception as e:
            return {"error": str(e)}
        
    @staticmethod
    def cancelar_inscripcion(id_socio, id_act):
        '''Elimina una inscripcion a una actividad'''
        query = 'DELETE FROM inscripciones WHERE socios_ID = %s AND actividad_id = %s;'
        params = (id_socio, id_act)
        try:
            rows_affected = DatabaseConnection.execute_query(query, params)
            if rows_affected == 0:
                return {'error': 'No se encontró una inscripcion con los datos proporcionados.'}
            return {'success': True}
        except Exception as e:
            return {'error': str(e)}
        
    @staticmethod
    def incremetar_cupo_disp(id_act, cupo_disp):
        '''Cuando se cancela una inscripcion o se cumplen las sesiones mensuales, incrementa el cupo disponible de la actividad'''
        new_cupo_disp = cupo_disp + 1
        query = '''UPDATE actividades SET cupo_disp = %s
                    WHERE id_actividad = %s'''
        params = (new_cupo_disp, id_act)
        try:
            DatabaseConnection.execute_query(query, params)
            return {"success": True}  
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def renovar_inscripcion(id_socio, id_act):
        '''Renueva la inscripcion a una actividad'''
        query = '''UPDATE inscripciones
                    SET estado = True
                    WHERE socios_ID = %s AND actividad_id = %s;'''
        params = (id_socio, id_act)
        try:
            rows_affected = DatabaseConnection.execute_query(query, params)
            if rows_affected == 0:
                return {'error': 'No se encontró una inscripcion para renovar con los datos proporcionados.'}
            return {'success': True}
        except Exception as e:
            return {'error': str(e)}
        
    @staticmethod
    def habilitar_sesiones(id_socio, id_act, sesiones):
        '''Habilita las sesiones de una actividad luego del pago'''
        query = '''UPDATE inscripciones SET sesiones_disp = %s WHERE socios_ID = %s AND actividad_id = %s'''
        params = (sesiones, id_socio, id_act)
        try:
            rows_affected = DatabaseConnection.execute_query(query, params)
            if rows_affected == 0:
                return {'error': 'No se encontró una actividad con los datos proporcionados.'}
            return {'success': True}
        except Exception as e:
            return {'error': str(e)}