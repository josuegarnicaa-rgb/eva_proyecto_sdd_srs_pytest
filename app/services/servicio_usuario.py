from app.models.usuario import Usuario

from app.validators.validador_usuario import (
    validar_apellido,
    validar_correo,
    validar_nombre,
)


class ServicioUsuario:
    def __init__(self, conexion):
        self.conexion = conexion

    def registrar_usuario(
        self,
        nombre,
        apellido,
        correo,
    ):
        nombre = validar_nombre(nombre)
        apellido = validar_apellido(apellido)
        correo = validar_correo(correo)

        if self._correo_existe(correo):
            raise ValueError(
                "El correo ya está registrado."
            )

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

        self.conexion.commit()

        return self.obtener_usuario(
            cursor.lastrowid
        )

    def obtener_usuario(
        self,
        usuario_id,
    ):
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

        return self._crear_usuario(fila)

    def listar_usuarios(self):
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
            self._crear_usuario(fila)
            for fila in filas
        ]

    def _correo_existe(
        self,
        correo,
    ):
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
    def _crear_usuario(fila):
        return Usuario(
            id=fila["id"],
            nombre=fila["nombre"],
            apellido=fila["apellido"],
            correo=fila["correo"],
        )