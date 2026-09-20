import sqlite3
from datetime import date

from app.persistencia.repositorio_equipo import (
    RepositorioEquipo,
)
from app.persistencia.repositorio_prestamo import (
    RepositorioPrestamo,
)
from app.persistencia.repositorio_usuario import (
    RepositorioUsuario,
)
from app.validators.validador_prestamo import (
    validar_fecha,
    validar_identificador,
    validar_rango_fechas,
)


class ServicioPrestamo:
    def __init__(self, conexion):
        self.conexion = conexion

        self.repositorio_usuario = (
            RepositorioUsuario(
                conexion
            )
        )

        self.repositorio_equipo = (
            RepositorioEquipo(
                conexion
            )
        )

        self.repositorio_prestamo = (
            RepositorioPrestamo(
                conexion
            )
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

        if not (
            self.repositorio_usuario
            .existe(usuario_id)
        ):
            raise ValueError(
                "El usuario no existe."
            )

        equipo = (
            self.repositorio_equipo
            .obtener(equipo_id)
        )

        if equipo is None:
            raise ValueError(
                "El equipo no existe."
            )

        prestamo_abierto = (
            self.repositorio_prestamo
            .tiene_prestamo_abierto(
                equipo_id
            )
        )

        if (
            equipo.estado != "DISPONIBLE"
            or prestamo_abierto
        ):
            raise ValueError(
                "El equipo no está disponible."
            )

        try:
            prestamo_id = (
                self.repositorio_prestamo
                .insertar(
                    usuario_id,
                    equipo_id,
                    inicio.isoformat(),
                    fin.isoformat(),
                )
            )

            self.repositorio_equipo.cambiar_estado(
                equipo_id,
                "PRESTADO",
            )

            self.conexion.commit()

        except sqlite3.IntegrityError as error:
            self.conexion.rollback()

            raise ValueError(
                "No se pudo crear "
                "el préstamo."
            ) from error

        except Exception:
            self.conexion.rollback()
            raise

        return self.consultar_prestamo(
            prestamo_id
        )

    def registrar_devolucion(
        self,
        prestamo_id,
    ):
        prestamo_id = validar_identificador(
            prestamo_id,
            "El identificador del préstamo",
        )

        self._actualizar_atrasados(
            date.today()
        )

        prestamo = (
            self.repositorio_prestamo
            .obtener(prestamo_id)
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
            self.repositorio_prestamo.cambiar_estado(
                prestamo_id,
                "DEVUELTO",
            )

            self.repositorio_equipo.cambiar_estado(
                prestamo.equipo_id,
                "DISPONIBLE",
            )

            self.conexion.commit()

        except Exception:
            self.conexion.rollback()
            raise

        return (
            self.repositorio_prestamo
            .obtener(prestamo_id)
        )

    def consultar_prestamo(
        self,
        prestamo_id,
    ):
        prestamo_id = validar_identificador(
            prestamo_id,
            "El identificador del préstamo",
        )

        self._actualizar_atrasados(
            date.today()
        )

        return (
            self.repositorio_prestamo
            .obtener(prestamo_id)
        )

    def listar_prestamos(self):
        self._actualizar_atrasados(
            date.today()
        )

        return (
            self.repositorio_prestamo
            .listar()
        )

    def detectar_prestamos_atrasados(
        self,
        fecha_actual=None,
    ):
        hoy = validar_fecha(
            fecha_actual or date.today(),
            "La fecha actual",
        )

        identificadores = (
            self._actualizar_atrasados(
                hoy
            )
        )

        return [
            self.repositorio_prestamo
            .obtener(prestamo_id)
            for prestamo_id
            in identificadores
        ]

    def _actualizar_atrasados(
        self,
        fecha_actual,
    ):
        hoy = validar_fecha(
            fecha_actual,
            "La fecha actual",
        )

        identificadores = (
            self.repositorio_prestamo
            .obtener_ids_atrasados(
                hoy.isoformat()
            )
        )

        if identificadores:
            self.repositorio_prestamo.marcar_atrasados(
                identificadores
            )

            self.conexion.commit()

        return identificadores