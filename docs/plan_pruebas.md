Plan de Pruebas
NoteBox – Sistema de Gestión de Inventario
1. Introducción

Este documento describe el plan de pruebas para el sistema NoteBox, una aplicación de gestión de inventario desarrollada para Papelería Valeria. Su propósito es garantizar que el sistema cumpla con los requisitos funcionales, no funcionales y de usabilidad, asegurando estabilidad, seguridad y eficiencia antes del despliegue.

1.1 Objetivos del Plan de Pruebas

Verificar que todas las funcionalidades operen según lo especificado.

Identificar y reportar defectos antes del lanzamiento.

Validar la integridad y consistencia de los datos.

Asegurar la facilidad de uso y navegación del sistema.

Confirmar la robustez del sistema frente a casos de uso normales y excepcionales.

1.2 Alcance

Este plan cubre:

Pruebas Unitarias: Funciones en los módulos model, controller y utils.

Pruebas de Integración: Interacción entre componentes (vista–controlador–modelo).

Pruebas de Sistema: Evaluación del sistema completo.

Pruebas de Aceptación: Validación por parte del cliente.

Pruebas de Rendimiento (básicas): Tiempos de carga y respuesta.

Pruebas de Seguridad (básicas): Autenticación y autorización.

1.3 Exclusiones

Pruebas de carga o estrés intensivas.

Compatibilidad con múltiples sistemas operativos o versiones de Python.

Pruebas de accesibilidad WCAG completas (solo revisiones básicas).

1.4 Responsables

Equipo de Desarrollo: Pruebas unitarias e integración.

Tester / QA: Pruebas de sistema y aceptación.

Cliente: Validación de aceptación y usabilidad.

1.5 Entregables

Informe de Pruebas.

Registro de Defectos (Bug Report).

Resumen Final de Calidad.

2. Estrategia de Pruebas
2.1 Tipos de Pruebas
Tipo de Prueba	Descripción	Responsable
Unitaria	Validación de funciones individuales (por ejemplo, create_product(), format_currency()).	Equipo de Desarrollo
Integración	Verificación de interacción entre módulos (por ejemplo, LoginView → LoginController → UserModel).	Equipo de Desarrollo
Sistema	Pruebas completas desde interfaz hasta base de datos.	Tester / QA
Aceptación	Validación contra los requisitos del negocio.	Cliente / Tester
Usabilidad	Evaluación de navegación e interfaz.	Tester / Cliente
Seguridad	Validación de autenticación y permisos.	Tester
2.2 Enfoque de Pruebas

Basado en Requisitos: Todos los casos se diseñarán según especificaciones funcionales.

Basado en Riesgo: Priorización en módulos críticos (Login, Movimientos, Reportes).

Automatización Parcial: Scripts para pruebas repetitivas (por ejemplo, creación masiva de productos).

2.3 Herramientas

Unittest / Pytest: Pruebas unitarias e integración.

CustomTkinter / Tkinter: Pruebas manuales de UI.

MySQL Workbench / phpMyAdmin: Validación de base de datos.

Gestión de Defectos: Hoja de cálculo, Jira o Trello.

