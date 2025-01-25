import mysql.connector
from config import Config

#Cambiar a conectionpool
class DatabaseConnection:
    _connection = None
    _config = None

    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            cls._config = Config()  
            cls._connection = mysql.connector.connect(
                host=cls._config.DATABASE_HOST,
                user=cls._config.DATABASE_USERNAME,
                port=cls._config.DATABASE_PORT,
                password=cls._config.DATABASE_PASSWORD,
                database=cls._config.DATABASE_NAME,
                use_pure=True, #Usa el cliente puro de Python
            )
        return cls._connection

    @classmethod
    def set_config(cls, config):
        cls._config = config
    
    @classmethod
    def execute_query(cls, query, params=None):
        cursor = cls.get_connection().cursor(buffered=True)
        try:
            cursor.execute(query, params)
            print("Executing SQL query: ", cursor.statement)  # Imprime la consulta SQL completa
        except Exception as e:
            print("Error executing query: ", e)  # Imprime la excepción completa
        cls._connection.commit()
        
        return cursor

    @classmethod
    def fetch_all(cls, query, params=None):
        cursor = cls.get_connection().cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    
    @classmethod
    def fetch_one(cls, query, params=None):
        cursor = cls.get_connection().cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()  # Cierra el cursor después de obtener el resultado
        return result

    @classmethod
    def close_connection(cls):
        if cls._connection is not None:
            cls._connection.close()
            cls._connection = None
