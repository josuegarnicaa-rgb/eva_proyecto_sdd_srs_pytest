from app.models.equipo import Equipo


class RepositorioEquipo:
    def __init__(self, conexion):
        self.conexion = conexion

    def insertar(
        self,
        nombre,
        codigo,
        descripcion,
    ):
        cursor = self.conexion.execute(
            """
            INSERT INTO equipos (
                nombre,
                codigo,
                descripcion,
                estado
            )
            VALUES (
                ?,
                ?,
                ?,
                'DISPONIBLE'
            )
            """,
            (
                nombre,
                codigo,
                descripcion,
            ),
        )

        return cursor.lastrowid

    def obtener(self, equipo_id):
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

        return self._crear_modelo(
            fila
        )

    def listar(self):
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
            self._crear_modelo(fila)
            for fila in filas
        ]

    def codigo_existe(self, codigo):
        fila = self.conexion.execute(
            """
            SELECT 1
            FROM equipos
            WHERE codigo = ?
            """,
            (codigo,),
        ).fetchone()

        return fila is not None

    def cambiar_estado(
        self,
        equipo_id,
        estado,
    ):
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

        return cursor.rowcount

    @staticmethod
    def _crear_modelo(fila):
        return Equipo(
            id=fila["id"],
            nombre=fila["nombre"],
            codigo=fila["codigo"],
            descripcion=fila["descripcion"],
            estado=fila["estado"],
        )