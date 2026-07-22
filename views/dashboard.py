"""Vista: Dashboard principal con resumen"""
import flet as ft
from datetime import datetime
from core import ventas as vtas, perdidas as perd, productos as prods
from theme import Colors, card
from config import APP_NAME


class DashboardView:
    def __init__(self, page, navegar):
        self.page = page
        self._navegar = navegar

    def build(self):
        prods_list = prods.listar()
        r_hoy = vtas.resumen_hoy()
        r_global = vtas.resumen_global()
        perdidas_total = perd.total_monto()
        bajo_stock = len(prods.stock_bajo(3))

        def _card(icon, label, valor, bg, icon_color=Colors.ACCENT):
            return ft.Container(
                content=ft.Column([
                    ft.Row([ft.Icon(icon, color=icon_color, size=28), ft.Container(expand=True)]),
                    ft.Text(valor, size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(label, size=13, color=ft.Colors.WHITE70),
                ], spacing=5),
                bgcolor=bg, padding=20, border_radius=16, expand=True,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=Colors.CARD_SHADOW),
            )

        return ft.Column([
            ft.Row([
                ft.Text("⚡ Dashboard", size=22, weight=ft.FontWeight.BOLD, color=Colors.PRIMARY),
                ft.Container(expand=True),
                ft.Text(datetime.now().strftime("%A, %d %B %Y"), size=13, color=Colors.TEXT_SEC),
            ]),
            ft.Divider(height=2, color=Colors.ACCENT),
            ft.Row([
                _card(ft.Icons.INVENTORY, "Productos", str(len(prods_list)), Colors.PRIMARY),
                _card(ft.Icons.TRENDING_UP, "Ventas hoy", f"₡{r_hoy['subtotal']:,.0f}", Colors.SUCCESS),
                _card(ft.Icons.ACCOUNT_BALANCE, "Ganancia total", f"₡{r_global['ganancia']:,.0f}", "#1565C0"),
                _card(ft.Icons.WARNING, "Pérdidas", f"₡{perdidas_total:,.0f}", Colors.DANGER, ft.Colors.WHITE),
            ], spacing=15),
            ft.Row([
                card(ft.Column([
                    ft.Text("📋 Resumen Rápido", size=16, weight=ft.FontWeight.BOLD, color=Colors.PRIMARY),
                    ft.Divider(),
                    ft.Text(f"🔴 Stock bajo (≤3): {bajo_stock}",
                            color=Colors.DANGER if bajo_stock > 0 else Colors.TEXT_SEC),
                    ft.Text(f"💰 Efectivo hoy: ₡{r_hoy['efectivo']:,.0f}"),
                    ft.Text(f"💳 SINPE hoy: ₡{r_hoy['sinpe']:,.0f}"),
                    ft.Text(f"📦 Total ventas: {sum(1 for _ in vtas.listar())}"),
                ]), expand=True),
                card(ft.Column([
                    ft.Text("🎯 Accesos Rápidos", size=16, weight=ft.FontWeight.BOLD, color=Colors.PRIMARY),
                    ft.Divider(),
                    ft.Button(content=ft.Text("➕ Nuevo Producto"),
                        on_click=lambda e: self._navegar("productos"), width=200),
                    ft.Button(content=ft.Text("🧾 Venta"),
                        on_click=lambda e: self._navegar("venta"), width=200),
                    ft.Button(content=ft.Text("📊 Reportes"),
                        on_click=lambda e: self._navegar("reportes"), width=200),
                ], spacing=10), expand=True),
            ]),
        ], expand=True)
