from datetime import date, timedelta

from app.services.servicio_equipo import ServicioEquipo
from app.services.servicio_prestamo import ServicioPrestamo
from app.services.servicio_usuario import ServicioUsuario


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

DOMINIOS = [
    "gmail.com",
    "hotmail.com",
    "outlook.com",
    "umss.edu.bo",
]


def base_datos_vacia(conexion):
    tablas = (
        "usuarios",
        "equipos",
        "prestamos",
    )

    for tabla in tablas:
        cantidad = conexion.execute(
            f"SELECT COUNT(*) FROM {tabla}"
        ).fetchone()[0]

        if cantidad != 0:
            return False

    return True


def cargar_poblacion_si_esta_vacia(conexion):
    if not base_datos_vacia(conexion):
        return False

    cargar_poblacion_inicial(conexion)
    return True


def cargar_poblacion_inicial(conexion):
    servicio_usuario = ServicioUsuario(
        conexion
    )

    servicio_equipo = ServicioEquipo(
        conexion
    )

    servicio_prestamo = ServicioPrestamo(
        conexion
    )

    _cargar_usuarios(
        servicio_usuario
    )

    _cargar_equipos(
        servicio_equipo
    )

    _cargar_prestamos(
        servicio_prestamo
    )


def obtener_resumen_poblacion(conexion):
    total_usuarios = conexion.execute(
        "SELECT COUNT(*) FROM usuarios"
    ).fetchone()[0]

    total_equipos = conexion.execute(
        "SELECT COUNT(*) FROM equipos"
    ).fetchone()[0]

    total_prestamos = conexion.execute(
        "SELECT COUNT(*) FROM prestamos"
    ).fetchone()[0]

    estados = dict(
        conexion.execute(
            """
            SELECT estado, COUNT(*)
            FROM prestamos
            GROUP BY estado
            ORDER BY estado
            """
        ).fetchall()
    )

    return {
        "usuarios": total_usuarios,
        "equipos": total_equipos,
        "prestamos": total_prestamos,
        "estados": estados,
    }


def _cargar_usuarios(servicio):
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
            f"@{DOMINIOS[indice % len(DOMINIOS)]}"
        )

        servicio.registrar_usuario(
            nombre,
            apellido,
            correo,
        )


def _cargar_equipos(servicio):
    for indice in range(1, 51):
        tipo = TIPOS_EQUIPO[
            (indice - 1)
            % len(TIPOS_EQUIPO)
        ]

        servicio.registrar_equipo(
            nombre=(
                f"{tipo} de laboratorio "
                f"{indice}"
            ),
            codigo=f"EQ{indice:03d}",
            descripcion=(
                "Equipo de laboratorio "
                f"número {indice} "
                "para prácticas académicas."
            ),
        )


def _cargar_prestamos(servicio):
    hoy = date.today()

    # Históricos devueltos.
    for indice in range(120):
        inicio = hoy - timedelta(
            days=220 - indice
        )

        fin = inicio + timedelta(
            days=7
        )

        prestamo = servicio.crear_prestamo(
            usuario_id=(
                indice % 100
            ) + 1,
            equipo_id=(
                indice % 20
            ) + 1,
            fecha_prestamo=inicio,
            fecha_devolucion=fin,
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

    # Préstamos atrasados.
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