from app.models.prestamo import Prestamo


class RepositorioPrestamo:
    def __init__(self, conexion):
        self.conexion = conexion

    def insertar(
        self,
        usuario_id,
        equipo_id,
        fecha_prestamo,
        fecha_devolucion,
    ):
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
                fecha_prestamo,
                fecha_devolucion,
            ),
        )

        return cursor.lastrowid

    def obtener(self, prestamo_id):
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

        return self._crear_modelo(
            fila
        )

    def listar(self):
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
            self._crear_modelo(fila)
            for fila in filas
        ]

    def tiene_prestamo_abierto(
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

    def cambiar_estado(
        self,
        prestamo_id,
        estado,
    ):
        cursor = self.conexion.execute(
            """
            UPDATE prestamos
            SET estado = ?
            WHERE id = ?
            """,
            (
                estado,
                prestamo_id,
            ),
        )

        return cursor.rowcount

    def obtener_ids_atrasados(
        self,
        fecha_actual,
    ):
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
            (fecha_actual,),
        ).fetchall()

        return [
            fila["id"]
            for fila in filas
        ]

    def marcar_atrasados(
        self,
        identificadores,
    ):
        if not identificadores:
            return

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

    @staticmethod
    def _crear_modelo(fila):
        return Prestamo(
            id=fila["id"],
            usuario_id=fila["usuario_id"],
            equipo_id=fila["equipo_id"],
            fecha_prestamo=(
                fila["fecha_prestamo"]
            ),
            fecha_devolucion=(
                fila["fecha_devolucion"]
            ),
            estado=fila["estado"],
        )