import sqlite3

from app.persistencia.repositorio_equipo import (
    RepositorioEquipo,
)
from app.validators.validador_equipo import (
    validar_codigo_equipo,
    validar_descripcion,
    validar_nombre_equipo,
)
from app.validators.validador_prestamo import (
    validar_identificador,
)


class ServicioEquipo:
    ESTADOS_PERMITIDOS = {
        "DISPONIBLE",
        "PRESTADO",
    }

    def __init__(self, conexion):
        self.conexion = conexion

        self.repositorio = (
            RepositorioEquipo(
                conexion
            )
        )

    def registrar_equipo(
        self,
        nombre,
        codigo,
        descripcion,
    ):
        nombre = validar_nombre_equipo(
            nombre
        )

        codigo = validar_codigo_equipo(
            codigo
        )

        descripcion = validar_descripcion(
            descripcion
        )

        if self.repositorio.codigo_existe(
            codigo
        ):
            raise ValueError(
                "El código del equipo "
                "ya está registrado."
            )

        try:
            equipo_id = (
                self.repositorio.insertar(
                    nombre,
                    codigo,
                    descripcion,
                )
            )

            self.conexion.commit()

        except sqlite3.IntegrityError as error:
            self.conexion.rollback()

            raise ValueError(
                "No se pudo registrar "
                "el equipo."
            ) from error

        return self.repositorio.obtener(
            equipo_id
        )

    def obtener_equipo(
        self,
        equipo_id,
    ):
        equipo_id = validar_identificador(
            equipo_id,
            "El identificador del equipo",
        )

        return self.repositorio.obtener(
            equipo_id
        )

    def listar_equipos(self):
        return self.repositorio.listar()

    def esta_disponible(
        self,
        equipo_id,
    ):
        equipo = self.obtener_equipo(
            equipo_id
        )

        return bool(
            equipo
            and equipo.estado
            == "DISPONIBLE"
        )

    def cambiar_estado(
        self,
        equipo_id,
        estado,
    ):
        equipo_id = validar_identificador(
            equipo_id,
            "El identificador del equipo",
        )

        if estado not in (
            self.ESTADOS_PERMITIDOS
        ):
            raise ValueError(
                "Estado de equipo "
                "no permitido."
            )

        filas = (
            self.repositorio
            .cambiar_estado(
                equipo_id,
                estado,
            )
        )

        if filas == 0:
            raise ValueError(
                "El equipo no existe."
            )

        self.conexion.commit()

        return self.repositorio.obtener(
            equipo_id
        )