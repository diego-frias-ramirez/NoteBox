NoteBox: Sistema de Gestión de Inventario
Descripción

NoteBox es un sistema de gestión de inventario desarrollado para Papelería Valeria. Su objetivo es modernizar y optimizar el control de inventarios, reemplazando procesos manuales mediante una solución tecnológica accesible, eficiente y fácil de usar.

El sistema permite administrar productos, registrar movimientos de entrada y salida, generar reportes, gestionar usuarios y recibir alertas automáticas sobre el estado del inventario.

Características Principales
Dashboard Principal

Resumen general del estado del inventario, estadísticas clave, gráficos y alertas activas.

Gestión de Inventario

Alta, baja y modificación de productos.

Filtros por categoría, búsqueda y ordenamiento avanzado.

Movimientos de Inventario

Registro de entradas (compras) y salidas (ventas).

Historial completo de movimientos.

Resumen diario.

Generación de Reportes

Exportación en PDF y Excel.

Gráficos de evolución y distribución por categoría.

Alertas y Notificaciones

Alertas automáticas para:

Stock bajo

Productos agotados

Movimientos recientes

Gestión de Usuarios

Creación, edición y eliminación de cuentas con roles:

Administrador

Empleado

Configuración del Sistema

Personalización de:

Datos de la empresa

Colores de interfaz

Configuración de copias de seguridad automáticas

Ayuda y Soporte

Incluye manuales, información de contacto y centro de soporte técnico.

Tecnologías Utilizadas

Lenguaje de Programación: Python 3.x

Interfaz Gráfica: CustomTkinter (basado en Tkinter)

Base de Datos: MySQL

Librerías Adicionales: PIL (Pillow), matplotlib, tkcalendar (opcional)

Estructura del Proyecto
NoteBox/
├── assets/              # Imágenes, iconos y elementos gráficos
├── components/          # Componentes reutilizables de la UI (Header, Sidebar, BaseView)
├── config/              # Configuraciones generales y de base de datos
├── controller/          # Lógica de negocio y manejo de interacciones
├── docs/                # Documentación del proyecto
├── exports/             # Backups, logs y reportes generados
├── logs/                # Registros del sistema
├── model/               # Modelos y esquema de base de datos
└── main.py              # Archivo principal de ejecución

Instalación y Ejecución
1. Clonar el repositorio
git clone <url-del-repositorio>
cd NoteBox

2. Instalar dependencias
pip install -r requirements.txt

3. Configurar la base de datos

Asegúrate de tener un servidor MySQL en ejecución.

Importa el archivo:

model/database/db_schema.sql


Configura las credenciales en:

config/db_config.json

4. Ejecutar la aplicación
python main.py

Uso

Al iniciar la aplicación se mostrará la pantalla de inicio de sesión.
Una vez autenticado, el usuario puede navegar entre los módulos mediante la barra lateral.

Contribuciones

Las contribuciones son bienvenidas. Para proponer cambios, crear un Pull Request siguiendo las buenas prácticas del repositorio.

Licencia

Este proyecto está licenciado bajo la Licencia MIT. Para más información consulte el archivo LICENSE.