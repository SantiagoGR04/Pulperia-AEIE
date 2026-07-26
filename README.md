# Pulpería AEIE

App de escritorio para gestión de pulpería, con temática de Ingeniería Eléctrica.

## 🚀 Descarga rápida

Ve a **Releases** → descarga el `.exe` más reciente, ejecútalo y ya. Sin instalar Python ni dependencias.

## 📦 Requisitos (para desarrollo / clonar)

- **Python 3.8+**
- **Flet** (`pip install flet`)
- **openpyxl** (`pip install openpyxl`)
- **python-dotenv** (`pip install python-dotenv`)

```bash
pip install flet openpyxl python-dotenv
```

## ▶️ Ejecutar

```bash
python app.py
```

## 🏗️ Empaquetar para distribución

```bash
pip install pyinstaller
flet pack app.py -n Pulperia --hidden-import openpyxl -y
```

El `.exe` generado está en `dist/Pulperia.exe`.

## ⚙️ Funcionalidades

| Vista | Descripción |
|-------|-------------|
| **📊 Dashboard** | Resumen: productos, ventas hoy, ganancia total, pérdidas |
| **📦 Productos** | CRUD con precios (compra/venta), stock, categorías |
| **🧾 Venta** | Registrar efectivo o SINPE, descuenta inventario automático |
| **⚠️ Pérdidas** | Registrar faltantes, robos, daños |
| **📈 Reportes** | Ventas por período, desglose por método de pago, inventario valorizado, exportación a Excel |

## 💾 Almacenamiento

Los datos se guardan en `Pulperia_Data/` en formato Excel:

- **`productos.xlsx`** — Catálogo de productos
- **`ventas_AÑO.xlsx`** — Ventas, una hoja por mes (Enero, Febrero…)
- **`perdidas_AÑO.xlsx`** — Pérdidas, una hoja por mes

Cada año nuevo genera su propio archivo automáticamente.

## 🧱 Estructura del proyecto

```
Pulperia-AEIE/
├── app.py                  # Punto de entrada
├── config.py               # Configuración global
├── theme.py                # Paleta de colores y estilos
├── database/
│   └── excel_db.py         # CRUD sobre Excel (año/mes)
├── core/
│   ├── productos.py        # Lógica de productos
│   ├── ventas.py           # Lógica de ventas
│   └── perdidas.py         # Lógica de pérdidas
├── views/
│   ├── dashboard.py        # Panel principal
│   ├── productos.py        # Gestión de productos
│   ├── venta.py            # Registrar venta
│   ├── perdidas.py         # Registrar pérdidas
│   └── reportes.py         # Reportes y exportación
├── utils/
│   └── dialogs.py          # Diálogos reutilizables
└── images/
    └── logo_aeie.png       # Logo de la app
```
