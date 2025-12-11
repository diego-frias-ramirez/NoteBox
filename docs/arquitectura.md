Arquitectura del Sistema NoteBox
1. Introducción

Este documento describe la arquitectura del sistema NoteBox, una aplicación de gestión de inventario desarrollada para Papelería Valeria. El diseño sigue el patrón Modelo-Vista-Controlador (MVC), lo que permite una separación clara de responsabilidades y facilita el mantenimiento, la escalabilidad y las pruebas del sistema.

La arquitectura se divide en tres capas principales: Vista (View), Controlador (Controller) y Modelo (Model), complementadas por módulos auxiliares como utils y components. Esta estructura asegura que cada parte del sistema tenga una función bien definida.

2. Diagrama de Arquitectura
+-------------------+
|    Vista (View)   | <-----> Interacción con el Usuario
+-------------------+
          |
          v
+-------------------+
| Controlador (Ctrl)| <-----> Lógica de Negocio y Coordinación
+-------------------+
          |
          v
+-------------------+
|      Modelo       | <-----> Acceso a Datos y Reglas de Negocio
+-------------------+


Adicionalmente, la arquitectura incluye módulos de soporte:

components/: Componentes UI reutilizables (Header, Sidebar, BaseView).

utils/: Funciones auxiliares (Logger, Helpers, Alerts).

config/: Archivos de configuración del sistema.

exports/, logs/: Directorios para almacenar datos generados por el sistema.

3. Descripción de Capas
3.1 Capa de Vista (View)

La capa de vista se encarga de mostrar la interfaz gráfica al usuario utilizando CustomTkinter. Cada pantalla del sistema es una clase independiente.

Responsabilidades:

Presentar datos recibidos del controlador.

Capturar acciones del usuario.

Enviar eventos al controlador.

Gestionar la navegación entre vistas.

Ejemplos de clases:

view/login_view.py

view/dashboard_view.py

view/inventory_view.py

view/movements_view.py

view/reports_view.py

view/users_view.py

view/settings_view.py

view/help_view.py

view/notifications_view.py

view/splash_view.py

Componentes reutilizables:

components/base_view.py

components/header.py

components/sidebar.py

components/ia.py (componente experimental)

3.2 Capa de Controlador (Controller)

El controlador actúa como intermediario entre la vista y el modelo. Gestiona la lógica de negocio y coordina las operaciones.

Responsabilidades:

Recibir y validar datos provenientes de la vista.

Ejecutar la lógica de negocio.

Solicitar datos al modelo o modificar la base de datos.

Preparar la información para que la vista la muestre.

Administrar la sesión y autenticación.

Ejemplos de clases:

controller/login_controller.py

controller/dashboard_controller.py

controller/inventory_controller.py

controller/movements_controller.py

controller/reports_controller.py

controller/users_controller.py

controller/settings_controller.py

controller/notifications_controller.py

controller/splash_controller.py

3.3 Capa de Modelo (Model)

La capa de modelo administra los datos y contiene las reglas de negocio del sistema. Se comunica directamente con la base de datos MySQL.

Responsabilidades:

Definir entidades como Producto, Usuario, Movimiento o Categoría.

Implementar reglas de validación, cálculos y alertas.

Realizar operaciones CRUD en la base de datos.

Proveer métodos limpios para que el controlador interactúe con los datos.

Ejemplos de clases y archivos:

model/database/db_schema.sql

model/database.py

model/product_model.py

model/user_model.py

model/movement_model.py

model/alert_model.py

model/report_model.py

model/category_model.py

model/settings_model.py

3.4 Módulos Auxiliares
3.4.1 utils/

Contiene funciones y utilidades generales del sistema.

logger.py: Registro de eventos y errores.

helpers.py: Utilidades diversas (formateo, validaciones, rutas).

alerts.py: Manejo de alertas y notificaciones.

validators.py: Validaciones de datos (correos, contraseñas, campos requeridos).

3.4.2 components/

Componentes reutilizables de interfaz gráfica.

base_view.py: Estructura común para todas las vistas.

header.py: Barra de encabezado.

sidebar.py: Barra lateral.

3.4.3 config/

Archivos de configuración.

app_settings.json: Colores, rutas, apariencia.

db_config.json: Credenciales y parámetros de MySQL.

paths.json: Rutas de directorios principales.

3.4.4 assets/

Recursos estáticos del sistema.

icons/: Iconos.

images/: Imágenes generales.

styles/: Colores y fuentes (colors.py, fonts.py, themes.py).

4. Flujo de Datos

Ejemplo de flujo típico al crear un producto:

El usuario hace clic en “Guardar”.

La vista captura el evento y llama al método del controlador.

El controlador valida los datos y crea un objeto de producto.

El modelo inserta el producto en la base de datos y devuelve un resultado.

El controlador genera una alerta de movimiento.

La vista actualiza la tabla y muestra un mensaje de confirmación.

5. Tecnologías Utilizadas

Python 3.x

CustomTkinter

MySQL

PIL (Pillow)

matplotlib

tkcalendar (opcional)

6. Consideraciones de Seguridad

Autenticación mediante credenciales válidas.

Autorización basada en roles (Administrador y Empleado).

Validación de todos los datos ingresados por el usuario.

Registro de eventos críticos para auditoría.

7. Consideraciones de Escalabilidad

La arquitectura MVC permite añadir nuevas funcionalidades sin afectar el resto del sistema.

El uso de módulos bien definidos facilita el mantenimiento.

El sistema puede migrarse a una arquitectura cliente-servidor en el futuro.