

while True:
    print("""
        Bienvenido a su pagina de compra
        de tickes de vuelos:
        1. Crear un usuario.
        2. Ingresa para consultar vuelos.
        3. salir
    """)
    try:
        usuario = str(input("Ingresa la opcion que desees."))
        if usuario == "1":
            print("Proxima funcionalidad.")
        elif usuario == "2":
            print("Proxima funcionalidad.")
        elif usuario == "3":
            print("Gracias por preferirnos.")
            break
    except ValueError as error:
        print(f"Error en el programa: {error}.")
