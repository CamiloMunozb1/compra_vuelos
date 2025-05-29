# Importacion de librerias para SQLite, enciptacion de contraseñas y regex
import sqlite3
import bcrypt
import re

# Clase para conexion de la base de datos.
class ConexionDB:
    def __init__(self,ruta_db):
        try:
            # Conexion y cursor para manejo de las base de datos.
            self.conn = sqlite3.connect(ruta_db)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}.")
    
    # Cierre de la base de datos.
    def cierre_db(self):
        self.conn.close()
        print("Cierre de la base de datos exitoso.")

# Clase para el registro del usuario.
class RegistroUsuario:

    def __init__(self,conexion):
        # Recibe la conexion con la base de datos.
        self.conexion = conexion

    def nuevo_usuario(self):
        try:
            # Ingreso de datos del usuario.
            nombre_usuario = input("Ingresa tu nombre: ").strip()
            apellido_usuario = input("Ingresa tu apellido de usuario: ").strip()
            nacimiento_user = input("Ingresa tu fecha de nacimiento (dd/mm/yyyy): ").strip()
            email_user = input("Ingresa tu correo electronico: ").strip()
            contraseña_user = input("Crea una contraseña (maximo 6 caracteres): ").strip()

            # eExpresiones regulares para email,contraseña y encriptador de contraseña.
            validador_contraseña = r"^[a-zA-Z0-9@#$%^&+=]{6,}$"
            validador_email =  r"[a-zA-Z-0-9]+@[a-zA-Z]+\.[a-z-.]+$"
            cifrado_contraseña = bcrypt.hashpw(contraseña_user.encode("utf-8"), bcrypt.gensalt())

            # Validadores de campos.
            if not all([nombre_usuario,apellido_usuario,nacimiento_user,email_user,contraseña_user]):
                print("Todos los campos debem estar completos.")
                return
            elif not re.fullmatch(validador_email,email_user):
                print("El email no cumple con los parametros, volver a intentar.")
                return
            elif not re.fullmatch(validador_contraseña,contraseña_user):
                print("La contraseña no cumple con los parametros, volver a intentar.")
                return
            
            # Revision del campo de "email_user" para revisar si ya existe.
            self.conexion.cursor.execute("SELECT 1 FROM usuario WHERE email_user = ?",(email_user,))
            if self.conexion.cursor.fetchone():
                print("Este correo ya fue ingresado.")
                return
            
            # Ingreso de los datos del usuario a la base de datos.
            self.conexion.cursor.execute(
                "INSERT INTO usuario (nombre_usuario,apellido_usuario,nacimiento_user,contraseña_user,email_user) VALUES (?,?,?,?,?)",(nombre_usuario,apellido_usuario,nacimiento_user,cifrado_contraseña,email_user))
            
            # Subida de los datos del usuario.
            self.conexion.conn.commit()
            print("Datos ingresados correctamente.")
        
        # Manejo de errores.
        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}.")
        except Exception as error:
            print(f"Error en el programa: {error}.")
