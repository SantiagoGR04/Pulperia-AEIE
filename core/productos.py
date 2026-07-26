"""Lógica de negocio — Productos"""
from database.excel_db import todos_productos, insertar_producto, actualizar_producto, eliminar_producto


def listar():
    return todos_productos()


def listar_con_stock():
    return [p for p in todos_productos() if p["stock"] > 0]


def obtener(pid):
    for p in todos_productos():
        if p["id"] == pid:
            return p
    return None


def crear(nombre, precio_compra, precio_venta, stock, categoria):
    prods = todos_productos()
    nid = max((p["id"] for p in prods), default=0) + 1
    insertar_producto([nid, nombre, precio_compra, precio_venta, stock, categoria])
    return nid


def editar(pid, **campos):
    for k, v in campos.items():
        actualizar_producto(pid, k, v)


def eliminar_por_id(pid):
    eliminar_producto(pid)


def buscar(filtro=""):
    if not filtro:
        return listar()
    f = filtro.lower()
    return [p for p in listar() if f in p["nombre"].lower()]


def descontar_stock(pid, cantidad):
    prod = obtener(pid)
    if prod:
        actualizar_producto(pid, "stock", prod["stock"] - cantidad)
