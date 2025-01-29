def cleanup(conn):
    """Limpia la base de datos y restablece los IDs de las tablas."""
    if conn is None or not conn.is_connected():
        print("Conexión a la base de datos no disponible. Saltando cleanup().")
        return

    with conn.cursor() as cursor:
        try:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

            # Resetear las tablas clave del sistema de gestión de socios
            cursor.execute("TRUNCATE TABLE socios;")
            cursor.execute("ALTER TABLE socios AUTO_INCREMENT = 1;")

            cursor.execute("TRUNCATE TABLE users;")
            cursor.execute("ALTER TABLE users AUTO_INCREMENT = 1;")

            cursor.execute("TRUNCATE TABLE empleados;")
            cursor.execute("ALTER TABLE empleados AUTO_INCREMENT = 1;")

            cursor.execute("TRUNCATE TABLE planes;")
            cursor.execute("ALTER TABLE planes AUTO_INCREMENT = 1;")

            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            conn.commit()
        except Exception as e:
            print(f"Error al ejecutar cleanup(): {e}")
