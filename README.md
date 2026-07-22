# Pulpería-AEIE

App de escritorio para gestión de pulpería, con temática de Ingeniería Eléctrica.

## Funcionalidades

- 📦 **Gestión de productos** — ABM con precios, stock y categorías
- 🧾 **Ventas** — Registrar ventas en efectivo o SINPE, descuenta inventario automáticamente
- ⚠️ **Pérdidas** — Registrar faltantes no contabilizados
- 📈 **Reportes** — Ventas por período con desglose efectivo/SINPE, exportación a Excel
- 💾 **Almacenamiento** — Todo en Excel (`Pulperia_Data/pulperia.xlsx`)

## Requisitos

- Python 3.8+
- [Flet](https://flet.dev)
- openpyxl

```
pip install flet openpyxl
```

## Ejecutar

```bash
python app.py
```

## Empaquetar

### Linux

```bash
pip install pyinstaller flet-web
flet pack app.py -n Pulperia --hidden-import openpyxl -y
```

### Windows (PowerShell)

```powershell
pip install flet openpyxl flet-web pyinstaller
flet pack app.py -n Pulperia --hidden-import openpyxl -y
```

## Estructura del proyecto

```
Pulperia-AEIE/
├── app.py                  # Punto de entrada
├── config.py               # Configuración global
├── theme.py                # Colores y estilos IE
├── database/
│   └── excel_db.py         # CRUD sobre Excel
├── core/
│   ├── productos.py        # Lógica de productos
│   ├── ventas.py           # Lógica de ventas
│   └── perdidas.py         # Lógica de pérdidas
├── views/
│   ├── dashboard.py        # Vista principal
│   ├── productos.py        # Gestión productos
│   ├── venta.py            # Registrar venta
│   ├── perdidas.py         # Registrar pérdidas
│   └── reportes.py         # Reportes y exportación
└── utils/
    └── dialogs.py          # Diálogos reutilizables
```
