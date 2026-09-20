from datetime import (
    date,
    timedelta,
)

from pathlib import Path

import sys


RAIZ = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

if str(RAIZ) not in sys.path:
    sys.path.insert(
        0,
        str(RAIZ),
    )


from app.database import (
    RUTA_BASE_DATOS,
    crear_tablas,
    obtener_conexion,
)

from app.services.servicio_equipo import (
    ServicioEquipo,
)

from app.services.servicio_prestamo import (
    ServicioPrestamo,
)

from app.services.servicio_usuario import (
    ServicioUsuario,
)


NOMBRES = [
    "Ana",
    "Luis",
    "María",
    "Carlos",
    "Sofía",
    "Diego",
    "Lucía",
    "Mateo",
    "Valeria",
    "Jorge",
    "Elena",
    "Marco",
    "Paola",
    "Bruno",
    "Camila",
    "Andrés",
    "Natalia",
    "Samuel",
    "Daniela",
    "Iván",
]


APELLIDOS = [
    "Rojas",
    "Mamani",
    "Quispe",
    "Flores",
    "Vargas",
    "Gómez",
    "López",
    "Fernández",
    "Torrez",
    "Rivera",
    "Condori",
    "Mendoza",
    "Salazar",
    "Paredes",
    "Castro",
    "Romero",
    "Arias",
    "Vega",
    "Cruz",
    "Sánchez",
]


TIPOS_EQUIPO = [
    "Microscopio",
    "Multímetro",
    "Osciloscopio",
    "Fuente DC",
    "Generador",
    "Protoboard",
    "Arduino",
    "ESP32",
    "Raspberry Pi",
    "Sensor",
]


def reiniciar_base_datos():
    if RUTA_BASE_DATOS.exists():
        RUTA_BASE_DATOS.unlink()

    conexion = obtener_conexion()

    crear_tablas(
        conexion
    )

    return conexion


def cargar_usuarios(
    servicio,
):
    dominios = [
        "gmail.com",
        "hotmail.com",
        "outlook.com",
        "umss.edu.bo",
    ]

    for indice in range(100):
        nombre = NOMBRES[
            indice % len(NOMBRES)
        ]

        apellido = APELLIDOS[
            (indice * 3)
            % len(APELLIDOS)
        ]

        correo = (
            f"usuario{indice + 1:03d}"
            f"@{dominios[indice % len(dominios)]}"
        )

        servicio.registrar_usuario(
            nombre,
            apellido,
            correo,
        )


def cargar_equipos(
    servicio,
):
    for indice in range(
        1,
        51,
    ):
        tipo = TIPOS_EQUIPO[
            (indice - 1)
            % len(TIPOS_EQUIPO)
        ]

        servicio.registrar_equipo(
            nombre=(
                f"{tipo} de laboratorio "
                f"{indice}"
            ),
            codigo=(
                f"EQ{indice:03d}"
            ),
            descripcion=(
                "Equipo de laboratorio "
                f"número {indice} "
                "para prácticas académicas."
            ),
        )


def cargar_prestamos(
    servicio,
):
    hoy = date.today()

    # Préstamos históricos.
    for indice in range(120):
        dias_atras = (
            220 - indice
        )

        inicio = (
            hoy
            - timedelta(
                days=dias_atras
            )
        )

        fin = (
            inicio
            + timedelta(days=7)
        )

        prestamo = (
            servicio.crear_prestamo(
                usuario_id=(
                    indice % 100
                ) + 1,
                equipo_id=(
                    indice % 20
                ) + 1,
                fecha_prestamo=inicio,
                fecha_devolucion=fin,
            )
        )

        servicio.registrar_devolucion(
            prestamo.id
        )

    # Préstamos activos.
    for indice in range(15):
        servicio.crear_prestamo(
            usuario_id=(
                (
                    indice + 20
                ) % 100
            ) + 1,
            equipo_id=indice + 1,
            fecha_prestamo=(
                hoy
                - timedelta(days=2)
            ),
            fecha_devolucion=(
                hoy
                + timedelta(
                    days=12 + indice
                )
            ),
        )

    # Préstamos vencidos.
    for indice in range(15):
        servicio.crear_prestamo(
            usuario_id=(
                (
                    indice + 50
                ) % 100
            ) + 1,
            equipo_id=indice + 16,
            fecha_prestamo=(
                hoy
                - timedelta(
                    days=20 + indice
                )
            ),
            fecha_devolucion=(
                hoy
                - timedelta(
                    days=5 + indice
                )
            ),
        )

    servicio.detectar_prestamos_atrasados(
        hoy
    )


def main():
    conexion = (
        reiniciar_base_datos()
    )

    try:
        usuarios = ServicioUsuario(
            conexion
        )

        equipos = ServicioEquipo(
            conexion
        )

        prestamos = ServicioPrestamo(
            conexion
        )

        cargar_usuarios(
            usuarios
        )

        cargar_equipos(
            equipos
        )

        cargar_prestamos(
            prestamos
        )

        total_usuarios = (
            conexion.execute(
                """
                SELECT COUNT(*)
                FROM usuarios
                """
            ).fetchone()[0]
        )

        total_equipos = (
            conexion.execute(
                """
                SELECT COUNT(*)
                FROM equipos
                """
            ).fetchone()[0]
        )

        total_prestamos = (
            conexion.execute(
                """
                SELECT COUNT(*)
                FROM prestamos
                """
            ).fetchone()[0]
        )

        estados = dict(
            conexion.execute(
                """
                SELECT
                    estado,
                    COUNT(*)
                FROM prestamos
                GROUP BY estado
                ORDER BY estado
                """
            ).fetchall()
        )

        print(
            "Población inicial cargada correctamente."
        )

        print(
            f"Usuarios: {total_usuarios}"
        )

        print(
            f"Equipos: {total_equipos}"
        )

        print(
            f"Préstamos: {total_prestamos}"
        )

        print(
            f"Estados: {estados}"
        )

    finally:
        conexion.close()


if __name__ == "__main__":
    main()