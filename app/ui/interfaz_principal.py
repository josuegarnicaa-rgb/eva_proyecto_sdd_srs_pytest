import tkinter as tk

from datetime import (
    date,
    timedelta,
)

from tkinter import (
    messagebox,
    ttk,
)

from app.database import (
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


class InterfazPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(
            "Gestión de préstamos de laboratorio"
        )

        self.geometry(
            "1100x700"
        )

        self.minsize(
            980,
            620,
        )

        self.conexion = obtener_conexion()

        self.usuarios = ServicioUsuario(
            self.conexion
        )

        self.equipos = ServicioEquipo(
            self.conexion
        )

        self.prestamos = ServicioPrestamo(
            self.conexion
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self._cerrar,
        )

        self._crear_interfaz()
        self._actualizar_todo()

    def _crear_interfaz(self):
        contenedor = ttk.Frame(
            self,
            padding=12,
        )

        contenedor.pack(
            fill="both",
            expand=True,
        )

        self.pestanas = ttk.Notebook(
            contenedor
        )

        self.pestanas.pack(
            fill="both",
            expand=True,
        )

        self.tab_usuarios = ttk.Frame(
            self.pestanas,
            padding=12,
        )

        self.tab_equipos = ttk.Frame(
            self.pestanas,
            padding=12,
        )

        self.tab_prestamos = ttk.Frame(
            self.pestanas,
            padding=12,
        )

        self.tab_consultas = ttk.Frame(
            self.pestanas,
            padding=12,
        )

        self.pestanas.add(
            self.tab_usuarios,
            text="Usuarios",
        )

        self.pestanas.add(
            self.tab_equipos,
            text="Equipos",
        )

        self.pestanas.add(
            self.tab_prestamos,
            text="Préstamos",
        )

        self.pestanas.add(
            self.tab_consultas,
            text="Consultas",
        )

        self._crear_tab_usuarios()
        self._crear_tab_equipos()
        self._crear_tab_prestamos()
        self._crear_tab_consultas()

    def _crear_tab_usuarios(self):
        formulario = ttk.LabelFrame(
            self.tab_usuarios,
            text="Registrar usuario",
            padding=10,
        )

        formulario.pack(
            fill="x"
        )

        ttk.Label(
            formulario,
            text="Nombre",
        ).grid(
            row=0,
            column=0,
            sticky="w",
        )

        ttk.Label(
            formulario,
            text="Apellido",
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=(10, 0),
        )

        ttk.Label(
            formulario,
            text="Correo",
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=(10, 0),
        )

        self.ent_nombre_usuario = ttk.Entry(
            formulario,
            width=24,
        )

        self.ent_apellido_usuario = ttk.Entry(
            formulario,
            width=24,
        )

        self.ent_correo_usuario = ttk.Entry(
            formulario,
            width=34,
        )

        self.ent_nombre_usuario.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        self.ent_apellido_usuario.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(10, 0),
        )

        self.ent_correo_usuario.grid(
            row=1,
            column=2,
            sticky="ew",
            padx=(10, 0),
        )

        ttk.Button(
            formulario,
            text="Registrar",
            command=self._registrar_usuario,
        ).grid(
            row=1,
            column=3,
            padx=(10, 0),
        )

        for columna in range(3):
            formulario.columnconfigure(
                columna,
                weight=1,
            )

        self.tabla_usuarios = (
            self._crear_tabla(
                self.tab_usuarios,
                (
                    "id",
                    "nombre",
                    "apellido",
                    "correo",
                ),
                (
                    "ID",
                    "Nombre",
                    "Apellido",
                    "Correo",
                ),
            )
        )

    def _crear_tab_equipos(self):
        formulario = ttk.LabelFrame(
            self.tab_equipos,
            text="Registrar equipo",
            padding=10,
        )

        formulario.pack(
            fill="x"
        )

        ttk.Label(
            formulario,
            text="Nombre",
        ).grid(
            row=0,
            column=0,
            sticky="w",
        )

        ttk.Label(
            formulario,
            text="Código",
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=(10, 0),
        )

        ttk.Label(
            formulario,
            text="Descripción",
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=(10, 0),
        )

        self.ent_nombre_equipo = ttk.Entry(
            formulario,
            width=24,
        )

        self.ent_codigo_equipo = ttk.Entry(
            formulario,
            width=16,
        )

        self.ent_descripcion_equipo = ttk.Entry(
            formulario,
            width=45,
        )

        self.ent_nombre_equipo.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        self.ent_codigo_equipo.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(10, 0),
        )

        self.ent_descripcion_equipo.grid(
            row=1,
            column=2,
            sticky="ew",
            padx=(10, 0),
        )

        ttk.Button(
            formulario,
            text="Registrar",
            command=self._registrar_equipo,
        ).grid(
            row=1,
            column=3,
            padx=(10, 0),
        )

        for columna in range(3):
            formulario.columnconfigure(
                columna,
                weight=1,
            )

        self.tabla_equipos = (
            self._crear_tabla(
                self.tab_equipos,
                (
                    "id",
                    "nombre",
                    "codigo",
                    "descripcion",
                    "estado",
                ),
                (
                    "ID",
                    "Nombre",
                    "Código",
                    "Descripción",
                    "Estado",
                ),
            )
        )

    def _crear_tab_prestamos(self):
        formulario = ttk.LabelFrame(
            self.tab_prestamos,
            text="Crear préstamo",
            padding=10,
        )

        formulario.pack(
            fill="x"
        )

        etiquetas = (
            "ID usuario",
            "ID equipo",
            "Fecha préstamo",
            "Fecha devolución",
        )

        for indice, texto in enumerate(
            etiquetas
        ):
            ttk.Label(
                formulario,
                text=texto,
            ).grid(
                row=0,
                column=indice,
                sticky="w",
                padx=(
                    10 if indice else 0,
                    0,
                ),
            )

        self.ent_usuario_id = ttk.Entry(
            formulario,
            width=12,
        )

        self.ent_equipo_id = ttk.Entry(
            formulario,
            width=12,
        )

        self.ent_fecha_prestamo = ttk.Entry(
            formulario,
            width=16,
        )

        self.ent_fecha_devolucion = ttk.Entry(
            formulario,
            width=16,
        )

        hoy = date.today()

        self.ent_fecha_prestamo.insert(
            0,
            hoy.isoformat(),
        )

        self.ent_fecha_devolucion.insert(
            0,
            (
                hoy
                + timedelta(days=7)
            ).isoformat(),
        )

        entradas = (
            self.ent_usuario_id,
            self.ent_equipo_id,
            self.ent_fecha_prestamo,
            self.ent_fecha_devolucion,
        )

        for indice, entrada in enumerate(
            entradas
        ):
            entrada.grid(
                row=1,
                column=indice,
                sticky="ew",
                padx=(
                    10 if indice else 0,
                    0,
                ),
            )

            formulario.columnconfigure(
                indice,
                weight=1,
            )

        ttk.Button(
            formulario,
            text="Crear préstamo",
            command=self._crear_prestamo,
        ).grid(
            row=1,
            column=4,
            padx=(10, 0),
        )

        devolucion = ttk.Frame(
            self.tab_prestamos,
            padding=(0, 10, 0, 0),
        )

        devolucion.pack(
            fill="x"
        )

        ttk.Label(
            devolucion,
            text="ID préstamo a devolver",
        ).pack(
            side="left"
        )

        self.ent_prestamo_devolver = ttk.Entry(
            devolucion,
            width=12,
        )

        self.ent_prestamo_devolver.pack(
            side="left",
            padx=8,
        )

        ttk.Button(
            devolucion,
            text="Registrar devolución",
            command=self._devolver_prestamo,
        ).pack(
            side="left"
        )

        self.tabla_prestamos = (
            self._crear_tabla(
                self.tab_prestamos,
                (
                    "id",
                    "usuario",
                    "equipo",
                    "inicio",
                    "fin",
                    "estado",
                ),
                (
                    "ID",
                    "Usuario",
                    "Equipo",
                    "Préstamo",
                    "Devolución",
                    "Estado",
                ),
            )
        )

    def _crear_tab_consultas(self):
        barra = ttk.Frame(
            self.tab_consultas
        )

        barra.pack(
            fill="x"
        )

        ttk.Label(
            barra,
            text="ID préstamo",
        ).pack(
            side="left"
        )

        self.ent_consulta_prestamo = ttk.Entry(
            barra,
            width=12,
        )

        self.ent_consulta_prestamo.pack(
            side="left",
            padx=8,
        )

        ttk.Button(
            barra,
            text="Consultar",
            command=self._consultar_prestamo,
        ).pack(
            side="left"
        )

        ttk.Button(
            barra,
            text="Ver atrasados",
            command=self._mostrar_atrasados,
        ).pack(
            side="left",
            padx=8,
        )

        self.lbl_resultado_consulta = ttk.Label(
            self.tab_consultas,
            text=(
                "Ingrese un ID o consulte "
                "los préstamos atrasados."
            ),
            padding=(0, 12),
        )

        self.lbl_resultado_consulta.pack(
            anchor="w"
        )

        self.tabla_atrasados = (
            self._crear_tabla(
                self.tab_consultas,
                (
                    "id",
                    "usuario",
                    "equipo",
                    "inicio",
                    "fin",
                    "estado",
                ),
                (
                    "ID",
                    "Usuario",
                    "Equipo",
                    "Préstamo",
                    "Devolución",
                    "Estado",
                ),
            )
        )

    @staticmethod
    def _crear_tabla(
        padre,
        columnas,
        titulos,
    ):
        contenedor = ttk.Frame(
            padre
        )

        contenedor.pack(
            fill="both",
            expand=True,
            pady=(12, 0),
        )

        tabla = ttk.Treeview(
            contenedor,
            columns=columnas,
            show="headings",
        )

        barra = ttk.Scrollbar(
            contenedor,
            orient="vertical",
            command=tabla.yview,
        )

        tabla.configure(
            yscrollcommand=barra.set
        )

        for columna, titulo in zip(
            columnas,
            titulos,
        ):
            tabla.heading(
                columna,
                text=titulo,
            )

            tabla.column(
                columna,
                anchor="center",
                width=130,
            )

        tabla.pack(
            side="left",
            fill="both",
            expand=True,
        )

        barra.pack(
            side="right",
            fill="y",
        )

        return tabla

    def _registrar_usuario(self):
        try:
            usuario = (
                self.usuarios
                .registrar_usuario(
                    self.ent_nombre_usuario.get(),
                    self.ent_apellido_usuario.get(),
                    self.ent_correo_usuario.get(),
                )
            )

            self._limpiar_entradas(
                self.ent_nombre_usuario,
                self.ent_apellido_usuario,
                self.ent_correo_usuario,
            )

            self._actualizar_usuarios()

            messagebox.showinfo(
                "Correcto",
                f"Usuario {usuario.id} registrado.",
            )

        except ValueError as error:
            messagebox.showerror(
                "Dato inválido",
                str(error),
            )

    def _registrar_equipo(self):
        try:
            equipo = (
                self.equipos
                .registrar_equipo(
                    self.ent_nombre_equipo.get(),
                    self.ent_codigo_equipo.get(),
                    self.ent_descripcion_equipo.get(),
                )
            )

            self._limpiar_entradas(
                self.ent_nombre_equipo,
                self.ent_codigo_equipo,
                self.ent_descripcion_equipo,
            )

            self._actualizar_equipos()

            messagebox.showinfo(
                "Correcto",
                f"Equipo {equipo.id} registrado.",
            )

        except ValueError as error:
            messagebox.showerror(
                "Dato inválido",
                str(error),
            )

    def _crear_prestamo(self):
        try:
            prestamo = (
                self.prestamos
                .crear_prestamo(
                    self.ent_usuario_id.get(),
                    self.ent_equipo_id.get(),
                    self.ent_fecha_prestamo.get(),
                    self.ent_fecha_devolucion.get(),
                )
            )

            self._limpiar_entradas(
                self.ent_usuario_id,
                self.ent_equipo_id,
            )

            self._actualizar_equipos()
            self._actualizar_prestamos()

            messagebox.showinfo(
                "Correcto",
                f"Préstamo {prestamo.id} creado.",
            )

        except ValueError as error:
            messagebox.showerror(
                "No se pudo crear",
                str(error),
            )

    def _devolver_prestamo(self):
        try:
            prestamo = (
                self.prestamos
                .registrar_devolucion(
                    self.ent_prestamo_devolver.get()
                )
            )

            self._limpiar_entradas(
                self.ent_prestamo_devolver
            )

            self._actualizar_equipos()
            self._actualizar_prestamos()

            messagebox.showinfo(
                "Correcto",
                (
                    f"Préstamo "
                    f"{prestamo.id} devuelto."
                ),
            )

        except ValueError as error:
            messagebox.showerror(
                "No se pudo devolver",
                str(error),
            )

    def _consultar_prestamo(self):
        try:
            prestamo = (
                self.prestamos
                .consultar_prestamo(
                    self.ent_consulta_prestamo.get()
                )
            )

            if prestamo is None:
                self.lbl_resultado_consulta.config(
                    text=(
                        "No existe un préstamo "
                        "con ese ID."
                    )
                )

                return

            self.lbl_resultado_consulta.config(
                text=(
                    f"Préstamo {prestamo.id} | "
                    f"Usuario {prestamo.usuario_id} | "
                    f"Equipo {prestamo.equipo_id} | "
                    f"{prestamo.fecha_prestamo} a "
                    f"{prestamo.fecha_devolucion} | "
                    f"Estado: {prestamo.estado}"
                )
            )

        except ValueError as error:
            messagebox.showerror(
                "Consulta inválida",
                str(error),
            )

    def _mostrar_atrasados(self):
        atrasados = (
            self.prestamos
            .detectar_prestamos_atrasados()
        )

        self._vaciar_tabla(
            self.tabla_atrasados
        )

        for prestamo in atrasados:
            self.tabla_atrasados.insert(
                "",
                "end",
                values=(
                    prestamo.id,
                    prestamo.usuario_id,
                    prestamo.equipo_id,
                    prestamo.fecha_prestamo,
                    prestamo.fecha_devolucion,
                    prestamo.estado,
                ),
            )

        self.lbl_resultado_consulta.config(
            text=(
                f"Préstamos atrasados: "
                f"{len(atrasados)}"
            )
        )

        self._actualizar_prestamos()

    def _actualizar_todo(self):
        self._actualizar_usuarios()
        self._actualizar_equipos()
        self._actualizar_prestamos()

    def _actualizar_usuarios(self):
        self._vaciar_tabla(
            self.tabla_usuarios
        )

        for usuario in (
            self.usuarios.listar_usuarios()
        ):
            self.tabla_usuarios.insert(
                "",
                "end",
                values=(
                    usuario.id,
                    usuario.nombre,
                    usuario.apellido,
                    usuario.correo,
                ),
            )

    def _actualizar_equipos(self):
        self._vaciar_tabla(
            self.tabla_equipos
        )

        for equipo in (
            self.equipos.listar_equipos()
        ):
            self.tabla_equipos.insert(
                "",
                "end",
                values=(
                    equipo.id,
                    equipo.nombre,
                    equipo.codigo,
                    equipo.descripcion,
                    equipo.estado,
                ),
            )

    def _actualizar_prestamos(self):
        self._vaciar_tabla(
            self.tabla_prestamos
        )

        for prestamo in (
            self.prestamos.listar_prestamos()
        ):
            self.tabla_prestamos.insert(
                "",
                "end",
                values=(
                    prestamo.id,
                    prestamo.usuario_id,
                    prestamo.equipo_id,
                    prestamo.fecha_prestamo,
                    prestamo.fecha_devolucion,
                    prestamo.estado,
                ),
            )

    @staticmethod
    def _vaciar_tabla(tabla):
        for elemento in tabla.get_children():
            tabla.delete(elemento)

    @staticmethod
    def _limpiar_entradas(
        *entradas,
    ):
        for entrada in entradas:
            entrada.delete(
                0,
                "end",
            )

    def _cerrar(self):
        self.conexion.close()
        self.destroy()