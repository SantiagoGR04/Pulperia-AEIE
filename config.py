"""Configuración de Pulpería App (Flet)"""
import os
import sys

# Si es PyInstaller, guarda datos junto al binario. Si no, en el proyecto.
if getattr(sys, 'frozen', False):
    PROJECT_ROOT = os.path.dirname(os.path.abspath(sys.executable))
else:
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "Pulperia_Data")
EXCEL_FILE = os.path.join(DATA_DIR, "pulperia.xlsx")

SHEETS = {
    "productos": ["id", "nombre", "precio_compra", "precio_venta", "stock", "categoria"],
    "ventas":    ["id", "producto_id", "producto_nombre", "cantidad", "precio_unitario", "subtotal", "ganancia", "fecha"],
    "perdidas":  ["id", "producto_id", "producto_nombre", "cantidad", "monto_estimado", "motivo", "fecha"],
}

APP_NAME = "Pulpería IE"
APP_WIDTH  = 1100
APP_HEIGHT = 750

CATEGORIAS = [
    "Alimentos", "Bebidas", "Limpieza", "Lácteos",
    "Panadería", "Snacks", "Higiene", "Otros"
]
