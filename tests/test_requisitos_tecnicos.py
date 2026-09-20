import sqlite3

import pytest

from app.database import (
    inicializar_base_datos,
    obtener_conexion,
)

from app.validators.validador_prestamo import (
    validar_identificador,
)


# RNF-008
def test_rechazar_identificadores_decimales():
    valores_invalidos = [
        1.5,
        1.0,
        "1.5",
        True,
        0,
        -1,
        "-2",
    ]

    for valor in valores_invalidos:
        with pytest.raises(
            ValueError
        ):
            validar_identificador(
                valor
            )

    assert (
        validar_identificador(1)
        == 1
    )

    assert (
        validar_identificador("25")
        == 25
    )


# RNF-009
def test_sqlite_rechaza_codigo_invalido(
    conexion,
):
    with pytest.raises(
        sqlite3.IntegrityError
    ):
        conexion.execute(
            """
            INSERT INTO equipos (
                nombre,
                codigo,
                descripcion,
                estado
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                "Equipo válido",
                "A-1",
                "Descripción válida",
                "DISPONIBLE",
            ),
        )


# RNF-009
def test_sqlite_rechaza_fecha_invalida(
    conexion,
    usuario_base,
    equipo_base,
):
    with pytest.raises(
        sqlite3.IntegrityError
    ):
        conexion.execute(
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
                usuario_base.id,
                equipo_base.id,
                "2026-02-30",
                "2026-03-05",
            ),
        )


# RNF-010
def test_inicializacion_carga_poblacion_base(
    tmp_path,
):
    ruta = (
        tmp_path
        / "poblacion.db"
    )

    inicializar_base_datos(
        ruta,
        cargar_poblacion=True,
    )

    conexion = obtener_conexion(
        ruta
    )

    try:
        usuarios = conexion.execute(
            """
            SELECT COUNT(*)
            FROM usuarios
            """
        ).fetchone()[0]

        equipos = conexion.execute(
            """
            SELECT COUNT(*)
            FROM equipos
            """
        ).fetchone()[0]

        prestamos = conexion.execute(
            """
            SELECT COUNT(*)
            FROM prestamos
            """
        ).fetchone()[0]

        assert usuarios == 100
        assert equipos == 50
        assert prestamos == 150

    finally:
        conexion.close()