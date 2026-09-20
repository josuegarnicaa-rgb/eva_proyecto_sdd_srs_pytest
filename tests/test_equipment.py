import pytest


# TEST-002.1
def test_registrar_equipo_valido(
    servicio_equipo,
):
    equipo = (
        servicio_equipo
        .registrar_equipo(
            "Osciloscopio",
            "OSC001",
            (
                "Osciloscopio digital "
                "de laboratorio."
            ),
        )
    )

    assert equipo.id > 0

    assert (
        equipo.estado
        == "DISPONIBLE"
    )


# TEST-002.2
def test_rechazar_codigo_duplicado(
    servicio_equipo,
):
    servicio_equipo.registrar_equipo(
        "Osciloscopio",
        "OSC001",
        "Equipo uno",
    )

    with pytest.raises(
        ValueError
    ):
        servicio_equipo.registrar_equipo(
            "Multímetro",
            "OSC001",
            "Equipo dos",
        )


# TEST-002.3
def test_rechazar_codigo_con_simbolos(
    servicio_equipo,
):
    with pytest.raises(
        ValueError
    ):
        servicio_equipo.registrar_equipo(
            "Osciloscopio",
            "OSC-01",
            "Equipo de laboratorio",
        )


# TEST-002.4
def test_rechazar_datos_vacios(
    servicio_equipo,
):
    with pytest.raises(
        ValueError
    ):
        servicio_equipo.registrar_equipo(
            "",
            "",
            "",
        )


# TEST-002.5
def test_rechazar_datos_equipo_demasiado_largos(
    servicio_equipo,
):
    with pytest.raises(
        ValueError
    ):
        servicio_equipo.registrar_equipo(
            "E" * 81,
            "EQ001",
            "Equipo de laboratorio",
        )


# TEST-002.6
def test_rechazar_codigo_demasiado_corto(
    servicio_equipo,
):
    with pytest.raises(
        ValueError
    ):
        servicio_equipo.registrar_equipo(
            "Multímetro",
            "E1",
            "Equipo de laboratorio",
        )