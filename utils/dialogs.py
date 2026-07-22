"""Utilidades compartidas"""
import flet as ft


def msg(page, titulo, texto, tipo="info"):
    c = ft.Colors.GREEN if tipo == "ok" else ft.Colors.RED if tipo == "error" else ft.Colors.BLUE
    d = ft.AlertDialog(
        title=ft.Text(titulo, color=c),
        content=ft.Text(texto),
        actions=[ft.TextButton("OK", on_click=lambda e: page.pop_dialog())],
    )
    page.show_dialog(d)
