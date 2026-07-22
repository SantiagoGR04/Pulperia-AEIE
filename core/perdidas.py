"""Lógica de negocio — Pérdidas"""
from datetime import datetime
from database.excel_db import todos, insertar


def registrar(pid, nombre, cantidad, monto, motivo):
    perdidas = todos("inventario", "perdidas")
    nid = max((p["id"] for p in perdidas), default=0) + 1
    insertar("inventario", "perdidas", [nid, pid, nombre, cantidad, monto, motivo, datetime.now().isoformat()])
    return nid


def listar():
    return todos("inventario", "perdidas")


def total_monto():
    return sum(p["monto_estimado"] or 0 for p in todos("inventario", "perdidas"))


def ultimas(limite=50):
    return list(reversed(todos("inventario", "perdidas")[-limite:]))
