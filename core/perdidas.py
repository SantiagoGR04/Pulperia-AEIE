"""Lógica de negocio — Pérdidas"""
from datetime import datetime
from database.excel_db import todos_perdidas, insertar_perdida


def registrar(pid, nombre, cantidad, monto, motivo):
    perdidas = todos_perdidas()
    nid = max((p["id"] for p in perdidas), default=0) + 1
    insertar_perdida([
        nid, pid, nombre, cantidad, monto, motivo, datetime.now().isoformat()
    ])
    return nid


def listar():
    return todos_perdidas()


def total_monto():
    return sum(p["monto_estimado"] or 0 for p in todos_perdidas())


def ultimas(limite=50):
    return list(reversed(todos_perdidas()[-limite:]))
