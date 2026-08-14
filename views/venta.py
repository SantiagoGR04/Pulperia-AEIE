"""Vista: Registrar Venta (Efectivo / SINPE)"""
import flet as ft
from core import productos as prods, ventas as vtas
from theme import Colors
from utils.dialogs import msg


class VentaView:
    def __init__(self, page):
        self.page = page
        self._selected_id = None
        self._pv = 0
        self._pc = 0

    def build(self):
        form = ft.Column(spacing=8)

        # Lista de productos
        self.combo = ft.Dropdown(
            label="Producto",
            width=400,
            options=[
                ft.dropdown.Option(f"{p['id']} - {p['nombre']}")
                for p in prods.listar_con_stock()
            ],
            on_select=self._cargar_precio
        )

        # NUEVO: campo para buscar productos por nombre
        self.buscar = ft.TextField(
            label="Buscar producto por nombre",
            hint_text="Escribe el nombre del producto...",
            width=400,
            on_change=self._buscar_producto,
        )

        self.lbl_precio = ft.Text(
            "Precio: ₡0",
            size=16,
            weight=ft.FontWeight.BOLD
        )

        self.lbl_stock = ft.Text(
            "Stock disponible: —",
            size=13
        )

        self.cant = ft.TextField(
            label="Cantidad",
            width=200,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self._calcular
        )

        self.lbl_subtotal = ft.Text(
            "Subtotal: ₡0",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=Colors.PRIMARY
        )

        self.lbl_ganancia = ft.Text(
            "Ganancia: ₡0",
            size=14
        )

        self.metodo = ft.Dropdown(
            label="Método de pago",
            width=400,
            options=[
                ft.dropdown.Option("Efectivo"),
                ft.dropdown.Option("SINPE")
            ],
            value="Efectivo",
            on_select=self._cambiar_metodo,
        )
        self.efectivo_recibido = ft.TextField(
            label="Dinero recibido",
            width=400,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self._calcular_vuelto,
        )
        self.vuelto = ft.Text(
            "Vuelto: ₡0",
            size=16,
            weight=ft.FontWeight.BOLD,
            color=Colors.SUCCESS
        )

        form.controls = [
            # NUEVO: buscador
            self.buscar,

            # Lista de productos
            self.combo,

            self.lbl_stock,
            self.lbl_precio,
            self.cant,
            self.lbl_subtotal,
            self.lbl_ganancia,
            self.metodo,
            self.efectivo_recibido,
            self.vuelto,
            ft.Button(
                content=ft.Text("💵 Registrar Venta"),
                style=ft.ButtonStyle(
                    bgcolor=Colors.SUCCESS,
                    color=ft.Colors.WHITE
                ),
                on_click=lambda e: self._registrar(self.metodo.value)
            ),
        ]

        # Estado inicial: mostrar/ocultar según método seleccionado
        self._cambiar_metodo(None)

        return ft.Column(
            [
                ft.Text(
                    "🧾 Venta",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=Colors.PRIMARY
                ),

                ft.Divider(
                    height=2,
                    color=Colors.ACCENT
                ),

                ft.Container(
                    content=form,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12,
                    padding=20,
                    width=500,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=8,
                        color=Colors.CARD_SHADOW
                    )
                ),
            ],
            expand=True
        )

    # NUEVO: buscar producto por nombre
    def _buscar_producto(self, e):
        texto = self.buscar.value.strip().lower()

        # Obtener productos disponibles
        productos = prods.listar_con_stock()

        # Si escribió algo, filtrar por nombre
        if texto:
            productos = [
                p for p in productos
                if texto in p["nombre"].lower()
            ]

        # Actualizar opciones del Dropdown
        self.combo.options = [
            ft.dropdown.Option(
                f"{p['id']} - {p['nombre']}"
            )
            for p in productos
        ]

        # Limpiar selección si estaba seleccionada
        self.combo.value = None
        self._selected_id = None

        self.lbl_precio.value = "Precio: ₡0"
        self.lbl_stock.value = "Stock disponible: —"
        self.lbl_subtotal.value = "Subtotal: ₡0"
        self.lbl_ganancia.value = "Ganancia: ₡0"
        self.vuelto.value = "Vuelto: ₡0"

        self.page.update()

    def _cargar_precio(self, e):
        try:
            pid = int(self.combo.value.split(" - ")[0])
            p = prods.obtener(pid)

            if p:
                self._selected_id = pid
                self._pv = p["precio_venta"]
                self._pc = p["precio_compra"]

                self.lbl_precio.value = f"Precio: ₡{self._pv:,.0f}"
                self.lbl_stock.value = f"Stock disponible: {p['stock']}"

                self._calcular()
                self.page.update()

        except:
            pass

    def _calcular(self, e=None):
        try:
            c = int(self.cant.value)

            sub = c * self._pv
            gan = c * (self._pv - self._pc)

            self.lbl_subtotal.value = f"Subtotal: ₡{sub:,.0f}"
            self.lbl_ganancia.value = f"Ganancia: ₡{gan:,.0f}"

        except:
            self.lbl_subtotal.value = "Subtotal: ₡0"
            self.lbl_ganancia.value = "Ganancia: ₡0"

        self._calcular_vuelto()

    def _calcular_vuelto(self, e=None):
        # En Flet 0.86.5, el valor actualizado viene en e.control.value;
        # leer self.efectivo_recibido.value puede quedar desincronizado.
        if e is not None:
            valor = e.control.value if hasattr(e, "control") else self.efectivo_recibido.value
        else:
            valor = self.efectivo_recibido.value

        try:
            recibido = int(valor)
        except (ValueError, TypeError):
            self.vuelto.value = "Vuelto: ₡0"
            self.page.update()
            return

        sub = int(self.cant.value or 0) * self._pv

        if self.metodo.value == "Efectivo":
            if recibido < sub:
                self.vuelto.value = "Dinero recibido insuficiente"
                self.vuelto.color = Colors.DANGER
            else:
                v = recibido - sub
                self.vuelto.value = f"Vuelto: ₡{v:,.0f}"
                self.vuelto.color = Colors.SUCCESS
        else:
            self.vuelto.value = "Vuelto: ₡0"
            self.vuelto.color = Colors.SUCCESS

        self.page.update()

    def _cambiar_metodo(self, e):
        es_efectivo = self.metodo.value == "Efectivo"
        self.efectivo_recibido.visible = es_efectivo
        self.vuelto.visible = es_efectivo
        if es_efectivo:
            self._calcular_vuelto()
        self.page.update()

    def _registrar(self, metodo):
        if self._selected_id is None:
            msg(
                self.page,
                "Error",
                "Selecciona un producto",
                "error"
            )
            return

        try:
            cant = int(self.cant.value)

            if cant <= 0:
                raise ValueError

        except:
            msg(
                self.page,
                "Error",
                "Cantidad inválida",
                "error"
            )
            return

        p = prods.obtener(self._selected_id)

        if not p:
            return

        if cant > p["stock"]:
            msg(
                self.page,
                "Stock insuficiente",
                f"Solo hay {p['stock']} unidades",
                "error"
            )
            return

        if metodo == "Efectivo":
            try:
                recibido = int(self.efectivo_recibido.value)
            except (ValueError, TypeError):
                msg(
                    self.page,
                    "Error",
                    "Indica cuánto dinero recibiste",
                    "error"
                )
                return

            subtotal = cant * self._pv

            if recibido < subtotal:
                msg(
                    self.page,
                    "Efectivo insuficiente",
                    f"Faltan ₡{subtotal - recibido:,.0f}",
                    "error"
                )
                return
        else:
            recibido = 0

        _, vuelto = vtas.registrar(
            p["id"],
            p["nombre"],
            cant,
            self._pv,
            self._pc,
            metodo,
            recibido
        )

        prods.descontar_stock(
            p["id"],
            cant
        )

        detalle = f"{cant}x {p['nombre']}\n{metodo}\n₡{cant * self._pv:,.0f}"

        if metodo == "Efectivo":
            detalle += f"\nRecibido: ₡{recibido:,.0f}\nVuelto: ₡{vuelto:,.0f}"

        msg(
            self.page,
            "Venta registrada",
            detalle,
            "ok"
        )

        # Limpiar campos
        self.combo.value = None
        self.buscar.value = ""
        self.cant.value = ""
        self.efectivo_recibido.value = ""
        self.vuelto.value = "Vuelto: ₡0"

        self._selected_id = None

        self.lbl_precio.value = "Precio: ₡0"
        self.lbl_stock.value = "Stock disponible: —"
        self.lbl_subtotal.value = "Subtotal: ₡0"
        self.lbl_ganancia.value = "Ganancia: ₡0"

        # Refresh product list
        self.combo.options = [
            ft.dropdown.Option(
                f"{p['id']} - {p['nombre']}"
            )
            for p in prods.listar_con_stock()
        ]

        self.page.update()
