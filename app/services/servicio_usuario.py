import sqlite3

from app.persistencia.repositorio_usuario import (
    RepositorioUsuario,
)
from app.validators.validador_prestamo import (
    validar_identificador,
)
from app.validators.validador_usuario import (
    validar_apellido,
    validar_correo,
    validar_nombre,
)


class ServicioUsuario:
    def __init__(self, conexion):
        self.conexion = conexion

        self.repositorio = (
            RepositorioUsuario(
                conexion
            )
        )

    def registrar_usuario(
        self,
        nombre,
        apellido,
        correo,
    ):
        nombre = validar_nombre(
            nombre
        )

        apellido = validar_apellido(
            apellido
        )

        correo = validar_correo(
            correo
        )

        if self.repositorio.correo_existe(
            correo
        ):
            raise ValueError(
                "El correo ya está registrado."
            )

        try:
            usuario_id = (
                self.repositorio.insertar(
                    nombre,
                    apellido,
                    correo,
                )
            )

            self.conexion.commit()

        except sqlite3.IntegrityError as error:
            self.conexion.rollback()

            raise ValueError(
                "No se pudo registrar "
                "el usuario."
            ) from error

        return self.repositorio.obtener(
            usuario_id
        )

    def obtener_usuario(
        self,
        usuario_id,
    ):
        usuario_id = validar_identificador(
            usuario_id,
            "El identificador del usuario",
        )

        return self.repositorio.obtener(
            usuario_id
        )

    def listar_usuarios(self):
        return self.repositorio.listar()