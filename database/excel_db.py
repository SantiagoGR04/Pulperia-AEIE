"""Capa de datos — Excel con openpyxl"""
import os
from openpyxl import Workbook, load_workbook
from config import EXCEL_FILE, SHEETS


def inicializar():
    if os.path.exists(EXCEL_FILE):
        return
    os.makedirs(os.path.dirname(EXCEL_FILE), exist_ok=True)
    wb = Workbook()
    wb.remove(wb.active)
    for name, cols in SHEETS.items():
        ws = wb.create_sheet(title=name)
        for i, col in enumerate(cols, 1):
            ws.cell(row=1, column=i, value=col)
        ws.freeze_panes = "A2"
    wb.save(EXCEL_FILE)


def _conectar():
    inicializar()
    return load_workbook(EXCEL_FILE)


def _guardar(wb):
    wb.save(EXCEL_FILE)


def insertar(hoja, datos):
    wb = _conectar()
    ws = wb[hoja]
    ws.append(datos)
    _guardar(wb)


def actualizar(hoja, id_reg, columna, valor):
    wb = _conectar()
    ws = wb[hoja]
    cols = SHEETS[hoja]
    col_idx = cols.index(columna) + 1
    for r in range(2, ws.max_row + 1):
        if ws.cell(row=r, column=1).value == id_reg:
            ws.cell(row=r, column=col_idx, value=valor)
            break
    _guardar(wb)


def eliminar(hoja, id_reg):
    wb = _conectar()
    ws = wb[hoja]
    for r in range(2, ws.max_row + 1):
        if ws.cell(row=r, column=1).value == id_reg:
            ws.delete_rows(r)
            break
    _guardar(wb)


def todos(hoja):
    wb = _conectar()
    ws = wb[hoja]
    cols = SHEETS[hoja]
    resultados = []
    for r in range(2, ws.max_row + 1):
        fila = {}
        for i, col in enumerate(cols, 1):
            fila[col] = ws.cell(row=r, column=i).value
        if fila[cols[0]] is not None:
            resultados.append(fila)
    wb.close()
    return resultados


def obtener_por_id(hoja, id_reg):
    for p in todos(hoja):
        if p["id"] == id_reg:
            return p
    return None
