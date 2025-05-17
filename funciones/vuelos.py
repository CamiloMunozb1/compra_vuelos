import sqlite3
import bcrypt
from cryptography.fernet import Fernet
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
        self.opciones_usuario()
    
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

    def opciones_usuario(self):
        self.opciones = {
            "1" : self.opcion_uno,
            "2" : self.opcion_dos,
            "3" : self.opcion_tres
        }
    
    def mostras_opciones(self):
        print("""
            Ingresa la opcion que desees:
            1. Ingresa tu tarjeta de credito.
            2. Reserva tu vuelo.
            3. Cerrar sesion.
        """)
    
    def seleccionar_opcion(self):
        try:
            while True:
                usuario = str(input("Ingresa la opcion que desees: ")).strip()
                if not usuario:
                    print("Debes seleccionar una opcion.")
                    continue
                accion = self.opciones.get(usuario)
                if accion:
                    accion()
                    if accion == "5":
                        break
                else:
                    print("Ingresa por favor una opcion del 1 al 3.")
        except ValueError:
            print("Error de digitacion, ingresa una opcion correcta.")
    
    def ingreso_tarjeta(self):
        try:

            numero_tarjeta = input("Ingresa tu pan de tarjeta: ").strip()
            fecha_vencimiento = input("Ingresa la fecha de vencimiento de tu tarjeta: ").strip()
            codigo_seguridad = input("Ingresa el codigo de seguridad de tu tarjeta: ").strip()


            validador_tarjeta = r"^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$"
            validador_vencimiento = r"^(0[1-9]|1[0-2])\/\d{2}$"
            validador_cvv = r"^\d{3,4}$"


            if not all([numero_tarjeta,fecha_vencimiento,codigo_seguridad]):
                print("Los campos deben estar completos.")
            if not re.fullmatch(validador_tarjeta,numero_tarjeta):
                print("El formato de la tarjeta no es valido.")
                return
            if not re.fullmatch(validador_vencimiento,fecha_vencimiento):
                print("La fecha de vencimiento es invalida.")
                return
            if not re.fullmatch(validador_cvv,codigo_seguridad):
                print("El codigo de seguridad no es valido.")
                return
            
            self.conexion.cursor.execute("SELECT 1 FROM usuario WHERE numero_tarjeta = ?",(numero_tarjeta,))
            if self.conexion.cursor.fetchone():
                print("Tarjeta ya ingresada.")
                return
            
            key = Fernet.generate_key()
            cipher = Fernet(key)
            encrypted_pan = cipher.encrypt(numero_tarjeta.encode())
            encrypted_expired = cipher.encrypt(fecha_vencimiento.encode())
            encrypted_cvv = cipher.encrypt(codigo_seguridad.encode())
            
            self.conexion.cursor.execute("INSERT INTO tarjeta_usuario(numero_tarjeta,fecha_vencimiento,codigo_seguridad) VALUES(?,?,?)",(encrypted_pan,encrypted_expired,encrypted_cvv))
            self.conexion.conn.commit()
            print("Tarjeta ingresada de manera correcta.")
        
        except sqlite3 as error:
            print(f"Error en la base de datos: {error}")
        except Exception as error:
            print(f"Error en el programa: {error}.")