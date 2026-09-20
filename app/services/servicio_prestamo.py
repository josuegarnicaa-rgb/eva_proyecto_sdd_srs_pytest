from datetime import date

from app.models.prestamo import Prestamo

from app.services.servicio_equipo import (
    ServicioEquipo,
)

from app.validators.validador_prestamo import (
    validar_fecha,
    validar_identificador,
    validar_rango_fechas,
)


class ServicioPrestamo:
    def __init__(
        self,
        conexion,
    ):
        self.conexion = conexion

        self.servicio_equipo = ServicioEquipo(
            conexion
        )

    def crear_prestamo(
        self,
        usuario_id,
        equipo_id,
        fecha_prestamo,
        fecha_devolucion,
    ):
        usuario_id = validar_identificador(
            usuario_id,
            "El identificador del usuario",
        )

        equipo_id = validar_identificador(
            equipo_id,
            "El identificador del equipo",
        )

        inicio, fin = validar_rango_fechas(
            fecha_prestamo,
            fecha_devolucion,
        )

        if not self._usuario_existe(
            usuario_id
        ):
            raise ValueError(
                "El usuario no existe."
            )

        equipo = (
            self.servicio_equipo
            .obtener_equipo(equipo_id)
        )

        if equipo is None:
            raise ValueError(
                "El equipo no existe."
            )

        if (
            equipo.estado != "DISPONIBLE"
            or self._tiene_prestamo_abierto(
                equipo_id
            )
        ):
            raise ValueError(
                "El equipo no está disponible."
            )

        try:
            cursor = self.conexion.execute(
                """
                INSERT INTO prestamos (
                    usuario_id,
                    equipo_id,
                    fecha_prestamo,
                    fecha_devolucion,
                    estado
                )
                VALUES (
                    ?,
                    ?,
                    ?,
                    ?,
                    'ACTIVO'
                )
                """,
                (
                    usuario_id,
                    equipo_id,
                    inicio.isoformat(),
                    fin.isoformat(),
                ),
            )

            self.servicio_equipo.cambiar_estado(
                equipo_id,
                "PRESTADO",
            )

            self.conexion.commit()

        except Exception:
            self.conexion.rollback()
            raise

        return self.consultar_prestamo(
            cursor.lastrowid
        )

    def registrar_devolucion(
        self,
        prestamo_id,
    ):
        prestamo_id = validar_identificador(
            prestamo_id,
            "El identificador del préstamo",
        )

        prestamo = self.consultar_prestamo(
            prestamo_id
        )

        if prestamo is None:
            raise ValueError(
                "El préstamo no existe."
            )

        if prestamo.estado == "DEVUELTO":
            raise ValueError(
                "El préstamo ya fue devuelto."
            )

        try:
            self.conexion.execute(
                """
                UPDATE prestamos
                SET estado = 'DEVUELTO'
                WHERE id = ?
                """,
                (prestamo_id,),
            )

            self.servicio_equipo.cambiar_estado(
                prestamo.equipo_id,
                "DISPONIBLE",
            )

            self.conexion.commit()

        except Exception:
            self.conexion.rollback()
            raise

        return self.consultar_prestamo(
            prestamo_id
        )

    def consultar_prestamo(
        self,
        prestamo_id,
    ):
        prestamo_id = validar_identificador(
            prestamo_id,
            "El identificador del préstamo",
        )

        fila = self.conexion.execute(
            """
            SELECT
                id,
                usuario_id,
                equipo_id,
                fecha_prestamo,
                fecha_devolucion,
                estado
            FROM prestamos
            WHERE id = ?
            """,
            (prestamo_id,),
        ).fetchone()

        if fila is None:
            return None

        return self._crear_prestamo(
            fila
        )

    def listar_prestamos(self):
        filas = self.conexion.execute(
            """
            SELECT
                id,
                usuario_id,
                equipo_id,
                fecha_prestamo,
                fecha_devolucion,
                estado
            FROM prestamos
            ORDER BY id DESC
            """
        ).fetchall()

        return [
            self._crear_prestamo(fila)
            for fila in filas
        ]

    def detectar_prestamos_atrasados(
        self,
        fecha_actual=None,
    ):
        hoy = validar_fecha(
            fecha_actual or date.today(),
            "La fecha actual",
        )

        filas = self.conexion.execute(
            """
            SELECT id
            FROM prestamos
            WHERE estado IN (
                'ACTIVO',
                'ATRASADO'
            )
            AND date(fecha_devolucion)
                < date(?)
            ORDER BY id
            """,
            (hoy.isoformat(),),
        ).fetchall()

        identificadores = [
            fila["id"]
            for fila in filas
        ]

        if identificadores:
            self.conexion.executemany(
                """
                UPDATE prestamos
                SET estado = 'ATRASADO'
                WHERE id = ?
                AND estado = 'ACTIVO'
                """,
                [
                    (prestamo_id,)
                    for prestamo_id
                    in identificadores
                ],
            )

            self.conexion.commit()

        return [
            self.consultar_prestamo(
                prestamo_id
            )
            for prestamo_id
            in identificadores
        ]

    def _usuario_existe(
        self,
        usuario_id,
    ):
        fila = self.conexion.execute(
            """
            SELECT 1
            FROM usuarios
            WHERE id = ?
            """,
            (usuario_id,),
        ).fetchone()

        return fila is not None

    def _tiene_prestamo_abierto(
        self,
        equipo_id,
    ):
        fila = self.conexion.execute(
            """
            SELECT 1
            FROM prestamos
            WHERE equipo_id = ?
            AND estado IN (
                'ACTIVO',
                'ATRASADO'
            )
            """,
            (equipo_id,),
        ).fetchone()

        return fila is not None

    @staticmethod
    def _crear_prestamo(fila):
        return Prestamo(
            id=fila["id"],
            usuario_id=fila["usuario_id"],
            equipo_id=fila["equipo_id"],
            fecha_prestamo=fila["fecha_prestamo"],
            fecha_devolucion=fila["fecha_devolucion"],
            estado=fila["estado"],
        )