from db import DatabaseConnection
from flask import jsonify
from utils.convertir_a_json import convertir_valores_para_json

class ActividadModel:
    '''
    Modelo para interactuar con las tablas actividades e inscripciones en la base de datos
    '''

    @staticmethod
    def crear_actividad(nombre, instructor, precio, hora, dia, cupo_max):
        '''Crea una nueva actividad'''
        query = 'INSERT INTO actividades(actividad_name, instructor, precio, hora, dia, cupo_max) VALUE (%s, %s, %s, %s, %s, %s);'
        params = (nombre, instructor, precio, hora, dia, cupo_max)
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
    def actualizar_actividad(id_act, nombre, instructor, precio, hora, dia, cupo_max):
        '''Actualizar una actividad existente'''
        query = '''UPDATE actividades
                    SET actividad_name = %s, instructor = %s, precio = %s, hora = %s, dia = %s, cupo_max = %s
                    WHERE id_actividad = %s;'''
        params = (nombre, instructor, precio, hora, dia, cupo_max, id_act)
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
    def obtener_actividad_por_fecha(fecha):
        '''Obtiene actividades por fecha'''
        query = 'SELECT * FROM actividades WHERE dia = %s;'
        params = (fecha,)
        try:
            result= DatabaseConnection.fetch_all(query, params) 
            result_formateado= convertir_valores_para_json(result)
            
            return result_formateado 
        except Exception as e:
            return {'error': str(e)}
        
    @staticmethod
    def inscripcion_actividad(id_socio, id_act):
        query = 'INSERT INTO inscripciones(socios_ID, actividad_id) VALUE (%s, %s);'
        params = (id_socio, id_act,)
        try:
            DatabaseConnection.execute_query(query, params)
            return {"success": True}  
        except Exception as e:
            return {"error": str(e)}
        
    @staticmethod
    def obtener_actividades_por_socio(id_socio):
        query = '''SELECT a.* FROM actividades a
                    JOIN inscripciones i ON a.id_actividad = i.actividad_id
                    WHERE socios_ID = %s;'''
        params = (id_socio,)
        try:
            return DatabaseConnection.fetch_all(query, params)
        except Exception as e:
            return {'error': str(e)}