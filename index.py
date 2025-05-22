from funciones.registro_usuario import ConexionDB, RegistroUsuario


ruta_db = r"TU_BASE_DATOS"
conexion = ConexionDB(ruta_db)

while True:
    print("""
        Bienvenido a su pagina de compra
        de tickes de vuelos:
        1. Crear un usuario.
        2. Ingresa para consultar vuelos.
        3. salir
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
            print("Proxima funcionalidad.")
        elif usuario == "3":
            print("Gracias por preferirnos.")
            break
        else:
            print("Ingresar un valor valido de 1-3")
        
        input("\nPresiona enter para continuar...")

    except ValueError as error:
        print(f"Error en el programa: {error}.")
