"""Vista: Registrar Venta / Punto de Venta"""

import flet as ft
from core import productos as prods, ventas as vtas
from theme import Colors
from utils.dialogs import msg


class VentaView:
    def __init__(self, page):
        self.page = page

        # ==========================================================
        # DATOS
        # ==========================================================

        self.carrito = []

        # ==========================================================
        # CONTROLES
        # ==========================================================

        self.buscar = None
        self.lista_productos = None
        self.lista_factura = None

        self.lbl_total = None
        self.lbl_ganancia = None
        self.lbl_unidades = None
        self.lbl_productos_factura = None

        self.metodo = None
        self.monto_recibido = None
        self.lbl_vuelto = None

    # ==============================================================
    # BUILD
    # ==============================================================

    def build(self):

        # ==========================================================
        # BUSCADOR
        # ==========================================================

        self.buscar = ft.TextField(
            label="Buscar producto",
            hint_text="Nombre del producto...",
            prefix_icon=ft.Icons.SEARCH,
            suffix=ft.IconButton(
                icon=ft.Icons.CLEAR,
                tooltip="Limpiar búsqueda",
                on_click=self._limpiar_busqueda,
            ),
            expand=True,
            on_change=self._buscar_producto,
            on_submit=self._buscar_enter,
        )

        # ==========================================================
        # LISTA DE PRODUCTOS
        # ==========================================================

        self.lista_productos = ft.Column(
            spacing=7,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        # ==========================================================
        # LISTA DE FACTURA
        # ==========================================================

        self.lista_factura = ft.Column(
            spacing=3,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        # ==========================================================
        # TOTALES
        # ==========================================================

        self.lbl_total = ft.Text(
            "₡0",
            size=27,
            weight=ft.FontWeight.BOLD,
            color=Colors.PRIMARY,
        )

        self.lbl_ganancia = ft.Text(
            "Ganancia estimada: ₡0",
            size=13,
            color=ft.Colors.GREY_700,
        )

        self.lbl_unidades = ft.Text(
            "0 unidades",
            size=13,
            color=ft.Colors.GREY_700,
        )

        self.lbl_productos_factura = ft.Text(
            "0 productos",
            size=13,
            color=ft.Colors.GREY_700,
        )

        # ==========================================================
        # MÉTODO DE PAGO
        # ==========================================================

        self.metodo = ft.Dropdown(
            label="Método de pago",
            width=220,
            options=[
                ft.DropdownOption("Efectivo"),
                ft.DropdownOption("SINPE"),
            ],
            value="Efectivo",
            on_select=self._cambiar_metodo,
        )

        # ==========================================================
        # MONTO RECIBIDO
        # ==========================================================

        self.monto_recibido = ft.TextField(
            label="Monto recibido",
            hint_text="Ingrese el monto",
            width=220,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self._calcular_vuelto,
        )

        self.lbl_vuelto = ft.Text(
            "Vuelto: ₡0",
            size=17,
            weight=ft.FontWeight.BOLD,
        )

        # ==========================================================
        # MOSTRAR PRODUCTOS
        # ==========================================================

        self._mostrar_productos()

        # ==========================================================
        # PANEL PRODUCTOS
        # ==========================================================

        panel_productos = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "Productos",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=Colors.PRIMARY,
                            ),

                            ft.Container(expand=True),

                            ft.Text(
                                "Seleccione para agregar",
                                size=12,
                                color=ft.Colors.GREY_600,
                            ),
                        ]
                    ),

                    self.buscar,

                    ft.Divider(height=1),

                    self.lista_productos,
                ],
                spacing=10,
                expand=True,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=18,
            expand=True,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=Colors.CARD_SHADOW,
            ),
        )

        # ==========================================================
        # ENCABEZADO FACTURA
        # ==========================================================

        encabezado_factura = ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            "Factura",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=Colors.PRIMARY,
                        ),

                        ft.Row(
                            [
                                self.lbl_productos_factura,
                                ft.Text("•"),
                                self.lbl_unidades,
                            ],
                            spacing=5,
                        ),
                    ],
                    spacing=2,
                ),

                ft.Container(expand=True),

                ft.IconButton(
                    icon=ft.Icons.DELETE_SWEEP,
                    tooltip="Vaciar factura",
                    on_click=self._vaciar_carrito,
                ),
            ]
        )

        # ==========================================================
        # ENCABEZADO DE COLUMNAS
        # ==========================================================

        encabezado_columnas = ft.Row(
            [
                ft.Text(
                    "Producto",
                    weight=ft.FontWeight.BOLD,
                    expand=True,
                ),

                ft.Text(
                    "Cantidad",
                    weight=ft.FontWeight.BOLD,
                    width=120,
                    text_align=ft.TextAlign.CENTER,
                ),

                ft.Text(
                    "Subtotal",
                    weight=ft.FontWeight.BOLD,
                    width=100,
                    text_align=ft.TextAlign.RIGHT,
                ),

                ft.Container(width=40),
            ]
        )

        # ==========================================================
        # PANEL FACTURA
        # ==========================================================

        panel_factura = ft.Container(
            content=ft.Column(
                [
                    encabezado_factura,

                    ft.Divider(height=1),

                    encabezado_columnas,

                    ft.Divider(height=1),

                    self.lista_factura,

                    ft.Divider(height=1),

                    # TOTAL
                    ft.Row(
                        [
                            ft.Text(
                                "TOTAL",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            ),

                            ft.Container(expand=True),

                            self.lbl_total,
                        ]
                    ),

                    self.lbl_ganancia,

                    ft.Divider(height=1),

                    # MÉTODO DE PAGO
                    ft.Row(
                        [
                            self.metodo,
                            self.monto_recibido,
                        ],
                        spacing=10,
                    ),

                    self.lbl_vuelto,

                    # BOTÓN REGISTRAR
                    ft.Button(
                        content=ft.Text(
                            "💵  REGISTRAR VENTA",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                        ),
                        style=ft.ButtonStyle(
                            bgcolor=Colors.SUCCESS,
                            color=ft.Colors.WHITE,
                        ),
                        height=50,
                        on_click=self._registrar,
                    ),
                ],
                spacing=9,
                expand=True,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=18,
            expand=True,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=Colors.CARD_SHADOW,
            ),
        )

        # ==========================================================
        # VISTA COMPLETA
        # ==========================================================

        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "🧾 Venta",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=Colors.PRIMARY,
                        ),

                        ft.Container(expand=True),

                        ft.Text(
                            "Punto de venta",
                            size=13,
                            color=ft.Colors.GREY_600,
                        ),
                    ]
                ),

                ft.Divider(
                    height=2,
                    color=Colors.ACCENT,
                ),

                ft.Row(
                    [
                        panel_productos,
                        panel_factura,
                    ],
                    spacing=15,
                    expand=True,
                ),
            ],
            expand=True,
        )

    # ==============================================================
    # MOSTRAR PRODUCTOS
    # ==============================================================

    def _mostrar_productos(self, productos=None):

        if productos is None:
            productos = prods.listar_con_stock()

        self.lista_productos.controls.clear()

        if not productos:

            self.lista_productos.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(
                                ft.Icons.INVENTORY_2_OUTLINED,
                                size=40,
                                color=ft.Colors.GREY_400,
                            ),

                            ft.Text(
                                "No hay productos disponibles",
                                color=ft.Colors.GREY_600,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=30,
                    alignment=ft.Alignment.CENTER,
                )
            )

        else:

            for p in productos:

                producto_id = p["id"]
                nombre = p["nombre"]
                precio = p["precio_venta"]
                stock = p["stock"]

                # --------------------------------------------------
                # Verificar si ya está en factura
                # --------------------------------------------------

                cantidad_carrito = 0

                for item in self.carrito:
                    if item["id"] == producto_id:
                        cantidad_carrito = item["cantidad"]
                        break

                stock_restante = stock - cantidad_carrito

                # --------------------------------------------------
                # Información del producto
                # --------------------------------------------------

                if stock_restante <= 0:

                    texto_stock = "Máximo en factura"
                    color_stock = ft.Colors.RED

                elif stock_restante <= 5:

                    texto_stock = f"Stock: {stock_restante}"
                    color_stock = ft.Colors.ORANGE

                else:

                    texto_stock = f"Stock: {stock_restante}"
                    color_stock = ft.Colors.GREY_700

                # --------------------------------------------------
                # Botón agregar
                # --------------------------------------------------

                boton_agregar = ft.Button(
                    content=ft.Text(
                        "Agotado"
                        if stock_restante <= 0
                        else "Agregar"
                    ),
                    disabled=stock_restante <= 0,
                    on_click=lambda e, pid=producto_id:
                        self._agregar_producto(pid),
                )

                # --------------------------------------------------
                # Tarjeta
                # --------------------------------------------------

                tarjeta = ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.INVENTORY_2_OUTLINED,
                                    size=25,
                                ),
                                width=45,
                            ),

                            ft.Column(
                                [
                                    ft.Text(
                                        nombre,
                                        size=15,
                                        weight=ft.FontWeight.BOLD,
                                    ),

                                    ft.Row(
                                        [
                                            ft.Text(
                                                f"₡{precio:,.0f}",
                                                size=14,
                                                weight=ft.FontWeight.BOLD,
                                                color=Colors.PRIMARY,
                                            ),

                                            ft.Text(
                                                "•",
                                                color=ft.Colors.GREY_500,
                                            ),

                                            ft.Text(
                                                texto_stock,
                                                size=12,
                                                color=color_stock,
                                            ),
                                        ],
                                        spacing=5,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),

                            boton_agregar,
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),

                    padding=10,
                    border_radius=8,
                    bgcolor=ft.Colors.GREY_100,
                )

                self.lista_productos.controls.append(tarjeta)

        self.page.update()

    # ==============================================================
    # BUSCAR
    # ==============================================================

    def _buscar_producto(self, e):

        texto = self.buscar.value.strip().lower()

        productos = prods.listar_con_stock()

        if texto:

            productos = [
                p
                for p in productos
                if texto in p["nombre"].lower()
            ]

        self._mostrar_productos(productos)

    # ==============================================================
    # ENTER EN BUSCADOR
    # ==============================================================

    def _buscar_enter(self, e):

        texto = self.buscar.value.strip().lower()

        if not texto:
            return

        productos = prods.listar_con_stock()

        productos = [
            p
            for p in productos
            if texto in p["nombre"].lower()
        ]

        # Si solamente hay un resultado,
        # agregarlo automáticamente.
        if len(productos) == 1:

            self._agregar_producto(
                productos[0]["id"]
            )

            self.buscar.value = ""
            self._mostrar_productos()

    # ==============================================================
    # LIMPIAR BUSQUEDA
    # ==============================================================

    def _limpiar_busqueda(self, e):

        self.buscar.value = ""

        self._mostrar_productos()

    # ==============================================================
    # AGREGAR PRODUCTO
    # ==============================================================

    def _agregar_producto(self, producto_id):

        p = prods.obtener(producto_id)

        if not p:
            return

        stock = p["stock"]

        # ----------------------------------------------------------
        # Buscar en carrito
        # ----------------------------------------------------------

        producto_carrito = None

        for item in self.carrito:

            if item["id"] == producto_id:

                producto_carrito = item
                break

        # ----------------------------------------------------------
        # Ya existe
        # ----------------------------------------------------------

        if producto_carrito:

            if producto_carrito["cantidad"] >= stock:

                msg(
                    self.page,
                    "Stock insuficiente",
                    f"No puedes agregar más unidades.\n\n"
                    f"{p['nombre']}\n"
                    f"Stock disponible: {stock}",
                    "error",
                )

                return

            producto_carrito["cantidad"] += 1

        # ----------------------------------------------------------
        # Nuevo producto
        # ----------------------------------------------------------

        else:

            self.carrito.append(
                {
                    "id": p["id"],
                    "nombre": p["nombre"],
                    "cantidad": 1,
                    "precio_venta": p["precio_venta"],
                    "precio_compra": p["precio_compra"],
                    "stock": stock,
                }
            )

        self._actualizar_factura()

        # Actualizar lista para reflejar
        # el stock restante.
        texto = self.buscar.value.strip().lower()

        productos = prods.listar_con_stock()

        if texto:

            productos = [
                p
                for p in productos
                if texto in p["nombre"].lower()
            ]

        self._mostrar_productos(productos)

    # ==============================================================
    # AUMENTAR
    # ==============================================================

    def _aumentar_cantidad(self, producto_id):

        for item in self.carrito:

            if item["id"] == producto_id:

                # Actualizar stock real
                p = prods.obtener(producto_id)

                if not p:
                    return

                if item["cantidad"] >= p["stock"]:

                    msg(
                        self.page,
                        "Stock insuficiente",
                        f"Solo hay {p['stock']} unidades disponibles.",
                        "error",
                    )

                    return

                item["cantidad"] += 1

                break

        self._actualizar_factura()
        self._actualizar_productos()

    # ==============================================================
    # DISMINUIR
    # ==============================================================

    def _disminuir_cantidad(self, producto_id):

        for item in self.carrito:

            if item["id"] == producto_id:

                item["cantidad"] -= 1

                if item["cantidad"] <= 0:

                    self.carrito.remove(item)

                break

        self._actualizar_factura()
        self._actualizar_productos()

    # ==============================================================
    # ELIMINAR
    # ==============================================================

    def _eliminar_producto(self, producto_id):

        self.carrito = [
            item
            for item in self.carrito
            if item["id"] != producto_id
        ]

        self._actualizar_factura()
        self._actualizar_productos()

    # ==============================================================
    # ACTUALIZAR PRODUCTOS
    # ==============================================================

    def _actualizar_productos(self):

        texto = self.buscar.value.strip().lower()

        productos = prods.listar_con_stock()

        if texto:

            productos = [
                p
                for p in productos
                if texto in p["nombre"].lower()
            ]

        self._mostrar_productos(productos)

    # ==============================================================
    # ACTUALIZAR FACTURA
    # ==============================================================

    def _actualizar_factura(self):

        self.lista_factura.controls.clear()

        total = 0
        ganancia_total = 0
        total_unidades = 0

        # ==========================================================
        # FACTURA VACIA
        # ==========================================================

        if not self.carrito:

            self.lista_factura.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(
                                ft.Icons.RECEIPT_LONG,
                                size=50,
                                color=ft.Colors.GREY_400,
                            ),

                            ft.Text(
                                "Factura vacía",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREY_600,
                            ),

                            ft.Text(
                                "Agrega productos para comenzar.",
                                size=12,
                                color=ft.Colors.GREY_500,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                    ),
                    alignment=ft.Alignment.CENTER,
                    padding=35,
                )
            )

        # ==========================================================
        # PRODUCTOS
        # ==========================================================

        for item in self.carrito:

            cantidad = item["cantidad"]
            precio = item["precio_venta"]
            costo = item["precio_compra"]

            subtotal = cantidad * precio
            ganancia = cantidad * (precio - costo)

            total += subtotal
            ganancia_total += ganancia
            total_unidades += cantidad

            # ------------------------------------------------------
            # Fila
            # ------------------------------------------------------

            fila = ft.Container(
                content=ft.Row(
                    [
                        # Nombre
                        ft.Column(
                            [
                                ft.Text(
                                    item["nombre"],
                                    size=13,
                                    weight=ft.FontWeight.BOLD,
                                    max_lines=2,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),

                                ft.Text(
                                    f"₡{precio:,.0f} c/u",
                                    size=11,
                                    color=ft.Colors.GREY_600,
                                ),
                            ],
                            spacing=1,
                            expand=True,
                        ),

                        # Cantidad
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                                    icon_size=19,
                                    tooltip="Disminuir",
                                    on_click=lambda e, pid=item["id"]:
                                        self._disminuir_cantidad(pid),
                                ),

                                ft.Text(
                                    str(cantidad),
                                    width=25,
                                    text_align=ft.TextAlign.CENTER,
                                    weight=ft.FontWeight.BOLD,
                                ),

                                ft.IconButton(
                                    icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                                    icon_size=19,
                                    tooltip="Aumentar",
                                    on_click=lambda e, pid=item["id"]:
                                        self._aumentar_cantidad(pid),
                                ),
                            ],
                            spacing=0,
                            width=120,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),

                        # Subtotal
                        ft.Text(
                            f"₡{subtotal:,.0f}",
                            width=100,
                            text_align=ft.TextAlign.RIGHT,
                            weight=ft.FontWeight.BOLD,
                            size=13,
                        ),

                        # Eliminar
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            icon_color=ft.Colors.RED,
                            icon_size=20,
                            tooltip="Eliminar producto",
                            on_click=lambda e, pid=item["id"]:
                                self._eliminar_producto(pid),
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=5,
                border_radius=6,
            )

            self.lista_factura.controls.append(fila)

        # ==========================================================
        # ACTUALIZAR TOTALES
        # ==========================================================

        self.lbl_total.value = f"₡{total:,.0f}"

        self.lbl_ganancia.value = (
            f"Ganancia estimada: ₡{ganancia_total:,.0f}"
        )

        cantidad_productos = len(self.carrito)

        self.lbl_productos_factura.value = (
            f"{cantidad_productos} "
            f"{'producto' if cantidad_productos == 1 else 'productos'}"
        )

        self.lbl_unidades.value = (
            f"{total_unidades} "
            f"{'unidad' if total_unidades == 1 else 'unidades'}"
        )

        # Recalcular vuelto
        self._calcular_vuelto()

        self.page.update()

    # ==============================================================
    # CAMBIAR METODO
    # ==============================================================

    def _cambiar_metodo(self, e=None):

        metodo = self.metodo.value

        if metodo == "Efectivo":

            self.monto_recibido.visible = True
            self.lbl_vuelto.visible = True

        else:

            self.monto_recibido.value = ""
            self.monto_recibido.visible = False

            self.lbl_vuelto.value = "Pago por SINPE"
            self.lbl_vuelto.visible = True

        self.page.update()

    # ==============================================================
    # CALCULAR VUELTO
    # ==============================================================

    def _calcular_vuelto(self, e=None):

        if not self.lbl_vuelto:
            return

        if self.metodo.value != "Efectivo":

            self.lbl_vuelto.value = "Pago por SINPE"
            return

        total = self._obtener_total()

        try:

            monto = float(
                self.monto_recibido.value
                .replace(",", "")
                .replace(".", "")
                .strip()
            )

        except:

            self.lbl_vuelto.value = "Vuelto: ₡0"
            return

        vuelto = monto - total

        if vuelto >= 0:

            self.lbl_vuelto.value = (
                f"Vuelto: ₡{vuelto:,.0f}"
            )

        else:

            faltante = abs(vuelto)

            self.lbl_vuelto.value = (
                f"Falta: ₡{faltante:,.0f}"
            )

        self.page.update()

    # ==============================================================
    # OBTENER TOTAL
    # ==============================================================

    def _obtener_total(self):

        total = 0

        for item in self.carrito:

            total += (
                item["cantidad"]
                * item["precio_venta"]
            )

        return total

    # ==============================================================
    # OBTENER VUELTO
    # ==============================================================

    def _obtener_monto_recibido(self):

        try:

            return float(
                self.monto_recibido.value
                .replace(",", "")
                .replace(".", "")
                .strip()
            )

        except:

            return 0

    # ==============================================================
    # VACIAR CARRITO
    # ==============================================================

    def _vaciar_carrito(self, e=None):

        if not self.carrito:

            return

        self.carrito.clear()

        self.monto_recibido.value = ""

        self._actualizar_factura()
        self._actualizar_productos()

    # ==============================================================
    # VALIDAR STOCK
    # ==============================================================

    def _validar_stock(self):

        for item in self.carrito:

            p = prods.obtener(item["id"])

            if not p:

                msg(
                    self.page,
                    "Producto no encontrado",
                    f"No se encontró:\n{item['nombre']}",
                    "error",
                )

                return False

            if item["cantidad"] > p["stock"]:

                msg(
                    self.page,
                    "Stock insuficiente",
                    f"{item['nombre']}\n\n"
                    f"Solicitado: {item['cantidad']}\n"
                    f"Disponible: {p['stock']}",
                    "error",
                )

                return False

        return True

    # ==============================================================
    # REGISTRAR VENTA
    # ==============================================================

    def _registrar(self, e=None):

        # ==========================================================
        # VALIDAR CARRITO
        # ==========================================================

        if not self.carrito:

            msg(
                self.page,
                "Factura vacía",
                "Agrega al menos un producto.",
                "error",
            )

            return

        # ==========================================================
        # TOTAL
        # ==========================================================

        total = self._obtener_total()

        # ==========================================================
        # MÉTODO
        # ==========================================================

        metodo = self.metodo.value

        if not metodo:

            metodo = "Efectivo"

        # ==========================================================
        # VALIDAR EFECTIVO
        # ==========================================================

        if metodo == "Efectivo":

            monto_recibido = self._obtener_monto_recibido()

            if monto_recibido <= 0:

                msg(
                    self.page,
                    "Monto inválido",
                    "Ingresa el monto recibido del cliente.",
                    "error",
                )

                return

            if monto_recibido < total:

                faltante = total - monto_recibido

                msg(
                    self.page,
                    "Pago insuficiente",
                    f"Faltan ₡{faltante:,.0f}",
                    "error",
                )

                return

        # ==========================================================
        # VALIDAR STOCK
        # ==========================================================

        if not self._validar_stock():

            return

        # ==========================================================
        # REGISTRAR
        # ==========================================================

        cantidad_productos = 0

        for item in self.carrito:

            cantidad = item["cantidad"]

            cantidad_productos += cantidad

            vtas.registrar(
                item["id"],
                item["nombre"],
                cantidad,
                item["precio_venta"],
                item["precio_compra"],
                metodo,
                monto_recibido if metodo == "Efectivo" else 0,
            )

            prods.descontar_stock(
                item["id"],
                cantidad,
            )

        # ==========================================================
        # CALCULAR VUELTO
        # ==========================================================

        vuelto = 0

        if metodo == "Efectivo":

            vuelto = (
                monto_recibido
                - total
            )

        # ==========================================================
        # RESUMEN
        # ==========================================================

        resumen = ""

        for item in self.carrito:

            subtotal = (
                item["cantidad"]
                * item["precio_venta"]
            )

            resumen += (
                f"{item['cantidad']}x "
                f"{item['nombre']}\n"
                f"    ₡{subtotal:,.0f}\n"
            )

        mensaje = (
            f"{resumen}\n"
            f"────────────────\n"
            f"Total: ₡{total:,.0f}\n"
            f"Método: {metodo}\n"
        )

        if metodo == "Efectivo":

            mensaje += (
                f"Recibido: ₡{monto_recibido:,.0f}\n"
                f"Vuelto: ₡{vuelto:,.0f}\n"
            )

        mensaje += (
            f"Unidades: {cantidad_productos}"
        )

        # ==========================================================
        # LIMPIAR
        # ==========================================================

        self.carrito.clear()

        self.buscar.value = ""
        self.monto_recibido.value = ""

        self._actualizar_factura()

        self._mostrar_productos()

        self.page.update()

        # ==========================================================
        # MENSAJE
        # ==========================================================

        msg(
            self.page,
            "Venta registrada",
            mensaje,
            "ok",
        )