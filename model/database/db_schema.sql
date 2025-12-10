-- NoteBox - Script de creación de base de datos y tablas
-- Universidad Tecnológica de Durango

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS notebox_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE notebox_db;

-- ============================================
-- TABLA: categorias
-- ============================================
CREATE TABLE IF NOT EXISTS categorias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT DEFAULT NULL,
    activo BOOLEAN DEFAULT TRUE, -- <-- NUEVA COLUMNA
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre),
    INDEX idx_activo (activo) -- <-- ÍNDICE PARA MEJORAR CONSULTAS FILTRANDO POR ACTIVO
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ============================================
-- TABLA: productos
-- ============================================
CREATE TABLE IF NOT EXISTS productos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT DEFAULT NULL,
    categoria_id INT DEFAULT NULL,
    stock INT NOT NULL DEFAULT 0,
    stock_minimo INT NOT NULL DEFAULT 5,
    precio DECIMAL(10, 2) NOT NULL,
    estado ENUM('Disponible', 'Stock Bajo', 'Agotado') DEFAULT 'Disponible',
    dias_sin_movimiento INT DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE, -- <-- NUEVA COLUMNA
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL,
    INDEX idx_codigo (codigo),
    INDEX idx_nombre (nombre),
    INDEX idx_categoria (categoria_id),
    INDEX idx_stock (stock),
    INDEX idx_estado (estado),
    INDEX idx_activo (activo) -- <-- ÍNDICE PARA MEJORAR CONSULTAS FILTRANDO POR ACTIVO
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ============================================
-- TABLA: usuarios
-- ============================================
CREATE TABLE IF NOT EXISTS usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    rol ENUM('Admin', 'Empleado') NOT NULL,
    estado ENUM('Activo', 'Inactivo') DEFAULT 'Activo', -- <-- ESTE ES EL ESTADO DEL USUARIO, NO UNA COLUMNA ACTIVO GENERAL
    ultimo_acceso DATETIME DEFAULT NULL,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_usuario (usuario),
    INDEX idx_rol (rol),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ============================================
