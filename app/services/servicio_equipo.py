from app.models.equipo import Equipo

from app.validators.validador_equipo import (
    validar_codigo_equipo,
    validar_descripcion,
    validar_nombre_equipo,
)

from app.validators.validador_prestamo import (
    validar_identificador,
)


class ServicioEquipo:
    def __init__(self, conexion):
        self.conexion = conexion

    def registrar_equipo(
        self,
        nombre,
        codigo,
        descripcion,
    ):
        nombre = validar_nombre_equipo(nombre)
        codigo = validar_codigo_equipo(codigo)
        descripcion = validar_descripcion(descripcion)

        if self._codigo_existe(codigo):
            raise ValueError(
                "El código del equipo ya está registrado."
            )

        cursor = self.conexion.execute(
            """
            INSERT INTO equipos (
                nombre,
                codigo,
                descripcion,
                estado
            )
            VALUES (?, ?, ?, 'DISPONIBLE')
            """,
            (
                nombre,
                codigo,
                descripcion,
            ),
        )

        self.conexion.commit()

        return self.obtener_equipo(
            cursor.lastrowid
        )

    def obtener_equipo(
        self,
        equipo_id,
    ):
        equipo_id = validar_identificador(
            equipo_id,
            "El identificador del equipo",
        )

        fila = self.conexion.execute(
            """
            SELECT
                id,
                nombre,
                codigo,
                descripcion,
                estado
            FROM equipos
            WHERE id = ?
            """,
            (equipo_id,),
        ).fetchone()

        if fila is None:
            return None

        return self._crear_equipo(fila)

    def listar_equipos(self):
        filas = self.conexion.execute(
            """
            SELECT
                id,
                nombre,
                codigo,
                descripcion,
                estado
            FROM equipos
            ORDER BY id
            """
        ).fetchall()

        return [
            self._crear_equipo(fila)
            for fila in filas
        ]

    def esta_disponible(
        self,
        equipo_id,
    ):
        equipo = self.obtener_equipo(
            equipo_id
        )

        return bool(
            equipo
            and equipo.estado == "DISPONIBLE"
        )

    def cambiar_estado(
        self,
        equipo_id,
        estado,
    ):
        if estado not in {
            "DISPONIBLE",
            "PRESTADO",
        }:
            raise ValueError(
                "Estado de equipo no permitido."
            )

        equipo_id = validar_identificador(
            equipo_id,
            "El identificador del equipo",
        )

        cursor = self.conexion.execute(
            """
            UPDATE equipos
            SET estado = ?
            WHERE id = ?
            """,
            (
                estado,
                equipo_id,
            ),
        )

        if cursor.rowcount == 0:
            raise ValueError(
                "El equipo no existe."
            )

    def _codigo_existe(
        self,
        codigo,
    ):
        fila = self.conexion.execute(
            """
            SELECT 1
            FROM equipos
            WHERE codigo = ?
            """,
            (codigo,),
        ).fetchone()

        return fila is not None

    @staticmethod
    def _crear_equipo(fila):
        return Equipo(
            id=fila["id"],
            nombre=fila["nombre"],
            codigo=fila["codigo"],
            descripcion=fila["descripcion"],
            estado=fila["estado"],
        )