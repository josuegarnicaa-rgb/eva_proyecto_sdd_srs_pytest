from datetime import date, datetime


FORMATO_FECHA = "%Y-%m-%d"


def validar_identificador(
    valor,
    campo="El identificador",
):
    if isinstance(valor, bool):
        raise ValueError(
            f"{campo} debe ser un entero positivo."
        )

    try:
        numero = int(valor)

    except (TypeError, ValueError) as error:
        raise ValueError(
            f"{campo} debe ser un entero positivo."
        ) from error

    if numero <= 0:
        raise ValueError(
            f"{campo} debe ser un entero positivo."
        )

    return numero


def validar_fecha(
    valor,
    campo="La fecha",
):
    if isinstance(valor, datetime):
        return valor.date()

    if isinstance(valor, date):
        return valor

    if not isinstance(valor, str):
        raise ValueError(
            f"{campo} no representa una fecha válida."
        )

    try:
        return datetime.strptime(
            valor.strip(),
            FORMATO_FECHA,
        ).date()

    except ValueError as error:
        raise ValueError(
            f"{campo} no representa una fecha válida. "
            "Use AAAA-MM-DD."
        ) from error


def validar_rango_fechas(
    fecha_prestamo,
    fecha_devolucion,
):
    inicio = validar_fecha(
        fecha_prestamo,
        "La fecha de préstamo",
    )

    fin = validar_fecha(
        fecha_devolucion,
        "La fecha de devolución",
    )

    if fin < inicio:
        raise ValueError(
            "La fecha de devolución no puede ser anterior al préstamo."
        )

    return inicio, fin