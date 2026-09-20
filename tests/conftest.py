import pytest

from app.database import (
    crear_tablas,
    obtener_conexion,
)

from app.services.servicio_equipo import (
    ServicioEquipo,
)

from app.services.servicio_prestamo import (
    ServicioPrestamo,
)

from app.services.servicio_usuario import (
    ServicioUsuario,
)


@pytest.fixture
def conexion(
    tmp_path,
):
    ruta_temporal = (
        tmp_path / "pruebas.db"
    )

    conexion = obtener_conexion(
        ruta_temporal
    )

    crear_tablas(
        conexion
    )

    yield conexion

    conexion.close()


@pytest.fixture
def servicio_usuario(
    conexion,
):
    return ServicioUsuario(
        conexion
    )


@pytest.fixture
def servicio_equipo(
    conexion,
):
    return ServicioEquipo(
        conexion
    )


@pytest.fixture
def servicio_prestamo(
    conexion,
):
    return ServicioPrestamo(
        conexion
    )


@pytest.fixture
def usuario_base(
    servicio_usuario,
):
    return (
        servicio_usuario
        .registrar_usuario(
            "Ana",
            "Rojas",
            "ana.rojas@gmail.com",
        )
    )


@pytest.fixture
def equipo_base(
    servicio_equipo,
):
    return (
        servicio_equipo
        .registrar_equipo(
            "Microscopio óptico",
            "MIC001",
            (
                "Microscopio para "
                "prácticas de laboratorio."
            ),
        )
    )