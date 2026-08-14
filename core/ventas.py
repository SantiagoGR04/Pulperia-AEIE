"""Lógica de negocio — Ventas"""
from datetime import datetime as dt
from database.excel_db import todas_ventas, insertar_venta


def registrar(pid, nombre, cantidad, precio_venta, precio_compra, metodo_pago, efectivo_recibido):
    subtotal = cantidad * precio_venta
    ganancia = cantidad * (precio_venta - precio_compra)
    vuelto = efectivo_recibido - subtotal if metodo_pago == "Efectivo" else 0
    ventas = todas_ventas()
    nid = max((v["id"] for v in ventas), default=0) + 1
    ahora = dt.now()
    fecha = ahora.strftime("%d/%m/%Y")
    hora = ahora.strftime("%H:%M")
    insertar_venta([
        nid, pid, nombre, cantidad, precio_venta,
        subtotal, ganancia, metodo_pago, fecha, hora
    ])
    return nid,vuelto


def listar():
    return todas_ventas()


def listar_por_periodo(inicio):
    ventas = todas_ventas()
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
    return resumen(todas_ventas())


def resumen_hoy():
    hoy = dt.now().strftime("%d/%m/%Y")
    ventas_hoy = [v for v in todas_ventas() if v.get("fecha") == hoy]
    return resumen(ventas_hoy)
