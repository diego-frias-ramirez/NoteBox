from database import Database

class ProductController:
    def __init__(self):
        self.db = Database()
        self.db.connect()
    
    def crear_producto(self, nombre_producto, stock, proveedor, precio, status, marca, descripcion):
        """
        Crea un nuevo producto
        Retorna: (éxito: bool, mensaje: str)
        """
        if not all([nombre_producto, stock, proveedor, precio]):
            return (False, "Los campos nombre, stock, proveedor y precio son obligatorios")
        
        try:
            stock = int(stock)
            precio = int(precio)
            status = int(status) if status else 1
        except ValueError:
            return (False, "Stock, precio y status deben ser números")
        
        query = """
            INSERT INTO productos (nombre_producto, stock, proveedor, precio, status, marca, descripcion) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        if self.db.execute_query(query, (nombre_producto, stock, proveedor, precio, status, marca, descripcion)):
            return (True, "Producto creado exitosamente")
        else:
            return (False, "Error al crear producto")
    
    def obtener_productos(self):
        """
        Obtiene todos los productos
        Retorna: lista de diccionarios con datos de productos
        """
        query = "SELECT * FROM productos"
        return self.db.fetch_all(query)
    
    def obtener_producto(self, id_producto):
        """
        Obtiene un producto por ID
        Retorna: diccionario con datos del producto o None
        """
        query = "SELECT * FROM productos WHERE id_producto = %s"
        return self.db.fetch_one(query, (id_producto,))
    
    def modificar_producto(self, id_producto, nombre_producto, stock, proveedor, precio, status, marca, descripcion):
        """
        Modifica un producto existente
        Retorna: (éxito: bool, mensaje: str)
        """
        if not all([id_producto, nombre_producto, stock, proveedor, precio]):
            return (False, "Los campos nombre, stock, proveedor y precio son obligatorios")
        
        try:
            stock = int(stock)
            precio = int(precio)
            status = int(status) if status else 1
        except ValueError:
            return (False, "Stock, precio y status deben ser números")
        
        query = """
            UPDATE productos 
            SET nombre_producto = %s, stock = %s, proveedor = %s, precio = %s, 
                status = %s, marca = %s, descripcion = %s
            WHERE id_producto = %s
        """
        
        if self.db.execute_query(query, (nombre_producto, stock, proveedor, precio, status, marca, descripcion, id_producto)):
            return (True, "Producto modificado exitosamente")
        else:
            return (False, "Error al modificar producto")
    
    def eliminar_producto(self, id_producto):
        """
        Elimina un producto
        Retorna: (éxito: bool, mensaje: str)
        """
        if not id_producto:
            return (False, "ID de producto no válido")
        
        query = "DELETE FROM productos WHERE id_producto = %s"
        
        if self.db.execute_query(query, (id_producto,)):
            return (True, "Producto eliminado exitosamente")
        else:
            return (False, "Error al eliminar producto")
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        self.db.disconnect()