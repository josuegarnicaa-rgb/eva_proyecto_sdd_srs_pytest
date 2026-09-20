import re


PATRON_NOMBRE = re.compile(
    r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+$"
)

PATRON_PARTE_LOCAL = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+$"
)

DOMINIOS_PERMITIDOS = {
    "gmail.com",
    "hotmail.com",
    "outlook.com",
    "umss.edu.bo",
}


def _validar_texto_persona(
    valor,
    campo,
):
    if not isinstance(valor, str):
        raise ValueError(
            f"{campo} debe ser texto."
        )

    valor = " ".join(
        valor.strip().split()
    )

    if not 2 <= len(valor) <= 50:
        raise ValueError(
            f"{campo} debe tener "
            "entre 2 y 50 caracteres."
        )

    if not PATRON_NOMBRE.fullmatch(valor):
        raise ValueError(
            f"{campo} solo admite "
            "letras y espacios."
        )

    return valor


def validar_nombre(nombre):
    return _validar_texto_persona(
        nombre,
        "El nombre",
    )


def validar_apellido(apellido):
    return _validar_texto_persona(
        apellido,
        "El apellido",
    )


def validar_correo(correo):
    if not isinstance(correo, str):
        raise ValueError(
            "El correo debe ser texto."
        )

    correo = correo.strip().lower()

    if not correo or len(correo) > 100:
        raise ValueError(
            "El correo debe tener "
            "como máximo 100 caracteres."
        )

    if correo.count("@") != 1:
        raise ValueError(
            "El correo no tiene "
            "un formato válido."
        )

    parte_local, dominio = correo.split(
        "@"
    )

    if not parte_local or not dominio:
        raise ValueError(
            "El correo no tiene "
            "un formato válido."
        )

    if len(parte_local) > 64:
        raise ValueError(
            "El correo no tiene "
            "un formato válido."
        )

    if not PATRON_PARTE_LOCAL.fullmatch(
        parte_local
    ):
        raise ValueError(
            "El correo no tiene "
            "un formato válido."
        )

    if (
        parte_local.startswith(".")
        or parte_local.endswith(".")
        or ".." in parte_local
    ):
        raise ValueError(
            "El correo no tiene "
            "un formato válido."
        )

    if dominio not in DOMINIOS_PERMITIDOS:
        raise ValueError(
            "El dominio del correo "
            "no está permitido."
        )

    return correo