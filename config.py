"""Configuración de Pulpería App (Flet)"""
import os
import sys

if getattr(sys, 'frozen', False):
    PROJECT_ROOT = os.path.dirname(os.path.abspath(sys.executable))
else:
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "Pulperia_Data")
INVENTARIO_FILE = os.path.join(DATA_DIR, "inventario.xlsx")
VENTAS_FILE = os.path.join(DATA_DIR, "ventas.xlsx")

INVENTARIO_SHEETS = {
    "productos": ["id", "nombre", "precio_compra", "precio_venta", "stock", "categoria"],
    "perdidas":  ["id", "producto_id", "producto_nombre", "cantidad", "monto_estimado", "motivo", "fecha"],
}

VENTAS_SHEETS = {
    "ventas": ["id", "producto_id", "producto_nombre", "cantidad", "precio_unitario", "subtotal", "ganancia", "metodo_pago", "fecha", "hora"],
}

APP_NAME = "Pulpería AEIE"
APP_WIDTH  = 1100
APP_HEIGHT = 750

CATEGORIAS = [
    "Dulces", "Bebidas","Snacks","Otros"]

METODOS_PAGO = ["Efectivo", "SINPE"]
