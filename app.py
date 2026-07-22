"""Pulpería IE — Punto de entrada
App de escritorio para gestión de pulpería
Temática: Escuela de Ingeniería Eléctrica (azul / ámbar)
"""
import flet as ft
from database.excel_db import inicializar
from config import APP_NAME, APP_WIDTH, APP_HEIGHT
from theme import Colors
from views.dashboard import DashboardView
from views.productos import ProductosView
from views.venta import VentaView
from views.perdidas import PerdidasView
from views.reportes import ReportesView


def main(page: ft.Page):
    page.title = APP_NAME
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = Colors.BG
    page.padding = 0
    page.window_width = APP_WIDTH
    page.window_height = APP_HEIGHT
    page.window_min_width = 900
    page.window_min_height = 600
    page.window_top = 100
    page.window_left = 100

    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(primary=Colors.PRIMARY, secondary=Colors.ACCENT),
        font_family="Segoe UI",
    )

    inicializar()
    content_area = ft.Container(expand=True, padding=20)

    def cambiar_vista(nombre):
        content_area.content = None
        content_area.update()
        vistas = {
            "dashboard": lambda: DashboardView(page, cambiar_vista).build(),
            "productos": lambda: ProductosView(page).build(),
            "venta":     lambda: VentaView(page).build(),
            "perdidas":  lambda: PerdidasView(page).build(),
            "reportes":  lambda: ReportesView(page).build(),
        }
        v = vistas.get(nombre)
        if v:
            content_area.content = v()
        content_area.update()

    sidebar = ft.Container(
        width=220, bgcolor=Colors.PRIMARY_DK, padding=0,
        content=ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.BOLT, size=36, color=Colors.ACCENT),
                    ft.Text("Pulpería IE", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text("Ing. Eléctrica", size=12, color=ft.Colors.GREY_400),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20, bgcolor=Colors.PRIMARY,
            ),
            ft.Divider(height=1, color=Colors.ACCENT),
            ft.Container(expand=True, content=ft.Column([
                ft.ListTile(leading=ft.Icon(ft.Icons.DASHBOARD, color=ft.Colors.WHITE),
                    title=ft.Text("Dashboard", color=ft.Colors.WHITE),
                    on_click=lambda e: cambiar_vista("dashboard")),
                ft.ListTile(leading=ft.Icon(ft.Icons.INVENTORY_2, color=ft.Colors.WHITE70),
                    title=ft.Text("Productos", color=ft.Colors.WHITE),
                    on_click=lambda e: cambiar_vista("productos")),
                ft.ListTile(leading=ft.Icon(ft.Icons.SHOPPING_CART, color=ft.Colors.WHITE70),
                    title=ft.Text("Venta", color=ft.Colors.WHITE),
                    on_click=lambda e: cambiar_vista("venta")),
                ft.ListTile(leading=ft.Icon(ft.Icons.WARNING_AMBER, color=ft.Colors.WHITE70),
                    title=ft.Text("Pérdidas", color=ft.Colors.WHITE),
                    on_click=lambda e: cambiar_vista("perdidas")),
                ft.ListTile(leading=ft.Icon(ft.Icons.BAR_CHART, color=ft.Colors.WHITE70),
                    title=ft.Text("Reportes", color=ft.Colors.WHITE),
                    on_click=lambda e: cambiar_vista("reportes")),
            ], spacing=0)),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ELECTRIC_BOLT, size=14, color=Colors.ACCENT),
                    ft.Text("IE-UCR", size=11, color=ft.Colors.GREY_500),
                ], alignment=ft.MainAxisAlignment.CENTER),
                padding=10,
            ),
        ]),
    )

    page.add(ft.Row([sidebar, content_area], expand=True, spacing=0))
    cambiar_vista("dashboard")


ft.run(main)
