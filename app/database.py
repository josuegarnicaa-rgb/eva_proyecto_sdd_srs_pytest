import sqlite3
from pathlib import Path


RUTA_RAIZ = Path(__file__).resolve().parent.parent
RUTA_DATOS = RUTA_RAIZ / "data"
RUTA_BASE_DATOS = RUTA_DATOS / "prestamos.db"


def obtener_conexion(ruta_base_datos=RUTA_BASE_DATOS):
    """Abre una conexión SQLite con integridad referencial activa."""
    ruta = str(ruta_base_datos)

    if ruta != ":memory:":
        Path(ruta_base_datos).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    conexion = sqlite3.connect(ruta)
    conexion.row_factory = sqlite3.Row
    conexion.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conexion


def crear_tablas(conexion):
    """Crea las tablas y restricciones del sistema."""

    conexion.executescript(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre TEXT NOT NULL
                CHECK (nombre = trim(nombre))
                CHECK (
                    length(nombre)
                    BETWEEN 2 AND 50
                )
                CHECK (
                    nombre NOT GLOB '*[0-9]*'
                ),

            apellido TEXT NOT NULL
                CHECK (apellido = trim(apellido))
                CHECK (
                    length(apellido)
                    BETWEEN 2 AND 50
                )
                CHECK (
                    apellido NOT GLOB '*[0-9]*'
                ),

            correo TEXT NOT NULL UNIQUE
                CHECK (
                    correo = lower(trim(correo))
                )
                CHECK (
                    length(correo)
                    BETWEEN 3 AND 100
                )
                CHECK (
                    length(correo)
                    - length(
                        replace(
                            correo,
                            '@',
                            ''
                        )
                    ) = 1
                )
                CHECK (
                    correo NOT LIKE '.%'
                )
                CHECK (
                    correo NOT LIKE '%.@%'
                )
                CHECK (
                    correo NOT LIKE '%..%'
                )
                CHECK (
                    instr(correo, ' ') = 0
                )
                CHECK (
                    correo LIKE '%@gmail.com'
                    OR correo LIKE '%@hotmail.com'
                    OR correo LIKE '%@outlook.com'
                    OR correo LIKE '%@umss.edu.bo'
                )
        );


        CREATE TABLE IF NOT EXISTS equipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre TEXT NOT NULL
                CHECK (
                    nombre = trim(nombre)
                )
                CHECK (
                    length(nombre)
                    BETWEEN 2 AND 80
                ),

            codigo TEXT NOT NULL UNIQUE
                CHECK (
                    codigo = upper(trim(codigo))
                )
                CHECK (
                    length(codigo)
                    BETWEEN 3 AND 10
                )
                CHECK (
                    codigo
                    NOT GLOB '*[^A-Z0-9]*'
                ),

            descripcion TEXT NOT NULL
                CHECK (
                    descripcion = trim(descripcion)
                )
                CHECK (
                    length(descripcion)
                    BETWEEN 1 AND 250
                ),

            estado TEXT NOT NULL
                DEFAULT 'DISPONIBLE'
                CHECK (
                    estado IN (
                        'DISPONIBLE',
                        'PRESTADO'
                    )
                )
        );


        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            usuario_id INTEGER NOT NULL
                CHECK (
                    usuario_id > 0
                ),

            equipo_id INTEGER NOT NULL
                CHECK (
                    equipo_id > 0
                ),

            fecha_prestamo TEXT NOT NULL

                CHECK (
                    length(fecha_prestamo) = 10
                )

                CHECK (
                    fecha_prestamo GLOB
                    '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
                )

                CHECK (
                    CAST(
                        substr(
                            fecha_prestamo,
                            1,
                            4
                        )
                        AS INTEGER
                    )
                    BETWEEN 1 AND 9999
                )

                CHECK (
                    CAST(
                        substr(
                            fecha_prestamo,
                            6,
                            2
                        )
                        AS INTEGER
                    )
                    BETWEEN 1 AND 12
                )

                CHECK (
                    CAST(
                        substr(
                            fecha_prestamo,
                            9,
                            2
                        )
                        AS INTEGER
                    )
                    BETWEEN 1
                    AND
                    CAST(
                        strftime(
                            '%d',
                            date(
                                substr(
                                    fecha_prestamo,
                                    1,
                                    7
                                )
                                || '-01',
                                '+1 month',
                                '-1 day'
                            )
                        )
                        AS INTEGER
                    )
                ),


            fecha_devolucion TEXT NOT NULL

                CHECK (
                    length(fecha_devolucion)
                    = 10
                )

                CHECK (
                    fecha_devolucion GLOB
                    '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
                )

                CHECK (
                    CAST(
                        substr(
                            fecha_devolucion,
                            1,
                            4
                        )
                        AS INTEGER
                    )
                    BETWEEN 1 AND 9999
                )

                CHECK (
                    CAST(
                        substr(
                            fecha_devolucion,
                            6,
                            2
                        )
                        AS INTEGER
                    )
                    BETWEEN 1 AND 12
                )

                CHECK (
                    CAST(
                        substr(
                            fecha_devolucion,
                            9,
                            2
                        )
                        AS INTEGER
                    )
                    BETWEEN 1
                    AND
                    CAST(
                        strftime(
                            '%d',
                            date(
                                substr(
                                    fecha_devolucion,
                                    1,
                                    7
                                )
                                || '-01',
                                '+1 month',
                                '-1 day'
                            )
                        )
                        AS INTEGER
                    )
                ),


            estado TEXT NOT NULL
                DEFAULT 'ACTIVO'
                CHECK (
                    estado IN (
                        'ACTIVO',
                        'DEVUELTO',
                        'ATRASADO'
                    )
                ),

            CHECK (
                date(fecha_devolucion)
                >= date(fecha_prestamo)
            ),

            FOREIGN KEY (
                usuario_id
            )
            REFERENCES usuarios(id),

            FOREIGN KEY (
                equipo_id
            )
            REFERENCES equipos(id)
        );


        CREATE UNIQUE INDEX IF NOT EXISTS
        idx_prestamo_abierto_equipo
        ON prestamos(equipo_id)
        WHERE estado IN (
            'ACTIVO',
            'ATRASADO'
        );
        """
    )

    conexion.commit()


def inicializar_base_datos(
    ruta_base_datos=RUTA_BASE_DATOS,
    cargar_poblacion=True,
):
    """Crea la base y carga la población si está vacía."""

    conexion = obtener_conexion(
        ruta_base_datos
    )

    try:
        crear_tablas(
            conexion
        )

        if cargar_poblacion:
            from app.datos_iniciales import (
                cargar_poblacion_si_esta_vacia,
            )

            cargar_poblacion_si_esta_vacia(
                conexion
            )

    finally:
        conexion.close()