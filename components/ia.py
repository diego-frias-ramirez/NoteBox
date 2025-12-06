"""
NoteBox - Módulo de Chat AI Mejorado
Ubicación: components/ia.py
"""

import customtkinter as ctk
from datetime import datetime
import threading
from model.database import Database


class ChatAIWindow(ctk.CTkToplevel):
    """Ventana de Chat AI con acceso a la base de datos."""

    def __init__(self, parent, user_data):
        super().__init__(parent)
        
        self.user_data = user_data
        self.chat_history = []
        self.is_processing = False
        
        # Configuración de la ventana
        self.title("💬 Chat AI - NoteBox Assistant")
        self.geometry("900x650")
        
        # Centrar ventana
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 900) // 2
        y = (self.winfo_screenheight() - 650) // 2
        self.geometry(f"900x650+{x}+{y}")
        
        # Configurar para que aparezca al frente
        self.lift()
        self.focus_force()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))
        
        # Configurar colores (turquesa/cyan)
        self.colors = {
            "bg": "#F0F9FF",
            "chat_bg": "#FFFFFF",
            "user_msg": "#00B4D8",
            "ai_msg": "#E0F2FE",
            "user_text": "#FFFFFF",
            "ai_text": "#0C4A6E",
            "input_bg": "#FFFFFF",
            "button": "#00B4D8",
            "button_hover": "#0096C7",
            "header": "#00B4D8",
            "typing": "#BAE6FD"
        }
        
        self.configure(fg_color=self.colors["bg"])
        
        self.create_ui()
        self.send_welcome_message()
        
        # Vincular evento de cierre
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_ui(self):
        """Crea la interfaz del chat."""
        
        # ===== HEADER =====
        header = ctk.CTkFrame(self, fg_color=self.colors["header"], height=70, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        
        # Contenedor izquierdo (título)
        left_container = ctk.CTkFrame(header, fg_color="transparent")
        left_container.pack(side="left", fill="y", padx=20, pady=10)
        
        title_label = ctk.CTkLabel(
            left_container,
            text="💬 Chat AI",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="#FFFFFF"
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(
            left_container,
            text="Tu asistente inteligente de NoteBox",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#E0F2FE"
        )
        subtitle_label.pack(anchor="w")
        
        # Contenedor derecho (botones de acción)
        right_container = ctk.CTkFrame(header, fg_color="transparent")
        right_container.pack(side="right", padx=20, pady=15)
        
        # Botón limpiar chat
        clear_btn = ctk.CTkButton(
            right_container,
            text="🗑️ Limpiar",
            width=100,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#0C4A6E",
            hover_color="#075985",
            corner_radius=8,
            command=self.clear_chat
        )
        clear_btn.pack(side="left", padx=5)
        
        # Botón ayuda
        help_btn = ctk.CTkButton(
            right_container,
            text="❓ Ayuda",
            width=100,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#0C4A6E",
            hover_color="#075985",
            corner_radius=8,
            command=self.show_help
        )
        help_btn.pack(side="left", padx=5)
        
        # ===== ÁREA DE CHAT =====
        chat_container = ctk.CTkFrame(self, fg_color=self.colors["bg"])
        chat_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ScrollableFrame para mensajes
        self.chat_frame = ctk.CTkScrollableFrame(
            chat_container,
            fg_color=self.colors["chat_bg"],
            corner_radius=15,
            border_width=2,
            border_color="#BAE6FD"
        )
        self.chat_frame.pack(fill="both", expand=True)
        
        # ===== ÁREA DE INPUT =====
        input_container = ctk.CTkFrame(self, fg_color=self.colors["bg"], height=90)
        input_container.pack(fill="x", side="bottom", padx=20, pady=(0, 20))
        input_container.pack_propagate(False)
        
        input_frame = ctk.CTkFrame(
            input_container,
            fg_color=self.colors["input_bg"],
            corner_radius=15,
            border_width=2,
            border_color="#BAE6FD"
        )
        input_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Entry de texto
        self.input_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Escribe tu pregunta aquí... (Ej: ¿Cuántos productos hay?)",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_width=0,
            height=50
        )
        self.input_entry.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        self.input_entry.bind("<Return>", lambda e: self.send_message())
        
        # Botón enviar
        self.send_btn = ctk.CTkButton(
            input_frame,
            text="Enviar ➤",
            width=120,
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors["button"],
            hover_color=self.colors["button_hover"],
            corner_radius=10,
            command=self.send_message
        )
        self.send_btn.pack(side="right", padx=15, pady=10)

    def send_welcome_message(self):
        """Envía mensaje de bienvenida."""
        welcome_text = f"¡Hola {self.user_data.get('nombre', 'Usuario')}! 👋\n\n"
        welcome_text += "Soy tu asistente inteligente de NoteBox. Puedo ayudarte con:\n\n"
        welcome_text += "📦 **Inventario y Productos**\n"
        welcome_text += "   • Total de productos, stock bajo, agotados\n"
        welcome_text += "   • Valor del inventario\n\n"
        welcome_text += "🔄 **Movimientos**\n"
        welcome_text += "   • Últimos movimientos, movimientos del día\n"
        welcome_text += "   • Estadísticas mensuales\n\n"
        welcome_text += "👥 **Usuarios**\n"
        welcome_text += "   • Información de usuarios y roles\n\n"
        welcome_text += "⚠️ **Alertas**\n"
        welcome_text += "   • Alertas pendientes del sistema\n\n"
        welcome_text += "📁 **Categorías**\n"
        welcome_text += "   • Productos por categoría\n\n"
        welcome_text += "💡 Escribe 'ayuda' para ver ejemplos de preguntas."
        
        self.add_message(welcome_text, is_user=False)

    def add_message(self, text, is_user=True):
        """Agrega un mensaje al chat."""
        
        # Frame contenedor del mensaje
        msg_container = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        msg_container.pack(fill="x", padx=15, pady=8)
        
        if is_user:
            # Mensaje del usuario (derecha, turquesa)
            msg_frame = ctk.CTkFrame(
                msg_container,
                fg_color=self.colors["user_msg"],
                corner_radius=20
            )
            msg_frame.pack(side="right", padx=5, pady=2)
            
            msg_label = ctk.CTkLabel(
                msg_frame,
                text=text,
                font=ctk.CTkFont(size=14),
                text_color=self.colors["user_text"],
                wraplength=500,
                justify="left"
            )
            msg_label.pack(padx=20, pady=12)
            
        else:
            # Mensaje de la IA (izquierda, azul claro)
            container = ctk.CTkFrame(msg_container, fg_color="transparent")
            container.pack(side="left", fill="x", expand=True)
            
            # Icono de IA
            icon_frame = ctk.CTkFrame(container, fg_color=self.colors["button"], width=40, height=40, corner_radius=20)
            icon_frame.pack(side="left", padx=(0, 10))
            icon_frame.pack_propagate(False)
            
            icon_label = ctk.CTkLabel(
                icon_frame,
                text="🤖",
                font=ctk.CTkFont(size=20)
            )
            icon_label.place(relx=0.5, rely=0.5, anchor="center")
            
            msg_frame = ctk.CTkFrame(
                container,
                fg_color=self.colors["ai_msg"],
                corner_radius=20
            )
            msg_frame.pack(side="left", fill="x", expand=True, padx=5, pady=2)
            
            msg_label = ctk.CTkLabel(
                msg_frame,
                text=text,
                font=ctk.CTkFont(size=14),
                text_color=self.colors["ai_text"],
                wraplength=600,
                justify="left"
            )
            msg_label.pack(padx=20, pady=12, anchor="w")
        
        # Scroll al final
        self.chat_frame._parent_canvas.yview_moveto(1.0)

    def send_message(self):
        """Envía un mensaje del usuario."""
        if self.is_processing:
            return
            
        message = self.input_entry.get().strip()
        
        if not message:
            return
        
        # Agregar mensaje del usuario
        self.add_message(message, is_user=True)
        self.input_entry.delete(0, "end")
        
        # Deshabilitar entrada mientras procesa
        self.is_processing = True
        self.input_entry.configure(state="disabled")
        self.send_btn.configure(state="disabled", text="Procesando...")
        
        # Mostrar indicador de escritura
        self.add_typing_indicator()
        
        # Procesar mensaje en segundo plano
        thread = threading.Thread(target=self.process_message, args=(message,))
        thread.daemon = True
        thread.start()

    def add_typing_indicator(self):
        """Muestra indicador de 'escribiendo...'."""
        self.typing_frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        self.typing_frame.pack(fill="x", padx=15, pady=8)
        
        container = ctk.CTkFrame(self.typing_frame, fg_color="transparent")
        container.pack(side="left")
        
        # Icono de IA
        icon_frame = ctk.CTkFrame(container, fg_color=self.colors["button"], width=40, height=40, corner_radius=20)
        icon_frame.pack(side="left", padx=(0, 10))
        icon_frame.pack_propagate(False)
        
        icon_label = ctk.CTkLabel(icon_frame, text="🤖", font=ctk.CTkFont(size=20))
        icon_label.place(relx=0.5, rely=0.5, anchor="center")
        
        indicator = ctk.CTkFrame(
            container,
            fg_color=self.colors["typing"],
            corner_radius=20
        )
        indicator.pack(side="left", padx=5, pady=2)
        
        typing_label = ctk.CTkLabel(
            indicator,
            text="⚡ Analizando tu consulta...",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["ai_text"]
        )
        typing_label.pack(padx=20, pady=12)

    def remove_typing_indicator(self):
        """Elimina el indicador de escritura."""
        if hasattr(self, 'typing_frame'):
            self.typing_frame.destroy()

    def process_message(self, message):
        """Procesa el mensaje y genera respuesta."""
        import time
        time.sleep(0.8)  # Simular procesamiento
        
        response = self.generate_response(message)
        
        # Actualizar UI en el hilo principal
        self.after(0, self.remove_typing_indicator)
        self.after(0, lambda: self.add_message(response, is_user=False))
        self.after(0, self.enable_input)

    def enable_input(self):
        """Habilita el input después de procesar."""
        self.is_processing = False
        self.input_entry.configure(state="normal")
        self.send_btn.configure(state="normal", text="Enviar ➤")
        self.input_entry.focus()

    def clear_chat(self):
        """Limpia todo el chat."""
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        self.chat_history = []
        self.send_welcome_message()

    def show_help(self):
        """Muestra información de ayuda."""
        self.add_message("ayuda", is_user=True)
        help_response = self.get_help_info()
        self.after(500, lambda: self.add_message(help_response, is_user=False))

    def on_closing(self):
        """Maneja el cierre de la ventana."""
        self.destroy()

    def generate_response(self, message):
        """Genera respuesta basada en el mensaje del usuario."""
        message_lower = message.lower()
        
        try:
            # ===== CONSULTAS DE PRODUCTOS =====
            if any(word in message_lower for word in ["producto", "inventario", "stock", "cuántos productos", "cuantos productos"]):
                
                if "bajo" in message_lower or "mínimo" in message_lower or "minimo" in message_lower:
                    return self.get_low_stock_products()
                
                elif "agotado" in message_lower:
                    return self.get_out_of_stock_products()
                
                elif "total" in message_lower or "cuántos" in message_lower or "cuantos" in message_lower:
                    return self.get_total_products()
                
                elif "valor" in message_lower or "precio" in message_lower or "dinero" in message_lower:
                    return self.get_inventory_value()
                
                else:
                    return self.get_products_summary()
            
            # ===== CONSULTAS DE MOVIMIENTOS =====
            elif any(word in message_lower for word in ["movimiento", "entrada", "salida", "transacción", "transaccion"]):
                
                if "últimos" in message_lower or "ultimos" in message_lower or "recientes" in message_lower:
                    return self.get_recent_movements()
                
                elif "hoy" in message_lower or "día" in message_lower or "dia" in message_lower:
                    return self.get_today_movements()
                
                else:
                    return self.get_movements_summary()
            
            # ===== CONSULTAS DE USUARIOS =====
            elif any(word in message_lower for word in ["usuario", "usuarios", "empleado", "personal", "equipo"]):
                return self.get_users_info()
            
            # ===== CONSULTAS DE ALERTAS =====
            elif any(word in message_lower for word in ["alerta", "notificación", "notificacion", "aviso", "pendiente"]):
                return self.get_alerts_info()
            
            # ===== CONSULTAS DE CATEGORÍAS =====
            elif "categoría" in message_lower or "categoria" in message_lower or "categorias" in message_lower:
                return self.get_categories_info()
            
            # ===== ESTADÍSTICAS GENERALES =====
            elif any(word in message_lower for word in ["resumen", "estadística", "estadistica", "reporte", "general"]):
                return self.get_general_stats()
            
            # ===== AYUDA =====
            elif "ayuda" in message_lower or "qué puedes hacer" in message_lower or "que puedes hacer" in message_lower:
                return self.get_help_info()
            
            # ===== SALUDOS =====
            elif any(word in message_lower for word in ["hola", "buenos días", "buenas tardes", "buenas noches", "hey"]):
                return f"¡Hola {self.user_data.get('nombre', 'Usuario')}! 😊\n\n¿En qué puedo ayudarte hoy?\n\nEscribe 'ayuda' para ver lo que puedo hacer."
            
            # ===== AGRADECIMIENTOS =====
            elif any(word in message_lower for word in ["gracias", "thanks", "excelente", "perfecto", "genial"]):
                return "¡De nada! 😊 Estoy aquí para ayudarte.\n\n¿Hay algo más en lo que pueda asistirte?"
            
            # ===== RESPUESTA POR DEFECTO =====
            else:
                return ("🤔 No estoy seguro de cómo ayudarte con eso.\n\n"
                       "**Puedo ayudarte con:**\n\n"
                       "📦 Información de productos e inventario\n"
                       "🔄 Movimientos y transacciones\n"
                       "👥 Usuarios y empleados\n"
                       "⚠️ Alertas del sistema\n"
                       "📁 Categorías de productos\n"
                       "📊 Estadísticas generales\n\n"
                       "**Ejemplos de preguntas:**\n"
                       "• '¿Cuántos productos hay?'\n"
                       "• 'Últimos movimientos'\n"
                       "• 'Productos con stock bajo'\n"
                       "• 'Resumen general'\n\n"
                       "Escribe 'ayuda' para más información.")
        
        except Exception as e:
            return f"❌ **Error al procesar tu solicitud**\n\n{str(e)}\n\nPor favor, intenta de nuevo o contacta al administrador del sistema."

    # ===== MÉTODOS DE CONSULTA A LA BASE DE DATOS =====
    
    def get_total_products(self):
        """Obtiene el total de productos."""
        query = "SELECT COUNT(*) as total FROM productos WHERE activo = TRUE"
        result = Database.execute_query(query, fetch=True)
        
        if result:
            total = result[0]['total']
            return f"📦 **Total de Productos**\n\nActualmente tienes **{total} productos** registrados en el inventario activo."
        return "❌ No se pudo obtener la información."

    def get_products_summary(self):
        """Obtiene resumen de productos."""
        query = """
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN estado = 'Disponible' THEN 1 ELSE 0 END) as disponibles,
            SUM(CASE WHEN estado = 'Stock Bajo' THEN 1 ELSE 0 END) as stock_bajo,
            SUM(CASE WHEN estado = 'Agotado' THEN 1 ELSE 0 END) as agotados
        FROM productos 
        WHERE activo = TRUE
        """
        result = Database.execute_query(query, fetch=True)
        
        if result:
            data = result[0]
            response = "📊 **Resumen de Inventario**\n\n"
            response += f"📦 Total de productos: **{data['total']}**\n"
            response += f"✅ Disponibles: **{data['disponibles']}**\n"
            response += f"⚠️ Stock bajo: **{data['stock_bajo']}**\n"
            response += f"❌ Agotados: **{data['agotados']}**\n\n"
            
            if data['stock_bajo'] > 0:
                response += "💡 *Tip: Hay productos con stock bajo que requieren atención.*"
            
            return response
        return "❌ No se pudo obtener el resumen."

    def get_low_stock_products(self):
        """Obtiene productos con stock bajo."""
        query = """
        SELECT nombre, stock, stock_minimo 
        FROM productos 
        WHERE activo = TRUE AND estado = 'Stock Bajo'
        ORDER BY stock ASC
        LIMIT 5
        """
        result = Database.execute_query(query, fetch=True)
        
        if result:
            response = "⚠️ **Productos con Stock Bajo**\n\n"
            for i, product in enumerate(result, 1):
                faltante = product['stock_minimo'] - product['stock']
                response += f"**{i}. {product['nombre']}**\n"
                response += f"   • Stock actual: {product['stock']} unidades\n"
                response += f"   • Stock mínimo: {product['stock_minimo']} unidades\n"
                response += f"   • Faltan: {faltante} unidades\n\n"
            
            response += "💡 *Considera reabastecer estos productos pronto.*"
            return response
        return "✅ ¡Excelente! No hay productos con stock bajo."

    def get_out_of_stock_products(self):
        """Obtiene productos agotados."""
        query = """
        SELECT nombre, stock_minimo, codigo
        FROM productos 
        WHERE activo = TRUE AND estado = 'Agotado'
        ORDER BY nombre ASC
        LIMIT 5
        """
        result = Database.execute_query(query, fetch=True)
        
        if result:
            response = "❌ **Productos Agotados**\n\n"
            for i, product in enumerate(result, 1):
                response += f"**{i}. {product['nombre']}**\n"
                response += f"   • Código: {product['codigo']}\n"
                response += f"   • Requerido: {product['stock_minimo']}+ unidades\n\n"
            
            response += "⚠️ *¡Atención! Estos productos necesitan reabastecimiento urgente.*"
            return response
        return "✅ ¡Perfecto! No hay productos agotados."

    def get_inventory_value(self):
        """Obtiene el valor total del inventario."""
        query = """
        SELECT 
            SUM(stock * precio) as valor_total,
            SUM(stock) as unidades_totales,
            COUNT(*) as productos_totales
        FROM productos 
        WHERE activo = TRUE
        """
        result = Database.execute_query(query, fetch=True)
        
        if result:
            data = result[0]
            valor = data['valor_total'] or 0
            unidades = data['unidades_totales'] or 0
            productos = data['productos_totales'] or 0
            
            response = "💰 **Valor del Inventario**\n\n"
            response += f"💵 Valor total: **${valor:,.2f} MXN**\n"
            response += f"📦 Productos: **{productos:,}**\n"
            response += f"📊 Unidades totales: **{unidades:,}**\n\n"
            
            if productos > 0:
                promedio = valor / productos
                response += f"📈 Valor promedio por producto: **${promedio:,.2f} MXN**"
            
            return response
        return "❌ No se pudo calcular el valor del inventario."

    def get_recent_movements(self):
        """Obtiene los últimos movimientos."""
        query = """
        SELECT 
            m.tipo,
            p.nombre as producto,
            m.cantidad,
            m.fecha,
            u.nombre as usuario,
            m.motivo
        FROM movimientos m
        JOIN productos p ON m.producto_id = p.id
        JOIN usuarios u ON m.usuario_id = u.id
        ORDER BY m.fecha DESC
        LIMIT 5
        """
        result = Database.execute_query(query, fetch=True)
        
        if result:
            response = "🔄 **Últimos Movimientos**\n\n"
            for i, mov in enumerate(result, 1):
                tipo_icon = "📥" if mov['tipo'] == 'Entrada' else "📤"
                response += f"**{i}. {tipo_icon} {mov['tipo']}**\n"
                response += f"   • Producto: {mov['producto']}\n"
                response += f"   • Cantidad: {mov['cantidad']} unidades\n"
                response += f"   • Motivo: {mov['motivo']}\n"
                response += f"   • Fecha: {mov['fecha'].strftime('%d/%m/%Y %H:%M')}\n"
                response += f"   • Usuario: {mov['usuario']}\n\n"
            return response
        return "📭 No hay movimientos recientes registrados."

    def get_today_movements(self):
        """Obtiene movimientos de hoy."""
        query = """
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN tipo = 'Entrada' THEN 1 ELSE 0 END) as entradas,
            SUM(CASE WHEN tipo = 'Salida' THEN 1 ELSE 0 END) as salidas,
            SUM(CASE WHEN tipo = 'Entrada' THEN cantidad ELSE 0 END) as unidades_entrada,
            SUM(CASE WHEN tipo = 'Salida' THEN cantidad ELSE 0 END) as unidades_salida
        FROM movimientos
        WHERE DATE(fecha) = CURDATE()
        """
        result = Database.execute_query(query, fetch=True)
        
        if result:
            data = result[0]
            response = "📅 **Movimientos de Hoy**\n\n"
            response += f"🔢 Total de movimientos: **{data['total']}**\n\n"
            response += f"📥 **Entradas:**\n"
            response += f"   • {data['entradas']} movimientos\n"
            response += f"   • {data['unidades_entrada']} unidades totales\n\n"
            response += f"📤 **Salidas:**\n"
            response += f"   • {data['salidas']} movimientos\n"
            response += f"   • {data['unidades_salida']} unidades totales\n\n"
            
            balance = data['unidades_entrada'] - data['unidades_salida']
            if balance > 0:
                response += f"📈 Balance neto: **+{balance} unidades**"
            elif balance < 0:
                response += f"📉 Balance neto: **{balance} unidades**"
            else:
                response += "⚖️ Balance neto: **0 unidades** (equilibrado)"
            
            return response
        return "📭 No hay movimientos registrados hoy."

    def get_movements_summary(self):
        """Obtiene resumen general de movimientos."""
        query = """
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN tipo = 'Entrada' THEN cantidad ELSE 0 END) as total_entradas,
            SUM(CASE WHEN tipo = 'Salida' THEN cantidad ELSE 0 END) as total_salidas
        FROM movimientos
        WHERE MONTH(fecha) = MONTH(CURDATE()) AND YEAR(fecha) = YEAR(CURDATE())
        """
        result = Database.execute_query(query, fetch=True)
        
        if result:
            data = result[0]
            response = "📊 **Resumen de Movimientos (Este Mes)**\n\n"
            response += f"🔢 Total de movimientos: **{data['total']}**\n"
            response += f"📥 Unidades de entrada: **{data['total_entradas']:,}**\n"
            response += f"📤 Unidades de salida: **{data['total_salidas']:,}**\n\n"
            
            balance = data['total_entradas'] - data['total_salidas']
            if balance > 0:
                response += f"📈 Balance mensual: **+{balance:,} unidades**"
            elif balance < 0:
                response += f"📉 Balance mensual: **{balance:,} unidades**"
            else:
                response += "⚖️ Balance mensual: **equilibrado**"
            
            return response
        return "📭 No hay movimientos registrados este mes."

    def get_users_info(self):
        """Obtiene información de usuarios."""
        query = """
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN rol = 'Admin' THEN 1 ELSE 0 END) as admins,
            SUM(CASE WHEN rol = 'Empleado' THEN 1 ELSE 0 END) as empleados,
            SUM(CASE WHEN estado = 'Activo' THEN 1 ELSE 0 END) as activos
        FROM usuarios
        """
        result = Database.execute_query(query, fetch=True)
        
        if result:
            data = result[0]
            response = "👥 **Información de Usuarios**\n\n"
            response += f"🔢 Total de usuarios: **{data['total']}**\n"
            response += f"👑 Administradores: **{data['admins']}**\n"
            response += f"👤 Empleados: **{data['empleados']}**\n"
            response += f"✅ Usuarios activos: **{data['activos']}**\n\n"
            
            inactivos = data['total'] - data['activos']
            if inactivos > 0:
                response += f"⚠️ Usuarios inactivos: **{inactivos}**"
            else:
                response += "✅ *Todos los usuarios están activos.*"
            
            return response
        return "❌ No se pudo obtener información de usuarios."

    def get_alerts_info(self):
        """Obtiene información de alertas."""
        query = """
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN leida = 0 THEN 1 ELSE 0 END) as no_leidas,
            tipo
        FROM alertas
        WHERE leida = 0
        GROUP BY tipo
        ORDER BY COUNT(*) DESC
        """
        result = Database.execute_query(query, fetch=True)
        
        if result:
            response = "⚠️ **Alertas del Sistema**\n\n"
            total_no_leidas = sum(r['no_leidas'] for r in result)
            response += f"🔔 Total de alertas sin leer: **{total_no_leidas}**\n\n"
            response += "**Por tipo:**\n"
            for alert in result:
                tipo_icon = "📦" if "stock" in alert['tipo'].lower() else "🔔"
                response += f"{tipo_icon} {alert['tipo']}: **{alert['no_leidas']}**\n"
            
            response += "\n💡 *Revisa las alertas desde el panel de notificaciones.*"
            return response
        return "✅ ¡Excelente! No hay alertas pendientes."

    def get_categories_info(self):
        """Obtiene información de categorías."""
        query = """
        SELECT 
            c.nombre,
            COUNT(p.id) as total_productos,
            SUM(p.stock) as total_unidades
        FROM categorias c
        LEFT JOIN productos p ON c.id = p.categoria_id AND p.activo = TRUE
        WHERE c.activo = TRUE
        GROUP BY c.id, c.nombre
        ORDER BY total_productos DESC
        LIMIT 8
        """
        result = Database.execute_query(query, fetch=True)
        
        if result:
            response = "📁 **Categorías de Productos**\n\n"
            for i, cat in enumerate(result, 1):
                unidades = cat['total_unidades'] or 0
                response += f"**{i}. {cat['nombre']}**\n"
                response += f"   • Productos: {cat['total_productos']}\n"
                response += f"   • Unidades: {unidades:,}\n\n"
            return response
        return "📁 No hay categorías registradas."

    def get_general_stats(self):
        """Obtiene estadísticas generales del sistema."""
        # Productos
        query_productos = """
        SELECT 
            COUNT(*) as total,
            SUM(stock) as unidades,
            SUM(stock * precio) as valor
        FROM productos WHERE activo = TRUE
        """
        productos = Database.execute_query(query_productos, fetch=True)[0]
        
        # Movimientos del mes
        query_movimientos = """
        SELECT COUNT(*) as total
        FROM movimientos
        WHERE MONTH(fecha) = MONTH(CURDATE()) AND YEAR(fecha) = YEAR(CURDATE())
        """
        movimientos = Database.execute_query(query_movimientos, fetch=True)[0]
        
        # Alertas
        query_alertas = """
        SELECT COUNT(*) as total
        FROM alertas
        WHERE leida = 0
        """
        alertas = Database.execute_query(query_alertas, fetch=True)[0]
        
        response = "📊 **Resumen General del Sistema**\n\n"
        response += "**📦 Inventario:**\n"
        response += f"   • {productos['total']} productos\n"
        response += f"   • {productos['unidades']:,} unidades\n"
        response += f"   • ${productos['valor']:,.2f} MXN\n\n"
        response += "**🔄 Movimientos (Este Mes):**\n"
        response += f"   • {movimientos['total']} transacciones\n\n"
        response += "**⚠️ Alertas:**\n"
        response += f"   • {alertas['total']} sin leer\n\n"
        response += f"👤 **Usuario actual:** {self.user_data.get('nombre', 'Usuario')}\n"
        response += f"🎭 **Rol:** {self.user_data.get('rol', 'N/A')}"
        
        return response

    def get_help_info(self):
        """Proporciona información de ayuda."""
        response = "💡 **Guía de Uso - Chat AI**\n\n"
        response += "**📦 Inventario:**\n"
        response += "• '¿Cuántos productos hay?'\n"
        response += "• 'Productos con stock bajo'\n"
        response += "• 'Productos agotados'\n"
        response += "• 'Valor del inventario'\n"
        response += "• 'Resumen de inventario'\n\n"
        response += "**🔄 Movimientos:**\n"
        response += "• 'Últimos movimientos'\n"
        response += "• 'Movimientos de hoy'\n"
        response += "• 'Resumen de movimientos'\n\n"
        response += "**👥 Usuarios:**\n"
        response += "• 'Información de usuarios'\n"
        response += "• 'Cuántos usuarios hay'\n\n"
        response += "**⚠️ Alertas:**\n"
        response += "• 'Alertas pendientes'\n"
        response += "• 'Notificaciones sin leer'\n\n"
        response += "**📁 Categorías:**\n"
        response += "• 'Mostrar categorías'\n"
        response += "• 'Productos por categoría'\n\n"
        response += "**📊 General:**\n"
        response += "• 'Resumen general'\n"
        response += "• 'Estadísticas del sistema'\n\n"
        response += "💬 *Puedes hacer preguntas en lenguaje natural.*\n"
        response += "🔄 *Usa el botón 'Limpiar' para reiniciar el chat.*"
        return response