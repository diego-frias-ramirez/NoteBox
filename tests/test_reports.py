"""
Test completo del módulo de reportes
Genera movimientos reales y valida los métodos del ReportsController
"""

# =======================================================
# FIX PARA IMPORTS DESDE CARPETA tests/
# =======================================================
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# =======================================================
# IMPORTS DEL PROYECTO
# =======================================================
from controller.reports_controller import ReportsController
from model.database import Database

import random
from datetime import datetime, timedelta


# Usuario administrador simulado
user_data = {"id": 1, "usuario": "admin", "rol": "Admin"}
controller = ReportsController(user_data)


# =======================================================
# 1. GENERAR MOVIMIENTOS DE PRUEBA
# =======================================================
def generate_test_movements(months=6, per_product=5):
    print("\n⏳ Generando movimientos de prueba...")

    # Obtener todos los productos
    products = Database.execute_query(
        "SELECT id, stock FROM productos WHERE activo = TRUE",
        fetch=True
    )

    if not products:
        print("❌ No hay productos en la base de datos.")
        return

    movimientos = []
    today = datetime.now()

    for prod in products:
        for _ in range(per_product):

            # Movimiento aleatorio dentro de los últimos X meses
            random_days = random.randint(0, months * 30)
            fecha_mov = today - timedelta(days=random_days)

            tipo = random.choice(["Entrada", "Salida"])
            cantidad = random.randint(5, 40)

            movimientos.append((
                tipo,
                prod["id"],
                cantidad,
                "Movimiento de prueba automática",
                fecha_mov.strftime("%Y-%m-%d %H:%M:%S"),
                1  # usuario admin
            ))

    # Insertar movimientos
    query = """
        INSERT INTO movimientos (tipo, producto_id, cantidad, motivo, fecha, usuario_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    for mov in movimientos:
        Database.execute_query(query, mov)

    print(f"✔ Se generaron {len(movimientos)} movimientos reales.")


# =======================================================
# 2. REPROCESAR STOCK SEGÚN MOVIMIENTOS
# =======================================================
def recalc_stock():
    print("\n🔄 Recalculando stock según movimientos...")

    query = """
        UPDATE productos p
        LEFT JOIN (
            SELECT 
                producto_id,
                SUM(CASE WHEN tipo='Entrada' THEN cantidad ELSE -cantidad END) AS mov
            FROM movimientos
            GROUP BY producto_id
        ) m ON p.id = m.producto_id
        SET p.stock = GREATEST(0, p.stock + IFNULL(m.mov, 0));
    """

    Database.execute_query(query)
    print("✔ Stock actualizado.")


# =======================================================
# 3. REPROCESAR DÍAS SIN MOVIMIENTO
# =======================================================
def recalc_days():
    print("\n📆 Recalculando días sin movimiento...")

    query = """
        UPDATE productos p
        LEFT JOIN (
            SELECT producto_id, MAX(fecha) AS ultima
            FROM movimientos
            GROUP BY producto_id
        ) m ON p.id = m.producto_id
        SET p.dias_sin_movimiento = 
            IF(m.ultima IS NULL, 999, DATEDIFF(CURDATE(), m.ultima));
    """

    Database.execute_query(query)
    print("✔ Días sin movimiento actualizados.")


# =======================================================
# 4. ACTUALIZAR ESTADO DE PRODUCTO
# =======================================================
def recalc_state():
    print("\n📦 Recalculando estado del producto...")

    query = """
        UPDATE productos
        SET estado =
            CASE
                WHEN stock = 0 THEN 'Agotado'
                WHEN stock <= stock_minimo THEN 'Stock Bajo'
                ELSE 'Disponible'
            END;
    """

    Database.execute_query(query)
    print("✔ Estado de productos recalculado.")


# =======================================================
# 5. PROBAR TODOS LOS REPORTES
# =======================================================
def run_all_reports():
    print("\n📊 Probando todos los reportes...\n")

    print("🔹 Métricas del Inventario:")
    print(controller.get_inventory_metrics())

    print("\n🔹 Productos de baja rotación:")
    print(controller.get_low_rotation_products())

    print("\n🔹 Distribución por categoría:")
    print(controller.get_category_distribution())

    print("\n🔹 Evolución del inventario (6 meses):")
    print(controller.get_inventory_evolution(6))


# =======================================================
# EJECUCIÓN GENERAL DEL TEST
# =======================================================
if __name__ == "__main__":
    print("\n🚀 INICIANDO TEST COMPLETO DE REPORTES...\n")

    generate_test_movements(months=6, per_product=5)
    recalc_stock()
    recalc_days()
    recalc_state()

    run_all_reports()

    print("\n🎉 TEST FINALIZADO — TODO FUNCIONANDO\n")
