Registro de Cambios (Changelog) - NoteBox

Este documento registra los cambios significativos en cada versión del sistema NoteBox. Sigue el formato Semantic Versioning 2.0.0.

[v1.0.0]
Lanzamiento Inicial

Primera versión estable del sistema NoteBox, diseñada específicamente para Papelería Valeria. El sistema está completo y listo para su uso en producción.

Nuevas Funcionalidades

Módulo de Login: autenticación, recordar usuario y recuperación de contraseña.

Dashboard Principal: estadísticas clave, gráfico de inventario por categoría y panel de alertas.

Gestión de Inventario: agregar, editar, eliminar y buscar productos; filtros, paginación y búsqueda global.

Movimientos de Inventario: registro de entradas y salidas con validación de stock, historial y exportación.

Generación de Reportes: exportación en PDF y Excel con gráficos de evolución y distribución por categoría.

Gestión de Usuarios: creación, edición, eliminación y administración de roles (Administrador/Empleado).

Notificaciones del Sistema: visualización, marcado y limpieza de alertas sobre stock y movimientos.

Configuración del Sistema: personalización de datos de empresa, colores y backups automáticos.

Centro de Ayuda: manuales, contacto y soporte técnico.

Splash Screen: pantalla de carga inicial con animación y verificación de dependencias.

Correcciones de Errores

Correcciones en navegación entre vistas.

Solución de problemas de carga de imágenes e íconos.

Mejora en la gestión de sesiones y usuarios no autenticados.

Reparación de errores en exportación de datos (CSV, PDF, Excel) y generación de backups.

Corrección del comportamiento de filtros en Inventario.

Mejoras de Rendimiento y Seguridad

Optimización de consultas a base de datos.

Validaciones de entrada para prevenir inyecciones y datos inválidos.

Refactorización para mejorar legibilidad y mantenibilidad.

Implementación de logging detallado para depuración.

Documentación

Creación de README.md con descripción general e instalación.

Generación de plan_pruebas.md.

Actualización de documentación interna sobre arquitectura y plan de pruebas.

[v0.9.0]
Versión de Prueba

Versión preliminar para pruebas internas y validación de funcionalidades básicas.

Nuevas Funcionalidades

Implementación inicial de vistas principales (Login, Dashboard, Inventario, Movimientos, Reportes, Usuarios, Notificaciones, Configuración y Ayuda).

Integración inicial con MySQL.

Diseño gráfico con CustomTkinter.

Correcciones de Errores

Solución de fallos críticos en inicio de sesión y carga de datos.

Corrección de errores visuales en componentes gráficos.

Mejoras

Organización del proyecto en módulos (model, view, controller, utils, components).

Sistema básico de alertas y notificaciones.

Sistema básico de logging.

[v0.8.0]
Versión de Desarrollo Inicial

Primera versión funcional con vistas base y estructura definida.

Nuevas Funcionalidades

Creación de estructura inicial del proyecto.

Implementación de Login y Dashboard.

Conexión básica con la base de datos.

Vista de Inventario con funciones CRUD básicas.

[v0.7.0]
Versión de Prototipo

Prototipo inicial para validación de arquitectura y flujo general.

Nuevas Funcionalidades

Definición de arquitectura (MVC).

Creación de modelos y controladores iniciales.

Implementación de Login y Dashboard con datos estáticos.