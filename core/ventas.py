"""Lógica de negocio — Ventas"""
from datetime import datetime as dt
from database.excel_db import todos, insertar


def registrar(pid, nombre, cantidad, precio_venta, precio_compra, metodo_pago):
    subtotal = cantidad * precio_venta
    ganancia = cantidad * (precio_venta - precio_compra)
    ventas = todos("ventas", "ventas")
    nid = max((v["id"] for v in ventas), default=0) + 1
    ahora = dt.now()
    fecha = ahora.strftime("%d/%m/%Y")
    hora = ahora.strftime("%H:%M")
    insertar("ventas", "ventas", [
        nid, pid, nombre, cantidad, precio_venta,
        subtotal, ganancia, metodo_pago, fecha, hora
    ])
    return nid


def listar():
    return todos("ventas", "ventas")


def listar_por_periodo(inicio):
    ventas = todos("ventas", "ventas")
    return [v for v in ventas if _fecha_valida(v, inicio)]


def _fecha_valida(v, inicio):
    try:
        f = dt.strptime(v["fecha"], "%d/%m/%Y")
        return f >= inicio
    except:
        try:
            f = dt.fromisoformat(v["fecha"])
            return f >= inicio
        except:
            return False


def resumen(ventas):
    return {
        "cantidad":   sum(v["cantidad"] or 0 for v in ventas),
        "subtotal":   sum(v["subtotal"] or 0 for v in ventas),
        "ganancia":   sum(v["ganancia"] or 0 for v in ventas),
        "efectivo":   sum(v["subtotal"] or 0 for v in ventas if v.get("metodo_pago") == "Efectivo"),
        "sinpe":      sum(v["subtotal"] or 0 for v in ventas if v.get("metodo_pago") == "SINPE"),
    }


def resumen_global():
    return resumen(todos("ventas", "ventas"))


def resumen_hoy():
    hoy = dt.now().strftime("%d/%m/%Y")
    ventas_hoy = [v for v in todos("ventas", "ventas") if v.get("fecha") == hoy]
    return resumen(ventas_hoy)