-- TABLA: movimientos
-- ============================================
CREATE TABLE IF NOT EXISTS movimientos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo ENUM('Entrada', 'Salida') NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    motivo VARCHAR(255) NOT NULL,
    fecha DATETIME NOT NULL,
    usuario_id INT NOT NULL,
    notas TEXT DEFAULT NULL,
    fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE RESTRICT,
    INDEX idx_producto (producto_id),
    INDEX idx_tipo (tipo),
    INDEX idx_fecha (fecha),
    INDEX idx_usuario (usuario_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ============================================
-- TABLA: alertas
-- ============================================
CREATE TABLE IF NOT EXISTS alertas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo ENUM('Stock bajo', 'Producto agotado', 'Sin movimiento', 'Backup', 'Actualizacion', 'Recordatorio') NOT NULL,
    producto_id INT DEFAULT NULL,
    descripcion TEXT NOT NULL,
    fecha_alerta DATETIME DEFAULT CURRENT_TIMESTAMP,
    leida TINYINT(1) DEFAULT 0,
    usuario_id INT DEFAULT NULL,
    
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    INDEX idx_tipo (tipo),
    INDEX idx_leida (leida),
    INDEX idx_fecha (fecha_alerta)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ============================================
-- TABLA: configuracion
-- ============================================
CREATE TABLE IF NOT EXISTS configuracion (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre_negocio VARCHAR(255) DEFAULT 'Papeleria Valeria',
    tipo_negocio VARCHAR(100) DEFAULT 'Papeleria',
    moneda VARCHAR(10) DEFAULT 'MXN',
    direccion TEXT DEFAULT NULL,
    telefono VARCHAR(20) DEFAULT NULL,
    email_contacto VARCHAR(100) DEFAULT NULL,
    logo VARCHAR(255) DEFAULT NULL,
    color_primario VARCHAR(7) DEFAULT '#2C3E50',
    color_secundario VARCHAR(7) DEFAULT '#3498DB',
    backup_automatico TINYINT(1) DEFAULT 1,
    backup_frecuencia INT DEFAULT 24,
    ultimo_backup DATETIME DEFAULT NULL,
    version VARCHAR(20) DEFAULT 'v1.0.0',
    licencia VARCHAR(50) DEFAULT 'Profesional',
    limite_productos INT DEFAULT 2000,
    limite_usuarios INT DEFAULT 10,
    fecha_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ============================================
-- INSERTAR DATOS INICIALES
-- ============================================

-- Categorías (Agregamos 'activo' explícitamente para claridad)
INSERT INTO categorias (nombre, descripcion, activo) VALUES
('Cuadernos', 'Cuadernos de diferentes tamaños y tipos', TRUE),
('Lapices y Lapiceros', 'Utiles de escritura', TRUE),
('Plumas y Marcadores', 'Plumas, marcadores y resaltadores', TRUE),
('Papel', 'Diferentes tipos de papel', TRUE),
('Arte y Dibujo', 'Materiales para arte y dibujo', TRUE),
('Archivo y Organizacion', 'Carpetas, archivadores y organizadores', TRUE),
('Pegamento y Adhesivos', 'Pegamentos, cintas y adhesivos', TRUE),
('Calculadoras', 'Calculadoras de diferentes tipos', TRUE),
('Mochilas y Estuches', 'Mochilas, estuches y loncheras', TRUE),
('Otros', 'Otros productos de papelería', TRUE)
ON DUPLICATE KEY UPDATE nombre=nombre; -- Evita duplicados si se ejecuta de nuevo

-- Usuarios (con contraseñas hasheadas en SHA256)
INSERT INTO usuarios (usuario, contrasena, nombre, email, rol, estado) VALUES
('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Administrador', 'admin@notebox.com', 'Admin', 'Activo'),
('vendedor1', '1c142b2d01aa34e9a36bde480645a57fd69e14155dacfab5a3f9257b77fdc8d8', 'María González', 'maria@notebox.com', 'Empleado', 'Activo'),
('vendedor2', '1c142b2d01aa34e9a36bde480645a57fd69e14155dacfab5a3f9257b77fdc8d8', 'Carlos Rodríguez', 'carlos@notebox.com', 'Empleado', 'Activo'),
('almacen', 'c1c224b03cd9bc7b6a86d77f5dace40191766c485cd55dc48caf9ac873335d6f', 'Ana Martínez', 'ana@notebox.com', 'Empleado', 'Activo')
ON DUPLICATE KEY UPDATE usuario=usuario;

-- Productos de ejemplo (Agregamos 'activo' explícitamente)
INSERT INTO productos (codigo, nombre, descripcion, categoria_id, stock, stock_minimo, precio, estado, dias_sin_movimiento, activo) VALUES
('CUA-001', 'Cuaderno Profesional A4 100 hojas', NULL, 1, 150, 20, 45.50, 'Disponible', 2, TRUE),
('CUA-002', 'Cuaderno Scribe Rayas 200 hojas', NULL, 1, 8, 15, 85.00, 'Stock Bajo', 5, TRUE),
('CUA-003', 'Cuaderno Norma Cuadro Chico', NULL, 1, 0, 10, 38.00, 'Agotado', 15, TRUE),
('CUA-004', 'Cuaderno Disney A5 80 hojas', NULL, 1, 25, 12, 32.50, 'Disponible', 3, TRUE),
('LAP-001', 'Lapiz HB Mirado Paquete 12', NULL, 2, 45, 10, 25.00, 'Disponible', 1, TRUE),
('LAP-002', 'Lapicero Bic Cristal Azul Caja 20', NULL, 2, 8, 15, 45.00, 'Stock Bajo', 8, TRUE),
('LAP-003', 'Portaminas Pentel 0.5mm', NULL, 2, 15, 8, 35.00, 'Disponible', 4, TRUE),
('LAP-004', 'Lapices de Colores Prismacolor 12', NULL, 2, 5, 10, 120.00, 'Stock Bajo', 12, TRUE),
('PLU-001', 'Pluma Pilot G2 0.7 Negro', NULL, 3, 30, 10, 18.50, 'Disponible', 2, TRUE),
('PLU-002', 'Marcador Permanente Sharpie Negro', NULL, 3, 12, 8, 25.00, 'Disponible', 7, TRUE),
('PLU-003', 'Resaltador Stabilo Boss Amarillo', NULL, 3, 0, 15, 15.00, 'Agotado', 20, TRUE),
('PLU-004', 'Pluma Faber-Castell Fineliner Set 6', NULL, 3, 8, 10, 85.00, 'Stock Bajo', 10, TRUE),
('PAP-001', 'Papel Bond A4 500 hojas', NULL, 4, 120, 30, 95.00, 'Disponible', 1, TRUE),
('PAP-002', 'Papel Color A4 100 hojas', NULL, 4, 15, 20, 45.00, 'Stock Bajo', 8, TRUE),
('PAP-003', 'Papel Carta Oficio 250 hojas', NULL, 4, 0, 25, 65.00, 'Agotado', 25, TRUE),
('ART-001', 'Block Canson A3 20 hojas', NULL, 5, 18, 10, 85.00, 'Disponible', 15, TRUE),
('ART-002', 'Acuarelas Winsor 12 colores', NULL, 5, 5, 8, 150.00, 'Stock Bajo', 30, TRUE),
('ART-003', 'Pinceles Set Profesional 6', NULL, 5, 12, 5, 75.00, 'Disponible', 18, TRUE),
('PEG-001', 'Resistol 850 40g', NULL, 7, 25, 10, 12.00, 'Disponible', 3, TRUE),
('PEG-002', 'Pegamento en Barra Pritt 21g', NULL, 7, 8, 15, 8.50, 'Stock Bajo', 10, TRUE)
ON DUPLICATE KEY UPDATE codigo=codigo; -- Evita duplicados si se ejecuta de nuevo

-- Configuración inicial
INSERT INTO configuracion (
    nombre_negocio, tipo_negocio, moneda, direccion, telefono, 
    email_contacto, color_primario, color_secundario, version
) VALUES (
    'Papelería Valeria', 
    'Papeleria', 
    'MXN', 
    'Durango, México', 
    '+52 618 000 0000',
    'contacto@papeleriavaleria.com',
    '#2C3E50',
    '#3498DB',
    'v1.0.0'
)
ON DUPLICATE KEY UPDATE id=id; -- Evita duplicados si se ejecuta de nuevo

-- ============================================
-- VISTAS
-- ============================================

-- Vista de productos con información completa
CREATE OR REPLACE VIEW productos_completos AS
SELECT 
    p.id,
    p.codigo,
    p.nombre,
    p.descripcion,
    p.categoria_id,
    c.nombre AS categoria_nombre,
    p.stock,
    p.stock_minimo,
    p.precio,
    p.estado,
    p.dias_sin_movimiento,
    p.fecha_creacion,
    p.fecha_actualizacion,
    p.activo,
    (p.stock * p.precio) AS valor_inventario
FROM productos p
LEFT JOIN categorias c ON p.categoria_id = c.id;

-- Vista de alertas de stock (filtrando por productos activos)
CREATE OR REPLACE VIEW vista_alertas_stock AS
SELECT 
    p.id,
    p.codigo,
    p.nombre,
    c.nombre AS categoria,
    p.stock,
    p.stock_minimo,
    p.estado,
    (p.stock_minimo - p.stock) AS unidades_faltantes,
    p.dias_sin_movimiento
FROM productos p
LEFT JOIN categorias c ON p.categoria_id = c.id
WHERE p.activo = TRUE AND p.estado IN ('Stock Bajo', 'Agotado') OR p.dias_sin_movimiento > 30
ORDER BY p.estado DESC, p.stock ASC;

-- Vista de productos por categoría (filtrando por productos y categorías activas)
CREATE OR REPLACE VIEW productos_por_categoria AS
SELECT 
    c.nombre AS categoria,
    COUNT(p.id) AS total_productos,
    SUM(p.stock) AS total_unidades,
    SUM(p.stock * p.precio) AS valor_inventario
FROM categorias c
LEFT JOIN productos p ON c.id = p.categoria_id AND p.activo = TRUE
WHERE c.activo = TRUE
GROUP BY c.id, c.nombre
ORDER BY c.nombre ASC;

-- ============================================
-- PROCEDIMIENTOS ALMACENADOS (Ejemplos)
-- ============================================

-- Procedimiento para obtener resumen de inventario
DELIMITER $$
CREATE PROCEDURE sp_resumen_inventario()
BEGIN
    SELECT 
        COUNT(*) AS total_productos,
        SUM(CASE WHEN estado = 'Disponible' THEN 1 ELSE 0 END) AS productos_disponibles,
        SUM(CASE WHEN estado = 'Stock Bajo' THEN 1 ELSE 0 END) AS productos_stock_bajo,
        SUM(CASE WHEN estado = 'Agotado' THEN 1 ELSE 0 END) AS productos_agotados,
        SUM(stock) AS unidades_totales,
        SUM(stock * precio) AS valor_total_inventario,
        COUNT(CASE WHEN dias_sin_movimiento > 30 THEN 1 END) AS productos_sin_movimiento
    FROM productos
    WHERE activo = TRUE; -- Filtrar por productos activos
END$$
DELIMITER ;

-- ============================================
-- TRIGGERS (Disparadores)
-- ============================================

-- Trigger para actualizar automáticamente el estado del producto cuando cambia el stock
DELIMITER $$
CREATE TRIGGER trg_actualizar_estado_producto
BEFORE UPDATE ON productos
FOR EACH ROW
BEGIN
    -- Actualizar el estado basado en el nuevo stock
    IF NEW.stock = 0 THEN
        SET NEW.estado = 'Agotado';
    ELSEIF NEW.stock <= NEW.stock_minimo THEN
        SET NEW.estado = 'Stock Bajo';
    ELSE
        SET NEW.estado = 'Disponible';
    END IF;
END$$
DELIMITER ;

COMMIT;

-- Confirmar creación
SELECT 'Base de datos NoteBox creada exitosamente' AS mensaje;