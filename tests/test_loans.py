from datetime import (
    date,
    timedelta,
)

import pytest


# TEST-003.1
def test_crear_prestamo_valido(
    servicio_prestamo,
    usuario_base,
    equipo_base,
):
    hoy = date.today()

    prestamo = (
        servicio_prestamo
        .crear_prestamo(
            usuario_base.id,
            equipo_base.id,
            hoy,
            hoy + timedelta(days=7),
        )
    )

    assert prestamo.id > 0

    assert (
        prestamo.estado
        == "ACTIVO"
    )


# TEST-003.2
def test_rechazar_usuario_inexistente(
    servicio_prestamo,
    equipo_base,
):
    hoy = date.today()

    with pytest.raises(
        ValueError,
        match="usuario no existe",
    ):
        servicio_prestamo.crear_prestamo(
            9999,
            equipo_base.id,
            hoy,
            hoy + timedelta(days=7),
        )


# TEST-003.3
def test_rechazar_equipo_inexistente(
    servicio_prestamo,
    usuario_base,
):
    hoy = date.today()

    with pytest.raises(
        ValueError,
        match="equipo no existe",
    ):
        servicio_prestamo.crear_prestamo(
            usuario_base.id,
            9999,
            hoy,
            hoy + timedelta(days=7),
        )


# TEST-004.1
def test_permitir_prestamo_equipo_disponible(
    servicio_prestamo,
    servicio_equipo,
    usuario_base,
    equipo_base,
):
    hoy = date.today()

    assert (
        servicio_equipo
        .esta_disponible(
            equipo_base.id
        )
    )

    prestamo = (
        servicio_prestamo
        .crear_prestamo(
            usuario_base.id,
            equipo_base.id,
            hoy,
            hoy + timedelta(days=5),
        )
    )

    assert (
        prestamo.estado
        == "ACTIVO"
    )

    assert not (
        servicio_equipo
        .esta_disponible(
            equipo_base.id
        )
    )


# TEST-004.2
def test_rechazar_prestamo_equipo_ocupado(
    servicio_prestamo,
    servicio_usuario,
    usuario_base,
    equipo_base,
):
    hoy = date.today()

    servicio_prestamo.crear_prestamo(
        usuario_base.id,
        equipo_base.id,
        hoy,
        hoy + timedelta(days=5),
    )

    otro_usuario = (
        servicio_usuario
        .registrar_usuario(
            "Luis",
            "Vargas",
            "luis@gmail.com",
        )
    )

    with pytest.raises(
        ValueError,
        match="no está disponible",
    ):
        servicio_prestamo.crear_prestamo(
            otro_usuario.id,
            equipo_base.id,
            hoy,
            hoy + timedelta(days=3),
        )


# TEST-005.1
def test_registrar_devolucion_correctamente(
    servicio_prestamo,
    servicio_equipo,
    usuario_base,
    equipo_base,
):
    hoy = date.today()

    prestamo = (
        servicio_prestamo
        .crear_prestamo(
            usuario_base.id,
            equipo_base.id,
            hoy,
            hoy + timedelta(days=7),
        )
    )

    devuelto = (
        servicio_prestamo
        .registrar_devolucion(
            prestamo.id
        )
    )

    assert (
        devuelto.estado
        == "DEVUELTO"
    )

    assert (
        servicio_equipo
        .esta_disponible(
            equipo_base.id
        )
    )


# TEST-005.2
def test_rechazar_devolucion_prestamo_inexistente(
    servicio_prestamo,
):
    with pytest.raises(
        ValueError,
        match="préstamo no existe",
    ):
        servicio_prestamo.registrar_devolucion(
            9999
        )


# TEST-005.3
def test_rechazar_segunda_devolucion(
    servicio_prestamo,
    usuario_base,
    equipo_base,
):
    hoy = date.today()

    prestamo = (
        servicio_prestamo
        .crear_prestamo(
            usuario_base.id,
            equipo_base.id,
            hoy,
            hoy + timedelta(days=7),
        )
    )

    servicio_prestamo.registrar_devolucion(
        prestamo.id
    )

    with pytest.raises(
        ValueError,
        match="ya fue devuelto",
    ):
        servicio_prestamo.registrar_devolucion(
            prestamo.id
        )


