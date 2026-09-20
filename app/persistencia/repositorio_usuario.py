from app.models.usuario import Usuario


class RepositorioUsuario:
    def __init__(self, conexion):
        self.conexion = conexion

    def insertar(
        self,
        nombre,
        apellido,
        correo,
    ):
        cursor = self.conexion.execute(
            """
            INSERT INTO usuarios (
                nombre,
                apellido,
                correo
            )
            VALUES (?, ?, ?)
            """,
            (
                nombre,
                apellido,
                correo,
            ),
        )

        return cursor.lastrowid

    def obtener(self, usuario_id):
        fila = self.conexion.execute(
            """
            SELECT
                id,
                nombre,
                apellido,
                correo
            FROM usuarios
            WHERE id = ?
            """,
            (usuario_id,),
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
                apellido,
                correo
            FROM usuarios
            ORDER BY id
            """
        ).fetchall()

        return [
            self._crear_modelo(fila)
            for fila in filas
        ]

    def existe(self, usuario_id):
        fila = self.conexion.execute(
            """
            SELECT 1
            FROM usuarios
            WHERE id = ?
            """,
            (usuario_id,),
        ).fetchone()

        return fila is not None

    def correo_existe(self, correo):
        fila = self.conexion.execute(
            """
            SELECT 1
            FROM usuarios
            WHERE correo = ?
            """,
            (correo,),
        ).fetchone()

        return fila is not None

    @staticmethod
    def _crear_modelo(fila):
        return Usuario(
            id=fila["id"],
            nombre=fila["nombre"],
            apellido=fila["apellido"],
            correo=fila["correo"],
        )