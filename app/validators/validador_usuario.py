import re


PATRON_NOMBRE = re.compile(
    r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+$"
)

PATRON_CORREO = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)$"
)

DOMINIOS_PERMITIDOS = {
    "gmail.com",
    "hotmail.com",
    "outlook.com",
    "umss.edu.bo",
}


def _validar_texto_persona(valor, campo):
    if not isinstance(valor, str):
        raise ValueError(f"{campo} debe ser texto.")

    valor = valor.strip()

    if not 2 <= len(valor) <= 50:
        raise ValueError(
            f"{campo} debe tener entre 2 y 50 caracteres."
        )

    if not PATRON_NOMBRE.fullmatch(valor):
        raise ValueError(
            f"{campo} solo admite letras y espacios."
        )

    return " ".join(valor.split())


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
            "El correo debe tener como máximo 100 caracteres."
        )

    coincidencia = PATRON_CORREO.fullmatch(correo)

    if not coincidencia:
        raise ValueError(
            "El correo no tiene un formato válido."
        )

    dominio = coincidencia.group(1).lower()

    if dominio not in DOMINIOS_PERMITIDOS:
        raise ValueError(
            "El dominio del correo no está permitido."
        )

    return correo