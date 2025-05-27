from funciones.registro_usuario import ConexionDB, RegistroUsuario
from funciones.vuelos import ConexionDB, IngresoUsuario


ruta_db = r"C:\Users\POWER\reserva_vuelo.db"
conexion = ConexionDB(ruta_db)

while True:
    print("""
        Bienvenido a su pagina de compra
        de tickes de vuelos:
        1. Crear un usuario.
        2. Iniciar sesion.
        2. salir
    """)
    try:
        usuario = str(input("Ingresa la opcion que desees: ")).strip()
        if not usuario:
            print("No se pueden tener campos en blanco, volver a intentar.")
            break
        elif usuario == "1":
            registro = RegistroUsuario(conexion)
            registro.nuevo_usuario()
        elif usuario == "2":
            login = IngresoUsuario(conexion)
            password_id = login.ingreso_usuario()
            if password_id:
                login.seleccionar_opcion()
        else:
            print("Ingresar un valor valido de 1-3")
        
        input("\nPresiona enter para continuar...")

    except ValueError as error:
        print(f"Error en el programa: {error}.")
