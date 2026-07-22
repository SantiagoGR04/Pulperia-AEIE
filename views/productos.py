"""Vista: Gestión de Productos"""
import flet as ft
import threading, os
from datetime import datetime
from tkinter import Tk, filedialog
from openpyxl import Workbook
from core import productos as prods
from theme import Colors
from utils.dialogs import msg
from config import CATEGORIAS


class ProductosView:
    def __init__(self, page):
        self.page = page

    def build(self):
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", size=11, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Producto", size=11, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Compra (₡)", size=11, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Venta (₡)", size=11, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Stock", size=11, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Categoría", size=11, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("", size=11)),
            ],
            rows=[],
            border_radius=8,
            horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_300),
            column_spacing=25,
        )

        self.search = ft.TextField(
            hint_text="Buscar…", prefix_icon=ft.Icons.SEARCH,
            width=300, height=40, on_change=lambda e: self._cargar(),
            border_radius=20, bgcolor=ft.Colors.WHITE,
        )

        self._cargar()
        return ft.Column([
            ft.Row([
                ft.Text("📦 Productos", size=20, weight=ft.FontWeight.BOLD, color=Colors.PRIMARY),
                ft.Container(expand=True), self.search,

                ft.Button(content=ft.Text("➕ Nuevo"),
                    style=ft.ButtonStyle(bgcolor=Colors.PRIMARY, color=ft.Colors.WHITE),
                    on_click=lambda e: self._formulario(), height=48),
            ]),
            ft.Divider(height=2, color=Colors.ACCENT),
            ft.Container(
                content=self.tabla, expand=True,
                bgcolor=ft.Colors.WHITE, border_radius=12, padding=10,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=8, color=Colors.CARD_SHADOW),
            ),
        ], expand=True)

    def _cargar(self):
        self.tabla.rows.clear()
        filtro = self.search.value.strip().lower() if self.search.value else ""
        for p in prods.buscar(filtro):
            self.tabla.rows.append(ft.DataRow([
                ft.DataCell(ft.Text(str(p["id"]))),
                ft.DataCell(ft.Text(p["nombre"], weight=ft.FontWeight.W_500)),
                ft.DataCell(ft.Text(f"₡{p['precio_compra']:,.0f}")),
                ft.DataCell(ft.Text(f"₡{p['precio_venta']:,.0f}")),
                ft.DataCell(ft.Text(str(p["stock"]),
                    color=Colors.DANGER if (p["stock"] or 0) == 0 else Colors.TEXT_PRIM)),
                ft.DataCell(ft.Text(p["categoria"] or "")),
                ft.DataCell(ft.Row([
                    ft.IconButton(ft.Icons.EDIT, icon_size=18, data=p["id"],
                        on_click=lambda e: self._formulario(int(e.control.data))),
                    ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_size=18, data=p["id"],
                        on_click=lambda e: self._eliminar(int(e.control.data)),
                        icon_color=Colors.DANGER),
                ])),
            ]))
        self.page.update()

    def _eliminar(self, pid):
        d = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text("¿Eliminar este producto?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.pop_dialog()),
                ft.TextButton("Eliminar", on_click=lambda e: (
                    prods.eliminar_por_id(pid), self.page.pop_dialog(), self._cargar(), self.page.update()
                ), style=ft.ButtonStyle(color=Colors.DANGER)),
            ],
        )
        self.page.show_dialog(d)

    def _exportar(self):
        def t():
            root = Tk(); root.withdraw()
            fn = filedialog.asksaveasfilename(title="Guardar inventario",
                defaultextension=".xlsx", filetypes=[("Excel files","*.xlsx")],
                initialfile=f"inventario_{datetime.now().strftime('%Y%m%d')}.xlsx")
            root.destroy()
            if not fn: return
            wb = Workbook()
            ws = wb.active; ws.title = "Inventario"
            ws.append(["ID","Producto","Precio Compra","Precio Venta","Stock","Categoría"])
            for p in prods.listar():
                ws.append([p["id"], p["nombre"], p["precio_compra"],
                          p["precio_venta"], p["stock"], p["categoria"]])
            for col in ws.columns:
                ws.column_dimensions[col[0].column_letter].width = max(len(str(c.value or "")) for c in col) + 3
            wb.save(fn)
            def mostrar():
                self.page.show_dialog(ft.AlertDialog(
                    title=ft.Text("✅ Exportado"),
                    content=ft.Text(f"Guardado: {os.path.basename(fn)}"),
                    actions=[ft.TextButton("OK", on_click=lambda e: self.page.pop_dialog())]
                ))
            self.page.run_thread(mostrar)
        threading.Thread(target=t, daemon=True).start()

    def _formulario(self, pid=None):
        prod = prods.obtener(pid) if pid else None
        editando = prod is not None

        e_nombre = ft.TextField(label="Nombre", value=prod["nombre"] if editando else "", width=300)
        e_compra = ft.TextField(label="Precio compra (₡)", value=str(prod["precio_compra"]) if editando else "", width=300, keyboard_type=ft.KeyboardType.NUMBER)
        e_venta  = ft.TextField(label="Precio venta (₡)", value=str(prod["precio_venta"]) if editando else "", width=300, keyboard_type=ft.KeyboardType.NUMBER)
        e_stock  = ft.TextField(label="Stock", value=str(prod["stock"]) if editando else "", width=300, keyboard_type=ft.KeyboardType.NUMBER)
        e_cat    = ft.Dropdown(label="Categoría", options=[ft.dropdown.Option(c) for c in CATEGORIAS],
                               value=prod["categoria"] if editando else CATEGORIAS[0], width=300)

        def guardar(e):
            try:
                nom = e_nombre.value.strip()
                if not nom:
                    msg(self.page, "Error", "Nombre requerido", "error")
                    return
                if editando:
                    prods.editar(pid, nombre=nom, precio_compra=float(e_compra.value),
                                 precio_venta=float(e_venta.value), stock=int(e_stock.value),
                                 categoria=e_cat.value)
                else:
                    prods.crear(nom, float(e_compra.value), float(e_venta.value),
                                int(e_stock.value), e_cat.value)
                self.page.pop_dialog()
                self._cargar()
                self.page.update()
            except ValueError:
                msg(self.page, "Error", "Precios y stock deben ser números", "error")

        dlg = ft.AlertDialog(
            title=ft.Text("Editar" if editando else "Nuevo Producto"),
            content=ft.Column([e_nombre, e_compra, e_venta, e_stock, e_cat,
                ft.Button(content=ft.Text("💾 Guardar"), on_click=guardar, style=ft.ButtonStyle(bgcolor=Colors.PRIMARY, color=ft.Colors.WHITE)),
            ], tight=True, scroll=ft.ScrollMode.AUTO),
            actions=[ft.TextButton("Cancelar", on_click=lambda e: self.page.pop_dialog())],
        )
        self.page.show_dialog(dlg)
