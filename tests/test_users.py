import pytest


# TEST-001.1
def test_registrar_usuario_valido(
    servicio_usuario,
):
    usuario = (
        servicio_usuario
        .registrar_usuario(
            "María",
            "López",
            "maria.lopez@gmail.com",
        )
    )

    assert usuario.id > 0

    assert (
        usuario.correo
        == "maria.lopez@gmail.com"
    )


# TEST-001.2
def test_rechazar_nombre_vacio(
    servicio_usuario,
):
    with pytest.raises(
        ValueError
    ):
        servicio_usuario.registrar_usuario(
            "",
            "López",
            "maria.lopez@gmail.com",
        )


# TEST-001.3
def test_rechazar_nombre_con_numeros(
    servicio_usuario,
):
    with pytest.raises(
        ValueError
    ):
        servicio_usuario.registrar_usuario(
            "María2",
            "López",
            "maria.lopez@gmail.com",
        )


# TEST-001.4
def test_rechazar_correo_invalido(
    servicio_usuario,
):
    correos_invalidos = [
        "correo-invalido",
        ".maria@gmail.com",
        "maria.@gmail.com",
        "ma..ria@gmail.com",
    ]

    for correo in correos_invalidos:
        with pytest.raises(
            ValueError
        ):
            servicio_usuario.registrar_usuario(
                "María",
                "López",
                correo,
            )


# TEST-001.5
def test_rechazar_dominio_no_permitido(
    servicio_usuario,
):
    with pytest.raises(
        ValueError
    ):
        servicio_usuario.registrar_usuario(
            "María",
            "López",
            "maria@empresa.com",
        )


# TEST-001.6
def test_rechazar_correo_duplicado(
    servicio_usuario,
):
    servicio_usuario.registrar_usuario(
        "María",
        "López",
        "maria.lopez@gmail.com",
    )

    with pytest.raises(
        ValueError
    ):
        servicio_usuario.registrar_usuario(
            "Lucía",
            "Rojas",
            "maria.lopez@gmail.com",
        )


# TEST-001.7
def test_rechazar_datos_usuario_demasiado_largos(
    servicio_usuario,
):
    with pytest.raises(
        ValueError
    ):
        servicio_usuario.registrar_usuario(
            "A" * 51,
            "López",
            "maria.lopez@gmail.com",
        )


# TEST-001.8
def test_rechazar_nombre_demasiado_corto(
    servicio_usuario,
):
    with pytest.raises(
        ValueError
    ):
        servicio_usuario.registrar_usuario(
            "M",
            "López",
            "maria.lopez@gmail.com",
        )


# TEST-001.9
def test_rechazar_apellido_con_simbolos(
    servicio_usuario,
):
    with pytest.raises(
        ValueError
    ):
        servicio_usuario.registrar_usuario(
            "María",
            "López!",
            "maria.lopez@gmail.com",
        )