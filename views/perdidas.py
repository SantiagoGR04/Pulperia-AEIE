"""Vista: Registro de Pérdidas"""
import flet as ft
from core import productos as prods, perdidas as perd
from theme import Colors
from utils.dialogs import msg


class PerdidasView:
    def __init__(self, page):
        self.page = page

    def build(self):
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Producto", size=15, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Cant", size=15, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Monto", size=15, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Motivo", size=15, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Fecha", size=15, weight=ft.FontWeight.BOLD)),
            ],
            rows=[], border_radius=8,
            horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_300),
            column_spacing=25,
        )

        self._cargar_tabla()

        return ft.Column([
            ft.Row([
                ft.Text("⚠️ Pérdidas", size=20, weight=ft.FontWeight.BOLD, color=Colors.DANGER),
                ft.Container(expand=True),
                ft.Button(content=ft.Text("⚠️ Nueva"),
                    style=ft.ButtonStyle(bgcolor=Colors.DANGER, color=ft.Colors.WHITE),
                    on_click=lambda e: self._formulario(), height=50),
            ]),
            ft.Divider(height=2, color=Colors.ACCENT),
            ft.Container(
                content=ft.Column([self.tabla], scroll=ft.ScrollMode.AUTO),
                expand=True, bgcolor=ft.Colors.WHITE, border_radius=12, padding=10,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=8, color=Colors.CARD_SHADOW),
            ),
        ], expand=True)

    def _cargar_tabla(self):
        self.tabla.rows.clear()
        for p in perd.ultimas(50):
            self.tabla.rows.append(ft.DataRow([
                ft.DataCell(ft.Text(p["producto_nombre"] or "")),
                ft.DataCell(ft.Text(str(p["cantidad"] or ""))),
                ft.DataCell(ft.Text(f"₡{p['monto_estimado']:,.0f}" if p['monto_estimado'] else "₡0")),
                ft.DataCell(ft.Text(p["motivo"] or "")),
                ft.DataCell(ft.Text(p["fecha"][:10] if p["fecha"] else "")),
            ]))
        self.page.update()

    def _formulario(self):
        prods_list = prods.listar()
        opciones = [f"{p['id']} - {p['nombre']}" for p in prods_list] + ["Otro (nombre libre)"]

        e_prod = ft.Dropdown(label="Producto", options=[ft.dropdown.Option(o) for o in opciones], width=350)
        e_cant = ft.TextField(label="Cantidad", width=350, keyboard_type=ft.KeyboardType.NUMBER)
        e_monto = ft.TextField(label="Monto (₡)", width=350, keyboard_type=ft.KeyboardType.NUMBER)
        e_motivo = ft.Dropdown(label="Motivo",
            options=[ft.dropdown.Option(m) for m in [
                "No se registró venta", "Robo/Hurto", "Daño/Caducó",
                "Error de inventario", "Otro"
            ]], value="No se registró venta", width=350)

        def guardar(e):
            txt = e_prod.value or ""
            pid = None; pnom = txt
            try:
                pid = int(txt.split(" - ")[0])
                p = prods.obtener(pid)
                if p: pnom = p["nombre"]
            except:
                pnom = txt.replace("Otro (nombre libre)", "No identificado") if "Otro" in txt else txt
            try:
                cant = int(e_cant.value) if e_cant.value else 0
            except: cant = 0
            try:
                monto = float(e_monto.value) if e_monto.value else 0
            except: monto = 0

            perd.registrar(pid, pnom, cant, monto, e_motivo.value)
            self.page.pop_dialog()
            self._cargar_tabla()

        dlg = ft.AlertDialog(
            title=ft.Text("Registrar Pérdida"),
            content=ft.Column([e_prod, e_cant, e_monto, e_motivo,
                ft.Button(content=ft.Text("💾 Guardar"), on_click=guardar, style=ft.ButtonStyle(bgcolor=Colors.DANGER, color=ft.Colors.WHITE)),
            ], tight=True, scroll=ft.ScrollMode.AUTO),
            actions=[ft.TextButton("Cancelar", on_click=lambda e: self.page.pop_dialog())],
        )
        self.page.show_dialog(dlg)
