import re


PATRON_CODIGO = re.compile(
    r"^[A-Z0-9]{3,10}$"
)


def validar_nombre_equipo(nombre):
    if not isinstance(nombre, str):
        raise ValueError(
            "El nombre del equipo debe ser texto."
        )

    nombre = nombre.strip()

    if not 2 <= len(nombre) <= 80:
        raise ValueError(
            "El nombre del equipo debe tener entre 2 y 80 caracteres."
        )

    return " ".join(nombre.split())


def validar_codigo_equipo(codigo):
    if not isinstance(codigo, str):
        raise ValueError(
            "El código debe ser texto."
        )

    codigo = codigo.strip()

    if not PATRON_CODIGO.fullmatch(codigo):
        raise ValueError(
            "El código debe tener de 3 a 10 letras mayúsculas o números."
        )

    return codigo


def validar_descripcion(descripcion):
    if not isinstance(descripcion, str):
        raise ValueError(
            "La descripción debe ser texto."
        )

    descripcion = descripcion.strip()

    if not 1 <= len(descripcion) <= 250:
        raise ValueError(
            "La descripción debe tener entre 1 y 250 caracteres."
        )

    return descripcion