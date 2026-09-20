# Sistema de Gestión de Préstamos de Equipos de Laboratorio

## 1. Estructura del proyecto

```text
eva_proyecto_sdd_srs_pytest/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── datos_iniciales.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── equipo.py
│   │   └── prestamo.py
│   │
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── validador_usuario.py
│   │   ├── validador_equipo.py
│   │   └── validador_prestamo.py
│   │
│   ├── persistencia/
│   │   ├── __init__.py
│   │   ├── repositorio_usuario.py
│   │   ├── repositorio_equipo.py
│   │   └── repositorio_prestamo.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── servicio_usuario.py
│   │   ├── servicio_equipo.py
│   │   └── servicio_prestamo.py
│   │
│   └── ui/
│       ├── __init__.py
│       └── interfaz_principal.py
│
├── data/
│   └── prestamos.db
│
├── scripts/
│   └── poblar_base_datos.py
│
├── tests/
│   ├── conftest.py
│   ├── test_users.py
│   ├── test_equipment.py
│   ├── test_loans.py
│   └── test_requisitos_tecnicos.py
│
├── main.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## 2. Qué se necesita instalar

Se necesita:

- Python 3.11 o superior
- Pytest

SQLite y Tkinter vienen incluidos normalmente con Python.

### Verificar Python

```powershell
python --version
```

### Verificar Tkinter

```powershell
python -m tkinter
```

### Verificar SQLite

```powershell
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

### Instalar Pytest

Desde la carpeta del proyecto ejecutar:

```powershell
python -m pip install -r requirements.txt
```

---

## 3. Pasos para ejecutar el proyecto

### Paso 1. Entrar a la carpeta del proyecto

```powershell
cd "RUTA_DEL_PROYECTO\eva_proyecto_sdd_srs_pytest"
```

### Paso 2. Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

### Paso 3. Crear la población inicial

```powershell
python scripts/poblar_base_datos.py
```

Debe mostrar:

```text
Población inicial cargada correctamente.
Usuarios: 100
Equipos: 50
Préstamos: 150
Estados: {'ACTIVO': 15, 'ATRASADO': 15, 'DEVUELTO': 120}
```

### Paso 4. Ejecutar las pruebas

```powershell
python -m pytest -q
```

El resultado esperado es:

```text
35 passed
```

### Paso 5. Ejecutar la interfaz

```powershell
python main.py
```

Se abrirá la interfaz gráfica del sistema.