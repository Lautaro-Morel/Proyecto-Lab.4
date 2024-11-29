import mysql.connector
from db_connection import conectar

def crear_base_datos():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",        
            password="root"  
        )
        cursor = conexion.cursor()
        
        cursor.execute("CREATE DATABASE IF NOT EXISTS gestion;")
        
        cursor.close()
        conexion.close()

        conexion = mysql.connector.connect(
            host="localhost",
            user="root",        
            password="root", 
            database="gestion"
        )
        print("Conectado a la base de datos 'gestion'.")
        return conexion

    except mysql.connector.Error as err:
        print(f"Error al crear la base de datos: {err}")
        return None

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="gestion"
    )


def crear_tablas():
    conexion = conectar()
    cursor = conexion.cursor()
    
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS personas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            apellido VARCHAR(50) NOT NULL,
            documento VARCHAR(20) UNIQUE NOT NULL,
            fecha_nacimiento DATE NOT NULL,
            telefono VARCHAR(15),
            domicilio TEXT
        );
        """)
        print("Tabla 'personas' creada o ya existe.")
    except Exception as e:
        print(f"Error al crear la tabla 'personas': {e}")

    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario_id INT NOT NULL,
            monto DECIMAL(10, 2) NOT NULL,
            fecha_pago DATE NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES personas(id)
        );
        """)
        print("Tabla 'pagos' creada o ya existe.")
    except Exception as e:
        print(f"Error al crear la tabla 'pagos': {e}")

    conexion.commit()
    conexion.close()

def consultar_usuarios():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM personas")
    resultados = cursor.fetchall()
    
    print("\n--- Usuarios Registrados ---")
    for usuario in resultados:
        print(f"ID: {usuario[0]}, Nombre: {usuario[1]}, Apellido: {usuario[2]}, Documento: {usuario[3]}")
    conexion.close()

def agregar_usuario():
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    documento = input("Número de documento: ")
    fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")
    telefono = input("Teléfono: ")
    domicilio = input("Domicilio: ")

    conexion = conectar()
    cursor = conexion.cursor()
    sql = """
        INSERT INTO personas (nombre, apellido, documento, fecha_nacimiento, telefono, domicilio)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (nombre, apellido, documento, fecha_nacimiento, telefono, domicilio)
    
    try:
        cursor.execute(sql, valores)
        conexion.commit()
        print("Usuario agregado exitosamente.")
    except Exception as e:
        print(f"Error al agregar usuario: {e}")
    finally:
        conexion.close()

def borrar_usuario():
    id_usuario = input("ID del usuario a eliminar: ")
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "DELETE FROM personas WHERE id = %s"
    
    try:
        cursor.execute(sql, (id_usuario,))
        conexion.commit()
        if cursor.rowcount > 0:
            print("Usuario eliminado exitosamente.")
        else:
            print("No se encontró un usuario con ese ID.")
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
    finally:
        conexion.close()

def actualizar_usuario():
    id_usuario = input("ID del usuario a actualizar: ")
    nuevo_nombre = input("Nuevo nombre: ")
    nuevo_apellido = input("Nuevo apellido: ")
    nuevo_documento = input("Nuevo número de documento: ")
    nueva_fecha = input("Nueva fecha de nacimiento (YYYY-MM-DD): ")
    nuevo_telefono = input("Nuevo teléfono: ")
    nuevo_domicilio = input("Nuevo domicilio: ")

    conexion = conectar()
    cursor = conexion.cursor()
    sql = """
        UPDATE personas 
        SET nombre = %s, apellido = %s, documento = %s, fecha_nacimiento = %s, telefono = %s, domicilio = %s 
        WHERE id = %s
    """
    valores = (nuevo_nombre, nuevo_apellido, nuevo_documento, nueva_fecha, nuevo_telefono, nuevo_domicilio, id_usuario)
    
    try:
        cursor.execute(sql, valores)
        conexion.commit()
        if cursor.rowcount > 0:
            print("Usuario actualizado exitosamente.")
        else:
            print("No se encontró un usuario con ese ID.")
    except Exception as e:
        print(f"Error al actualizar usuario: {e}")
    finally:
        conexion.close()


def registrar_pago():
    documento = input("Número de documento del usuario: ")
    monto = input("Monto del pago: ")
    fecha_pago = input("Fecha del pago (YYYY-MM-DD): ")

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT id FROM personas WHERE documento = %s", (documento,))
    usuario = cursor.fetchone()
    
    if usuario:
        usuario_id = usuario[0]
        sql = """
            INSERT INTO pagos (usuario_id, monto, fecha_pago)
            VALUES (%s, %s, %s)
        """
        valores = (usuario_id, monto, fecha_pago)

        try:
            cursor.execute(sql, valores)
            conexion.commit()
            print("Pago registrado exitosamente.")
        except Exception as e:
            print(f"Error al registrar pago: {e}")
    else:
        print("No se encontró un usuario con ese documento.")
    
    conexion.close()


def consultar_pagos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT p.id, pe.nombre, pe.apellido, p.monto, p.fecha_pago
        FROM pagos p
        JOIN personas pe ON p.usuario_id = pe.id
    """)
    resultados = cursor.fetchall()
    
    print("\n--- Pagos Registrados ---")
    for pago in resultados:
        print(f"ID: {pago[0]}, Usuario: {pago[1]} {pago[2]}, Monto: ${pago[3]}, Fecha: {pago[4]}")
    conexion.close()