# TEST-006.1
def test_aceptar_fechas_validas(
    servicio_prestamo,
    usuario_base,
    equipo_base,
):
    prestamo = (
        servicio_prestamo
        .crear_prestamo(
            usuario_base.id,
            equipo_base.id,
            "2026-09-20",
            "2026-09-25",
        )
    )

    assert (
        prestamo.fecha_prestamo
        == "2026-09-20"
    )

    assert (
        prestamo.fecha_devolucion
        == "2026-09-25"
    )


# TEST-006.2
def test_rechazar_fecha_devolucion_anterior(
    servicio_prestamo,
    usuario_base,
    equipo_base,
):
    with pytest.raises(
        ValueError
    ):
        servicio_prestamo.crear_prestamo(
            usuario_base.id,
            equipo_base.id,
            "2026-09-20",
            "2026-09-19",
        )


# TEST-006.3
def test_rechazar_fecha_invalida(
    servicio_prestamo,
    usuario_base,
    equipo_base,
):
    with pytest.raises(
        ValueError
    ):
        servicio_prestamo.crear_prestamo(
            usuario_base.id,
            equipo_base.id,
            "20-09-2026",
            "25-09-2026",
        )


# TEST-007.1
def test_consultar_prestamo_existente(
    servicio_prestamo,
    usuario_base,
    equipo_base,
):
    hoy = date.today()

    creado = (
        servicio_prestamo
        .crear_prestamo(
            usuario_base.id,
            equipo_base.id,
            hoy,
            hoy + timedelta(days=7),
        )
    )

    consultado = (
        servicio_prestamo
        .consultar_prestamo(
            creado.id
        )
    )

    assert (
        consultado
        == creado
    )


# TEST-007.2
def test_consultar_prestamo_inexistente(
    servicio_prestamo,
):
    assert (
        servicio_prestamo
        .consultar_prestamo(
            9999
        )
        is None
    )


# TEST-008.1
def test_detectar_prestamo_atrasado(
    servicio_prestamo,
    usuario_base,
    equipo_base,
):
    hoy = date.today()

    prestamo = (
        servicio_prestamo
        .crear_prestamo(
            usuario_base.id,
            equipo_base.id,
            hoy - timedelta(days=10),
            hoy - timedelta(days=2),
        )
    )

    atrasados = (
        servicio_prestamo
        .detectar_prestamos_atrasados(
            hoy
        )
    )

    assert any(
        item.id == prestamo.id
        for item in atrasados
    )

    assert (
        servicio_prestamo
        .consultar_prestamo(
            prestamo.id
        )
        .estado
        == "ATRASADO"
    )


# TEST-008.2
def test_no_marcar_prestamo_vigente_como_atrasado(
    servicio_prestamo,
    usuario_base,
    equipo_base,
):
    hoy = date.today()

    prestamo = (
        servicio_prestamo
        .crear_prestamo(
            usuario_base.id,
            equipo_base.id,
            hoy,
            hoy + timedelta(days=5),
        )
    )

    atrasados = (
        servicio_prestamo
        .detectar_prestamos_atrasados(
            hoy
        )
    )

    assert all(
        item.id != prestamo.id
        for item in atrasados
    )

    assert (
        servicio_prestamo
        .consultar_prestamo(
            prestamo.id
        )
        .estado
        == "ACTIVO"
    )


# TEST-008.3
def test_no_marcar_prestamo_devuelto_como_atrasado(
    servicio_prestamo,
    usuario_base,
    equipo_base,
):
    hoy = date.today()

    prestamo = (
        servicio_prestamo
        .crear_prestamo(
            usuario_base.id,
            equipo_base.id,
            hoy - timedelta(days=10),
            hoy - timedelta(days=2),
        )
    )

    servicio_prestamo.registrar_devolucion(
        prestamo.id
    )

    atrasados = (
        servicio_prestamo
        .detectar_prestamos_atrasados(
            hoy
        )
    )

    assert all(
        item.id != prestamo.id
        for item in atrasados
    )

    assert (
        servicio_prestamo
        .consultar_prestamo(
            prestamo.id
        )
        .estado
        == "DEVUELTO"
    )