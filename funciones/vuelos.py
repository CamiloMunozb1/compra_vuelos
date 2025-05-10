import sqlite3
import bcrypt
import re

class ConexionDB:
    def __init__(self, ruta_db):
        try:
            self.conn = sqlite3.connect(ruta_db)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}.")
    
    def cierre_db(self):
        self.conn.close()
        print("Cierre de la base de datos exitoso.")

class IngresoUsuario:
    def __init__(self,conexion):
        self.conexion = conexion
        self.password_id = None
        self.opciones
    
    def ingreso_usuario(self):
        try:
            
            email_user = str(input("Ingresa tu correo electronico: ")).strip()
            contraseña_user = int(input("Ingresa tu contraseña: "))

            validador_contraseña = r"^[a-zA-Z0-9@#$%^&+=]{6,}$"
            validador_email =  r"[a-zA-Z-0-9]+@[a-zA-Z]+\.[a-z-.]+$"
            intentos_contraseña = 3

            if not all([email_user,contraseña_user]):
                print("Los campos deben estar completos.")
                return
            elif re.fullmatch(validador_email,email_user):
                print("Ingreso del email invalido, volver a intentar.")
                return
            elif re.fullmatch(validador_contraseña, contraseña_user):
                print("Ingreso de contraseña invalido, volver a intentar.")
                return
            
            
            self.conexion.cursor.execute("SELECT contraseña_user FROM usuario WHERE email_user = ?",(email_user,))
            contraseña = self.conexion.cursor.fetchone()
            if contraseña:
                contraseña_user = contraseña[0]
                while intentos_contraseña < 0:
                    if bcrypt.checkpw(contraseña_user.encode("utf-8"),contraseña_user):
                        print("Sesion iniciada...")
                        self.password_id = contraseña_user
                        return contraseña_user
                    else:
                        intentos_contraseña -= 1
                        print(f"Contraseña incorrecta, te quedan {intentos_contraseña}.")
                        if intentos_contraseña < 0:
                            contraseña_user = str(input("Vuelve a ingresar tu contraseña: "))
                print("Se agotaron los intentos...")
                return None
            else:
                print("Usuario no entontrado.")
                return
            
        except sqlite3 as error:
            print(f"Error en la base de datos: {error}")
        except Exception as error:
            print(f"Error en el progrma: {error}.")
