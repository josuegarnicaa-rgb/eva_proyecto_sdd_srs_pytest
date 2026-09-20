import sqlite3
from pathlib import Path


RUTA_RAIZ = Path(__file__).resolve().parent.parent
RUTA_DATOS = RUTA_RAIZ / "data"
RUTA_BASE_DATOS = RUTA_DATOS / "prestamos.db"


def obtener_conexion(ruta_base_datos=RUTA_BASE_DATOS):
    """Abre una conexión SQLite con claves foráneas activas."""
    RUTA_DATOS.mkdir(exist_ok=True)

    conexion = sqlite3.connect(str(ruta_base_datos))
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")

    return conexion


def crear_tablas(conexion):
    """Crea las tablas y restricciones del sistema."""

    conexion.executescript(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre TEXT NOT NULL
                CHECK (
                    length(trim(nombre)) BETWEEN 2 AND 50
                ),

            apellido TEXT NOT NULL
                CHECK (
                    length(trim(apellido)) BETWEEN 2 AND 50
                ),

            correo TEXT NOT NULL UNIQUE
                CHECK (
                    length(correo) BETWEEN 3 AND 100
                )
        );


        CREATE TABLE IF NOT EXISTS equipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre TEXT NOT NULL
                CHECK (
                    length(trim(nombre)) BETWEEN 2 AND 80
                ),

            codigo TEXT NOT NULL UNIQUE
                CHECK (
                    length(codigo) BETWEEN 3 AND 10
                ),

            descripcion TEXT NOT NULL
                CHECK (
                    length(trim(descripcion)) BETWEEN 1 AND 250
                ),

            estado TEXT NOT NULL DEFAULT 'DISPONIBLE'
                CHECK (
                    estado IN ('DISPONIBLE', 'PRESTADO')
                )
        );


        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            usuario_id INTEGER NOT NULL
                CHECK (usuario_id > 0),

            equipo_id INTEGER NOT NULL
                CHECK (equipo_id > 0),

            fecha_prestamo TEXT NOT NULL,

            fecha_devolucion TEXT NOT NULL,

            estado TEXT NOT NULL DEFAULT 'ACTIVO'
                CHECK (
                    estado IN ('ACTIVO', 'DEVUELTO', 'ATRASADO')
                ),

            CHECK (
                date(fecha_devolucion) >= date(fecha_prestamo)
            ),

            FOREIGN KEY (usuario_id)
                REFERENCES usuarios(id),

            FOREIGN KEY (equipo_id)
                REFERENCES equipos(id)
        );


        CREATE UNIQUE INDEX IF NOT EXISTS
        idx_prestamo_activo_equipo
        ON prestamos(equipo_id)
        WHERE estado IN ('ACTIVO', 'ATRASADO');
        """
    )

    conexion.commit()


def inicializar_base_datos(ruta_base_datos=RUTA_BASE_DATOS):
    """Inicializa la base de datos indicada."""

    conexion = obtener_conexion(ruta_base_datos)

    try:
        crear_tablas(conexion)
    finally:
        conexion.close()