from app.database import (
    inicializar_base_datos,
)

from app.ui.interfaz_principal import (
    InterfazPrincipal,
)


def main():
    inicializar_base_datos()

    aplicacion = InterfazPrincipal()

    aplicacion.mainloop()


if __name__ == "__main__":
    main()