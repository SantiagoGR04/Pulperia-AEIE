"""Lógica de negocio — Productos"""
from database.excel_db import todos, insertar, actualizar, eliminar


def listar():
    return todos("inventario", "productos")


def listar_con_stock():
    return [p for p in todos("inventario", "productos") if p["stock"] > 0]


def obtener(pid):
    for p in todos("inventario", "productos"):
        if p["id"] == pid:
            return p
    return None


def crear(nombre, precio_compra, precio_venta, stock, categoria):
    prods = todos("inventario", "productos")
    nid = max((p["id"] for p in prods), default=0) + 1
    insertar("inventario", "productos", [nid, nombre, precio_compra, precio_venta, stock, categoria])
    return nid


def editar(pid, **campos):
    for k, v in campos.items():
        actualizar("inventario", "productos", pid, k, v)


def eliminar_por_id(pid):
    eliminar("inventario", "productos", pid)


def buscar(filtro=""):
    if not filtro:
        return listar()
    f = filtro.lower()
    return [p for p in listar() if f in p["nombre"].lower()]


def stock_bajo(limite=3):
    return [p for p in listar() if (p["stock"] or 0) <= limite]


def descontar_stock(pid, cantidad):
    prod = obtener(pid)
    if prod:
        actualizar("inventario", "productos", pid, "stock", prod["stock"] - cantidad)
