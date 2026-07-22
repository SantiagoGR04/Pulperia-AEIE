"""Paleta de colores y estilos compartidos — Ingeniería Eléctrica"""
import flet as ft

class Colors:
    PRIMARY    = "#0D47A1"
    PRIMARY_DK = "#002171"
    PRIMARY_LT = "#5472D3"
    ACCENT     = "#FFC107"
    ACCENT_DK  = "#FF8F00"
    SURFACE    = "#FFFFFF"
    BG         = "#F0F2F5"
    TEXT_PRIM  = "#1A1A2E"
    TEXT_SEC   = "#546E7A"
    SUCCESS    = "#2E7D32"
    DANGER     = "#C62828"
    WARNING    = "#E65100"
    CARD_SHADOW = "#1A000000"


def card(content, bg=ft.Colors.WHITE, padding=15, expand=False):
    return ft.Container(
        content=content,
        bgcolor=bg,
        border_radius=12,
        padding=padding,
        expand=expand,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=8, color=Colors.CARD_SHADOW),
    )
