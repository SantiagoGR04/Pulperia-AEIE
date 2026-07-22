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

        self.combo = ft.Dropdown(label="Producto", width=400,
            options=[ft.dropdown.Option(f"{p['id']} - {p['nombre']}") for p in prods.listar_con_stock()],
            on_select=self._cargar_precio)
        self.lbl_precio = ft.Text("Precio: ₡0", size=16, weight=ft.FontWeight.BOLD)
        self.lbl_stock = ft.Text("Stock disponible: —", size=13)

        self.cant = ft.TextField(label="Cantidad", width=200, keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self._calcular)
        self.lbl_subtotal = ft.Text("Subtotal: ₡0", size=18, weight=ft.FontWeight.BOLD, color=Colors.PRIMARY)
        self.lbl_ganancia = ft.Text("Ganancia: ₡0", size=14)

        metodo = ft.Dropdown(
            label="Método de pago", width=400,
            options=[ft.dropdown.Option("Efectivo"), ft.dropdown.Option("SINPE")],
            value="Efectivo",
        )

        form.controls = [
            self.combo, self.lbl_stock, self.lbl_precio,
            self.cant, self.lbl_subtotal, self.lbl_ganancia,
            metodo,
            ft.Button(content=ft.Text("💵 Registrar Venta"),
                style=ft.ButtonStyle(bgcolor=Colors.SUCCESS, color=ft.Colors.WHITE),
                on_click=lambda e: self._registrar(metodo.value)),
        ]

        return ft.Column([
            ft.Text("🧾 Venta", size=20, weight=ft.FontWeight.BOLD, color=Colors.PRIMARY),
            ft.Divider(height=2, color=Colors.ACCENT),
            ft.Container(content=form, bgcolor=ft.Colors.WHITE, border_radius=12,
                         padding=20, width=500,
                         shadow=ft.BoxShadow(spread_radius=1, blur_radius=8, color=Colors.CARD_SHADOW)),
        ], expand=True)

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

    def _registrar(self, metodo):
        if self._selected_id is None:
            msg(self.page, "Error", "Selecciona un producto", "error")
            return
        try:
            cant = int(self.cant.value)
            if cant <= 0:
                raise ValueError
        except:
            msg(self.page, "Error", "Cantidad inválida", "error")
            return

        p = prods.obtener(self._selected_id)
        if not p:
            return
        if cant > p["stock"]:
            msg(self.page, "Stock insuficiente", f"Solo hay {p['stock']} unidades", "error")
            return

        vtas.registrar(p["id"], p["nombre"], cant, self._pv, self._pc, metodo)
        prods.descontar_stock(p["id"], cant)

        msg(self.page, "Venta registrada",
            f"{cant}x {p['nombre']}\n{metodo}\n₡{cant * self._pv:,.0f}", "ok")
        self.combo.value = ""
        self.cant.value = ""
        self._selected_id = None
        self.lbl_precio.value = "Precio: ₡0"
        self.lbl_stock.value = "Stock disponible: —"
        self.lbl_subtotal.value = "Subtotal: ₡0"
        self.lbl_ganancia.value = "Ganancia: ₡0"
        # Refresh product list
        self.combo.options = [ft.dropdown.Option(f"{p['id']} - {p['nombre']}") for p in prods.listar_con_stock()]
        self.page.update()
