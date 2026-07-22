"""Capa de datos — dos archivos Excel separados"""
import os
from openpyxl import Workbook, load_workbook
from config import DATA_DIR, INVENTARIO_FILE, VENTAS_FILE, INVENTARIO_SHEETS, VENTAS_SHEETS


def _init_sheet(wb, name, cols):
    ws = wb.create_sheet(title=name)
    for i, col in enumerate(cols, 1):
        ws.cell(row=1, column=i, value=col)
    ws.freeze_panes = "A2"
    return ws


def _asegurar_columnas(archivo, sheets_def):
    """Agrega columnas faltantes sin borrar datos existentes"""
    wb = load_workbook(archivo)
    cambio = False
    for name, cols in sheets_def.items():
        if name not in wb.sheetnames:
            _init_sheet(wb, name, cols)
            cambio = True
            continue
        ws = wb[name]
        existentes = [ws.cell(row=1, column=c).value for c in range(1, ws.max_column + 1)]
        for i, col in enumerate(cols):
            if col not in existentes:
                ws.cell(row=1, column=len(existentes) + 1, value=col)
                existentes.append(col)
                cambio = True
    if cambio:
        wb.save(archivo)
    wb.close()


def inicializar():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(INVENTARIO_FILE):
        wb = Workbook()
        wb.remove(wb.active)
        for name, cols in INVENTARIO_SHEETS.items():
            _init_sheet(wb, name, cols)
        wb.save(INVENTARIO_FILE)
    else:
        _asegurar_columnas(INVENTARIO_FILE, INVENTARIO_SHEETS)

    if not os.path.exists(VENTAS_FILE):
        wb = Workbook()
        wb.remove(wb.active)
        for name, cols in VENTAS_SHEETS.items():
            _init_sheet(wb, name, cols)
        wb.save(VENTAS_FILE)
    else:
        _asegurar_columnas(VENTAS_FILE, VENTAS_SHEETS)


def _conectar(archivo):
    if archivo == "inventario":
        inicializar()
        return load_workbook(INVENTARIO_FILE)
    inicializar()
    return load_workbook(VENTAS_FILE)


def _guardar(archivo, wb):
    if archivo == "inventario":
        wb.save(INVENTARIO_FILE)
    else:
        wb.save(VENTAS_FILE)


def insertar(archivo, hoja, datos):
    wb = _conectar(archivo)
    ws = wb[hoja]
    ws.append(datos)
    _guardar(archivo, wb)


def actualizar(archivo, hoja, id_reg, columna, valor):
    wb = _conectar(archivo)
    ws = wb[hoja]
    cols = list_sheets(archivo)[hoja]
    col_idx = cols.index(columna) + 1
    for r in range(2, ws.max_row + 1):
        if ws.cell(row=r, column=1).value == id_reg:
            ws.cell(row=r, column=col_idx, value=valor)
            break
    _guardar(archivo, wb)


def eliminar(archivo, hoja, id_reg):
    wb = _conectar(archivo)
    ws = wb[hoja]
    for r in range(2, ws.max_row + 1):
        if ws.cell(row=r, column=1).value == id_reg:
            ws.delete_rows(r)
            break
    _guardar(archivo, wb)


def todos(archivo, hoja):
    wb = _conectar(archivo)
    ws = wb[hoja]
    cols = list_sheets(archivo)[hoja]
    resultados = []
    for r in range(2, ws.max_row + 1):
        fila = {}
        for i, col in enumerate(cols, 1):
            fila[col] = ws.cell(row=r, column=i).value
        if fila[cols[0]] is not None:
            resultados.append(fila)
    wb.close()
    return resultados


def obtener_por_id(archivo, hoja, id_reg):
    for p in todos(archivo, hoja):
        if p["id"] == id_reg:
            return p
    return None


def list_sheets(archivo):
    if archivo == "inventario":
        return INVENTARIO_SHEETS
    return VENTAS_SHEETS
