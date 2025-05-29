# Importaciones de modulos de las funciones.
from funciones.registro_usuario import ConexionDB, RegistroUsuario
from funciones.vuelos import ConexionDB, IngresoUsuario

# Conexion a la base de datos.
ruta_db = r"TU_RUTA_DB"
conexion = ConexionDB(ruta_db)


while True:
    print("""
        Bienvenido a su pagina de compra
        de tickes de vuelos:
        1. Crear un usuario.
        2. Iniciar sesion.
        3. salir
    """)
    try:
        # Ingreso de usuario.
        usuario = str(input("Ingresa la opcion que desees: ")).strip()
        # Validacion de campo primario.
        if not usuario:
            print("No se pueden tener campos en blanco, volver a intentar.")
            break
        # Opciones de usuario junto con los modulos de las funciones del sistema.
        elif usuario == "1":
            registro = RegistroUsuario(conexion)
            registro.nuevo_usuario()
        elif usuario == "2":
            login = IngresoUsuario(conexion)
            password_id = login.ingreso_usuario()
            if password_id:
                login.seleccionar_opcion()
        elif usuario == "3":
            print("Gracias por visitar a su aerolinia de confianza.")
            break
        else:
            print("Ingresar un valor valido de 1-3")
        
        input("\nPresiona enter para continuar...")

    # Manejo de errores.
    except ValueError as error:
        print(f"Error en el programa: {error}.")