def eliminar_pago():
    id_pago = input("ID del pago a eliminar: ")
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "DELETE FROM pagos WHERE id = %s"
    
    try:
        cursor.execute(sql, (id_pago,))
        conexion.commit()
        if cursor.rowcount > 0:
            print("Pago eliminado exitosamente.")
        else:
            print("No se encontró un pago con ese ID.")
    except Exception as e:
        print(f"Error al eliminar pago: {e}")
    finally:
        conexion.close()


def listar_usuarios_ordenados():
    print("\n--- Opciones de Ordenamiento ---")
    print("1. Ordenar alfabéticamente (por nombre)")
    print("2. Ordenar por ID")
    print("3. Ordenar por edad")
    
    opcion = input("Seleccione una opción de ordenamiento: ")
    criterio = ""
    
    if opcion == "1":
        criterio = "nombre ASC"  
    elif opcion == "2":
        criterio = "id ASC"  
    elif opcion == "3":
        criterio = "fecha_nacimiento ASC"  
    else:
        print("Opción no válida.")
        return

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(f"""
        SELECT id, nombre, apellido, documento, fecha_nacimiento, telefono, domicilio
        FROM personas
        ORDER BY {criterio}
    """)
    resultados = cursor.fetchall()
    
    print("\n--- Usuarios Ordenados ---")
    for usuario in resultados:
        print(f"ID: {usuario[0]}, Nombre: {usuario[1]}, Apellido: {usuario[2]}, Documento: {usuario[3]}, Fecha de Nacimiento: {usuario[4]}, Teléfono: {usuario[5]}, Domicilio: {usuario[6]}")
    
    conexion.close()

def borrar_usuario():
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        usuario_id = input("Ingrese el ID del usuario que desea borrar: ")

        cursor.execute("SELECT * FROM personas WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()

        if usuario:
            print(f"Usuario encontrado: {usuario}")
            confirmacion = input("¿Está seguro de que desea borrar este usuario? (s/n): ")
            if confirmacion.lower() == 's':
                cursor.execute("DELETE FROM personas WHERE id = %s", (usuario_id,))
                conexion.commit()
                print("Usuario borrado con éxito.")
            else:
                print("Operación cancelada.")
        else:
            print("El usuario con ese ID no existe.")

    except mysql.connector.Error as err:
        print(f"Error al borrar usuario: {err}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def menu():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Consultar usuarios")
        print("2. Agregar usuario")
        print("3. Registrar pago")
        print("4. Consultar pagos")
        print("5. Eliminar pago")
        print("6. Listar usuarios ordenados")
        print("7. Borrar usuario")  
        print("8. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            consultar_usuarios()
        elif opcion == "2":
            agregar_usuario()
        elif opcion == "3":
            registrar_pago()
        elif opcion == "4":
            consultar_pagos()
        elif opcion == "5":
            eliminar_pago()
        elif opcion == "6":
            listar_usuarios_ordenados()
        elif opcion == "7":
            borrar_usuario()  
        elif opcion == "8":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    conexion = crear_base_datos()
    if conexion:
        crear_tablas()  
        menu()          