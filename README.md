# ✈️ Sistema de Reserva de Vuelos
compra_vuelos es una aplicación de consola desarrollada en Python que permite a los usuarios registrarse, iniciar sesión y reserva de vuelos. El sistema utiliza SQLite como base de datos y bcrypt para la gestión segura de contraseñas.

# 📌 Características

-Registro e Inicio de Sesión: Los usuarios pueden crear una cuenta y autenticarse de forma segura.
-Gestión de Vuelos: Permite la búsqueda, reserva de vuelos.
-Historial de Reservas: Los usuarios pueden consultar sus reservas anteriores.
-Seguridad: Las contraseñas se almacenan de forma segura utilizando hashing con bcrypt.
-Persistencia de Datos: Utiliza SQLite para almacenar la información de usuarios y vuelos.

# 🛠️ Tecnologías Utilizadas

-Python 3.x
-SQLite: Base de datos ligera y embebida.
-bcrypt: Biblioteca para el hashing de contraseñas.
-cryptography: Biblioteca para encriptar datos de la tarjeta de credito.
-pandas: Para la visualización y manipulación de datos en formato tabular.

# Uso

Al ejecutar index.py, se presentará un menú interactivo en la consola que permitirá:
1. Registrarse: Crear una nueva cuenta de usuario.
2. Iniciar Sesión: Acceder al sistema con credenciales existentes.
3. Buscar Vuelos: Consultar vuelos disponibles según criterios específicos.
4. Reservar Vuelos: Realizar reservas de vuelos seleccionados.
5. Comprar Vuelos: Completar la compra de vuelos reservados.
6. Consultar Historial: Ver las reservas y compras realizadas anteriormente.
7. Cerrar Sesión: Finalizar la sesión actual.

# 📌 Consideraciones

- Gestión de Sesiones: El sistema mantiene la sesión del usuario utilizando el password_id obtenido tras una autenticación exitosa.
- Validaciones: Se implementan validaciones para asegurar la integridad de los datos ingresados por el usuario.
- Manejo de Errores: Se han incorporado mecanismos para manejar errores comunes y proporcionar mensajes informativos al usuario.

 # 🤝 Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar el proyecto o corregir errores, por favor:
- Haz un fork del repositorio.
- Crea una nueva rama (git checkout -b feature/nueva-funcionalidad).
- Realiza tus cambios y haz commit (git commit -am 'Agrega nueva funcionalidad').
- Sube tus cambios (git push origin feature/nueva-funcionalidad).
- Abre un Pull Request detallando tus modificaciones.

# 📄 Licencia

Este proyecto está bajo la Licencia MIT. 

 
