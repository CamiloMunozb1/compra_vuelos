import sqlite3
import bcrypt
import re

class ConexionDB:
    def __init__(self,ruta_db):
        try:
            self.conn = sqlite3.connect(ruta_db)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}.")
    
    def cierre_db(self):
        self.conn.close()
        print("Cierre de la base de datos exitoso.")

class RegistroUsuario:
    def __init__(self,conexion):
        self.conexion = conexion
    def nuevo_usuario(self):
        try:
            nombre_usuario = input("Ingresa tu nombre: ").strip()
            apellido_usuario = input("Ingresa tu apellido de usuario: ").strip()
            nacimiento_user = input("Ingresa tu fecha de nacimiento (dd/mm/yyyy): ").strip()
            email_user = input("Ingresa tu correo electroico: ").strip()
            contraseña_user = input("Crea una contraseña (maximo 6 caracteres): ").strip()

            validador_contraseña = r"^[a-zA-Z0-9@#$%^&+=]{6,}$"
            validador_email =  r"[a-zA-Z-0-9]+@[a-zA-Z]+\.[a-z-.]+$"
            cifrado_contraseña = bcrypt.hashpw(contraseña_user.encode("utf-8"), bcrypt.gensalt())

            if not all([nombre_usuario,apellido_usuario,nacimiento_user,email_user,contraseña_user]):
                print("Todos los campos debem estar completos.")
                return
            elif not re.fullmatch(validador_email,email_user):
                print("El email no cumple con los parametros, volver a intentar.")
                return
            elif not re.fullmatch(validador_contraseña,contraseña_user):
                print("La contraseña no cumple con los parametros, volver a intentar.")
                return
            
            self.conexion.cursor.execute("SELECT 1 FROM usuario WHERE email_user = ?",(email_user,))
            if self.conexion.cursor.fetchone():
                print("Este correo ya fue ingresado.")
                return
            
            self.conexion.cursor.execute(
                "INSERT INTO usuario (nombre_usuario,apellido_usuario,nacimiento_user,contraseña_user,email_user) VALUES (?,?,?,?,?)",(nombre_usuario,apellido_usuario,nacimiento_user,cifrado_contraseña,email_user))
            
            self.conexion.conn.commit()
            print("Datos ingresados correctamente.")
        
        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}.")
        except Exception as error:
            print(f"Error en el programa: {error}.")