3. Casos de Prueba
3.1 Módulo de Login (view/login_view.py)
ID	Caso de Prueba	Paso a Paso	Resultado Esperado	Prioridad
LT-01	Inicio de sesión exitoso	1. Ingresar usuario válido. 2. Ingresar contraseña válida. 3. Clic en "INGRESAR".	Redirigir al Dashboard. Mostrar mensaje de bienvenida.	Alta
LT-02	Inicio fallido	1. Ingresar usuario incorrecto. 2. Ingresar contraseña incorrecta. 3. Clic en "INGRESAR".	Mostrar mensaje de error. No redirigir.	Alta
LT-03	Recordar usuario	1. Activar la opción. 2. Iniciar sesión. 3. Reiniciar aplicación.	El usuario se autocompleta.	Media
LT-04	Olvidó contraseña	1. Clic en la opción correspondiente.	Mostrar mensaje de contacto con administrador.	Baja
3.2 Módulo de Dashboard (view/dashboard_view.py)
ID	Caso de Prueba	Paso a Paso	Resultado Esperado	Prioridad
DB-01	Cargar datos	1. Iniciar sesión.	Estadísticas, gráficos y alertas cargan correctamente.	Alta
DB-02	Navegación	1. Clic en “Ver todas las alertas”.	Redirige a Inventario.	Media
DB-03	Visualización de alertas	1. Ver panel de alertas.	Muestra productos con alertas. Colores correctos.	Alta
3.3 Módulo de Inventario (view/inventory_view.py)
ID	Caso de Prueba	Paso a Paso	Resultado Esperado	Prioridad
IV-01	Agregar producto	1. Clic en “Añadir Producto”. 2. Completar campos. 3. Guardar.	Aparece en tabla. Genera alerta.	Alta
IV-02	Editar producto	1. Seleccionar producto. 2. Modificar datos. 3. Guardar.	Cambios visibles.	Alta
IV-03	Eliminar producto	1. Seleccionar producto. 2. Confirmar eliminación.	Se elimina de la tabla.	Alta
IV-04	Filtrar por categoría	1. Seleccionar categoría.	Muestra productos filtrados.	Alta
IV-05	Exportar inventario	1. Clic en “Exportar”. 2. Guardar archivo.	Genera CSV.	Media
3.4 Módulo de Movimientos (view/movements_view.py)
ID	Caso de Prueba	Paso a Paso	Resultado Esperado	Prioridad
MV-01	Registrar entrada	Ingresar producto y datos. Guardar.	Stock aumenta. Historial registra.	Alta
MV-02	Registrar salida	Seleccionar producto con stock. Guardar.	Stock disminuye. Registro guardado.	Alta
MV-03	Salida con stock insuficiente	Registrar salida mayor al stock.	Mostrar error y no registrar.	Alta
MV-04	Ver movimientos	Clic en “Ver todos”.	Mostrar tabla con historial.	Media
MV-05	Exportar movimientos	Guardar archivo.	Genera CSV.	Media
3.5 Módulo de Reportes (view/reports_view.py)
ID	Caso de Prueba	Paso a Paso	Resultado Esperado	Prioridad
RP-01	Reporte PDF	Seleccionar rango, generar PDF.	Archivo generado correctamente.	Media
RP-02	Reporte Excel	Seleccionar rango, generar Excel.	Archivo generado correctamente.	Media
RP-03	Actualizar gráfico	Clic en actualizar.	Gráfico se recarga.	Media
RP-04	Informe de baja rotación	Clic en opción.	Muestra tabla con productos sin movimiento.	Media
3.6 Módulo de Usuarios (view/users_view.py)
ID	Caso de Prueba	Paso a Paso	Resultado Esperado	Prioridad
US-01	Crear usuario	Completar formulario. Guardar.	Usuario aparece en tabla.	Alta
US-02	Editar usuario	Seleccionar usuario. Modificar datos. Guardar.	Cambios guardados.	Alta
US-03	Cambiar estado	Cambiar estado activo/inactivo.	Actualización correcta.	Alta
US-04	Eliminar usuario	Confirmar eliminación.	Usuario eliminado.	Alta
3.7 Módulo de Configuración (view/settings_view.py)
ID	Caso de Prueba	Paso a Paso	Resultado Esperado	Prioridad
ST-01	Guardar datos de empresa	Modificar información y guardar.	Cambios persistentes.	Media
ST-02	Crear backup	Seleccionar ubicación y guardar.	Genera archivo .sql.	Alta
ST-03	Restaurar imagen por defecto	Confirmar restauración.	Imagen vuelve a valores por defecto.	Media
3.8 Módulo de Notificaciones (view/notifications_view.py)
ID	Caso de Prueba	Paso a Paso	Resultado Esperado	Prioridad
NT-01	Marcar como leída	Seleccionar notificación.	Cambia estado a leída.	Media
NT-02	Marcar todas como leídas	Ejecutar acción global.	Todas marcadas como leídas.	Media
NT-03	Limpiar antiguas	Confirmar limpieza.	Elimina notificaciones con más de 30 días.	Media
3.9 Módulo de Ayuda (view/help_view.py)
ID	Caso de Prueba	Paso a Paso	Resultado Esperado	Prioridad
HP-01	Abrir manual	Clic en “Ver Manual”.	Abre archivo PDF.	Media
HP-02	Ver contacto	Clic en contacto.	Muestra datos de contacto.	Baja
4. Ejecución de Pruebas
4.1 Preparación

Instalar Python 3.x y dependencias.

Configurar base de datos con db_schema.sql.

Crear datos de prueba iniciales.

4.2 Ciclos de Pruebas

Ciclo 1: Pruebas unitarias e integración (Desarrollo).

Ciclo 2: Pruebas de sistema y usabilidad (QA).

Ciclo 3: Aceptación final (Cliente).

4.3 Reporte de Defectos

Cada defecto debe incluir:

ID del Bug

Título

Descripción

Pasos de reproducción

Resultado actual

Resultado esperado

Prioridad

Gravedad

Evidencia (opcional)

5. Criterios de Salida

100% de casos de prueba ejecutados.

Defectos críticos y de alta prioridad resueltos.

Sin errores bloqueantes.

Aprobación final del cliente.