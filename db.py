import mysql.connector
from config import Config

class DatabaseConnection:
    _connection = None
    _config = None

    @classmethod
    def get_connection(cls):
        """Obtiene una conexión a la base de datos, asegurando que esté activa."""
        if cls._connection is None or not cls._connection.is_connected():
            cls._config = Config()
            try:
                cls._connection = mysql.connector.connect(
                    host=cls._config.DATABASE_HOST,
                    user=cls._config.DATABASE_USERNAME,
                    port=cls._config.DATABASE_PORT,
                    password=cls._config.DATABASE_PASSWORD,
                    database=cls._config.DATABASE_NAME,
                    use_pure=True
                )
                print("✅ Conexión a la base de datos establecida correctamente.")
            except mysql.connector.Error as e:
                print(f"Error al conectar a la base de datos: {e}")
                cls._connection = None  # Asegura que no se intente usar una conexión rota
        return cls._connection

    @classmethod
    def execute_query(cls, query, params=None):
        """Ejecuta una consulta SQL y maneja errores."""
        conn = cls.get_connection()
        if conn is None:
            raise Exception("No se pudo conectar a la base de datos.")

        cursor = conn.cursor(buffered=True)
        try:
            cursor.execute(query, params)
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error ejecutando la consulta: {e}")
        finally:
            cursor.close()

    @classmethod
    def fetch_all(cls, query, params=None):
        """Obtiene múltiples filas de una consulta."""
        conn = cls.get_connection()
        if conn is None:
            raise Exception("No se pudo conectar a la base de datos.")

        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        return result

    @classmethod
    def fetch_one(cls, query, params=None):
        """Obtiene una fila de una consulta."""
        conn = cls.get_connection()
        if conn is None:
            raise Exception("No se pudo conectar a la base de datos.")

        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        return result

    @classmethod
    def close_connection(cls):
        """Cierra la conexión a la base de datos si está abierta."""
        if cls._connection is not None:
            cls._connection.close()
            cls._connection = None
