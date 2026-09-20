from pathlib import Path
import sys


RAIZ = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

if str(RAIZ) not in sys.path:
    sys.path.insert(
        0,
        str(RAIZ),
    )


from app.database import (
    RUTA_BASE_DATOS,
    crear_tablas,
    obtener_conexion,
)

from app.datos_iniciales import (
    cargar_poblacion_inicial,
    obtener_resumen_poblacion,
)


def reiniciar_base_datos():
    if RUTA_BASE_DATOS.exists():
        RUTA_BASE_DATOS.unlink()

    conexion = obtener_conexion(
        RUTA_BASE_DATOS
    )

    crear_tablas(
        conexion
    )

    return conexion


def main():
    conexion = reiniciar_base_datos()

    try:
        cargar_poblacion_inicial(
            conexion
        )

        resumen = (
            obtener_resumen_poblacion(
                conexion
            )
        )

        print(
            "Población inicial "
            "cargada correctamente."
        )

        print(
            f"Usuarios: "
            f"{resumen['usuarios']}"
        )

        print(
            f"Equipos: "
            f"{resumen['equipos']}"
        )

        print(
            f"Préstamos: "
            f"{resumen['prestamos']}"
        )

        print(
            f"Estados: "
            f"{resumen['estados']}"
        )

    finally:
        conexion.close()


if __name__ == "__main__":
    main()