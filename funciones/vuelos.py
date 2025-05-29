# Librerias para la base de datos, enciptacion de contraseñas y regex.
import sqlite3
import bcrypt
# Libreria para encriptar datos de tarjetas de credito.
from cryptography.fernet import Fernet
import re
# Libreria para mostrar los datos ingresados.
import pandas as pd

# Clase para conexion de la base de datos.
class ConexionDB:
    def __init__(self, ruta_db):
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


class IngresoUsuario:
    def __init__(self,conexion):
        self.conexion = conexion  # Recibe la conexion con la base de datos.
        self.usuario_id = None    # Almacerna el id del usuario al inicio de sesion.
        self.opciones_usuario()   # Llamamos a las opciones disponibles.
    
    def ingreso_usuario(self):
        try:
            
            # Pedimos el email y contraseña ingresados.
            email_user = input("Ingresa tu correo electronico: ").strip()
            contraseña_user = input("Ingresa tu contraseña: ").strip()

            # Expresiones regulares para validar email y contraseña.
            validador_contraseña = r"^[a-zA-Z0-9@#$%^&+=]{6,}$"
            validador_email =  r"[a-zA-Z-0-9]+@[a-zA-Z]+\.[a-z-.]+$"
            # Intentos para ingreso de contraseña.
            intentos_contraseña = 3

            # Validadores campos.
            if not all([email_user,contraseña_user]):
                print("Los campos deben estar completos.")
                return
            elif not re.fullmatch(validador_email,email_user):
                print("Ingreso del email invalido, volver a intentar.")
                return
            elif not re.fullmatch(validador_contraseña, contraseña_user):
                print("Ingreso de contraseña invalido, volver a intentar.")
                return
            
            # Se busca la contraseña y el usuario_id en la base de datos.
            self.conexion.cursor.execute("SELECT usuario_id, contraseña_user FROM usuario WHERE email_user = ?",(email_user,))
            usuario = self.conexion.cursor.fetchone()
            if usuario: # si el id del usuario existe.
                usuario_id, contraseña_hashed = usuario # se extrae tanto el hash de la contraseña y el id del usuario.
                intentos_contraseña = 3
                while intentos_contraseña > 0:
                    # Verificar si la contraseña coincide con la ingresada.
                    if bcrypt.checkpw(contraseña_user.encode("utf-8"),contraseña_hashed):
                        print("Sesion iniciada...")
                        # Se guarda y se retorna el id del usuario.
                        self.usuario_id = usuario_id
                        return usuario_id
                    else:
                        # Si la contraseña no coincide se descuentan intentos.
                        intentos_contraseña -= 1
                        print(f"Contraseña incorrecta, te quedan {intentos_contraseña}.")
                        if intentos_contraseña > 0:
                            contraseña_user = str(input("Vuelve a ingresar tu contraseña: "))
                print("Se agotaron los intentos...")
                return None
            else:
                print("Usuario no entontrado.")
                return
        # Manejo de errores.
        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}")
        except Exception as error:
            print(f"Error en el progrma: {error}.")

    # Opciones para el usuario.
    def opciones_usuario(self):
        self.opciones = {
            "1" : self.opcion_uno,
            "2" : self.opcion_dos,
            "3" : self.opcion_tres,
            "4" : self.opcion_cuatro
        }
    
    # Mostrar opciones para que el usuario elija.
    def mostras_opciones(self):
        print("""
            Ingresa la opcion que desees:
            1. Ingresa tu tarjeta de credito.
            2. Reserva tu vuelo.
            3. Mostrar vuelos.
            4. Cerrar sesion.
        """)
    
    def seleccionar_opcion(self):
        try:
            while True:
                # Imprime las opciones hacia el usuario.
                self.mostras_opciones()
                # Ingreso de opcion.
                usuario = str(input("Ingresa la opcion que desees: ")).strip()
                # Validador de campo.
                if not usuario:
                    print("Debes seleccionar una opcion.")
                    continue
                accion = self.opciones.get(usuario) # Se obtiene la opcion registrada.
                if accion:
                    accion() # Se ejecuta la opcion.
                    if accion == "4":
                        break # Si se marca 4 se sale de la aplicacion.
                else:
                    print("Ingresa por favor una opcion del 1 al 4.")
        # Manejo de errores.
        except ValueError:
            print("Error de digitacion, ingresa una opcion correcta.")
    

    def ingreso_tarjeta(self, usuario_id): # se pasa "usuario_id" para bucar el id registrado.
        try:
            # Entrada de usuario.
            numero_tarjeta = input("Ingresa tu pan de tarjeta: ").strip()
            fecha_vencimiento = input("Ingresa la fecha de vencimiento de tu tarjeta: ").strip()
            codigo_seguridad = input("Ingresa el codigo de seguridad de tu tarjeta: ").strip()

            # Expresiones regulares para validar numero de tarjeta, fecha de vencimiento y CVV.
            validador_tarjeta = r"^(?:23[0-9]{14}|4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})$"
            validador_vencimiento = r"^(0[1-9]|1[0-2])\/\d{2}$"
            validador_cvv = r"^\d{3,4}$"

            # Validadot de campos.
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
            
            # Se verifica en la base de datos que el numero de la tarjeta no exista.
            self.conexion.cursor.execute("SELECT 1 FROM tarjeta_usuario WHERE numero_tarjeta = ?",(numero_tarjeta,))
            if self.conexion.cursor.fetchone():
                print("Tarjeta ya ingresada.")
                return
            
            # Se encripta el numero de la tarjeta, Fecha de vencimiento y CVVV.
            key = Fernet.generate_key()
            cipher = Fernet(key)
            encrypted_pan = cipher.encrypt(numero_tarjeta.encode())
            encrypted_expired = cipher.encrypt(fecha_vencimiento.encode())
            encrypted_cvv = cipher.encrypt(codigo_seguridad.encode())
            
            # Se agregan los datos de la taejta encriptados a la base de datos.
            self.conexion.cursor.execute("INSERT INTO tarjeta_usuario(numero_tarjeta,fecha_vencimiento,codigo_seguridad,usuario_id) VALUES(?,?,?,?)",(encrypted_pan,encrypted_expired,encrypted_cvv,usuario_id))
            self.conexion.conn.commit()
            print("Tarjeta ingresada de manera correcta.")
        
        # Manejo de errores.
        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}")
        except Exception as error:
            print(f"Error en el programa: {error}.")
    
    def reservar_vuelo(self, usuario_id): # se pasa "usuario_id" para bucar el id registrado.
        try:
            # Entrada de usuario. 
            pais_origen = input("Ingresa tu ciudad de origen: ").strip()
            pais_destino = input("Ingresa el ciudad destino: ").strip()
            fecha_vuelo = input("Ingresa la fecha de vuelo: ").strip()
            fecha_regreso = input("Ingresa la fecha de regreso: ").strip()

            # Validador de campos.
            if not all([pais_origen,pais_destino,fecha_vuelo,fecha_regreso]):
                print("Todos los datos deben estar completos.")
                return
            
            # Se ingresa la informacion sobre los vuelos a la base de datos.
            self.conexion.cursor.execute("INSERT INTO reserva_vuelos(pais_origen, pais_destino, fecha_vuelo, fecha_regreso, usuario_id) VALUES(?,?,?,?,?)",(pais_origen,pais_destino,fecha_vuelo,fecha_regreso,usuario_id))
            self.conexion.conn.commit()
            print("Reserva de vuelo ingresado exitosamente.")
        
        # Manejo de erroes.
        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}.")
        except Exception as error:
            print(f"Error en el programa: {error}.")
    
    def mostrar_vuelos(self, usuario_id): # se pasa "usuario_id" para bucar el id registrado.
        try:
            # Consulta para revisar los datos sobre el usuario y vuelo asignado.
            query = """
                    SELECT 
                    usuario.email_user,
                    reserva_vuelos.pais_origen,
                    reserva_vuelos.fecha_vuelo,
                    reserva_vuelos.pais_destino,
                    reserva_vuelos.fecha_regreso
                FROM usuario
                JOIN reserva_vuelos ON usuario.usuario_id = reserva_vuelos.usuario_id
                WHERE usuario.usuario_id = ?
                """
            # Muestra los datos seleccionados.
            resultado_df = pd.read_sql_query(query, self.conexion.conn, params=(usuario_id,))
            if not resultado_df.empty:
                print(resultado_df)
            else:
                print("No se encontraron vuelos o el usuario.")
        
        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}.")
    
    # Cada opcion guarda el id del usuario para mantener la sesion abierta para cada opcion.
    def opcion_uno(self):
        if not self.usuario_id:
            usuario_id = self.ingreso_usuario()
            if not usuario_id:
                return
        else:
            usuario_id = self.usuario_id
        self.ingreso_tarjeta(usuario_id)
    
    def opcion_dos(self):
        if not self.usuario_id:
            usuario_id = self.ingreso_usuario()
            if not usuario_id:
                return
        else:
            usuario_id = self.usuario_id
        self.reservar_vuelo(usuario_id)
    
    def opcion_tres(self):
        if not self.usuario_id:
            usuario_id = self.ingreso_usuario()
            if not usuario_id:
                return
        else:
            usuario_id = self.usuario_id
        self.mostrar_vuelos(usuario_id)
    
    # Cierra la sesion del usuario.
    def opcion_cuatro(self):
        self.usuario_id = False
        print("Sesion cerrada.")
        exit()