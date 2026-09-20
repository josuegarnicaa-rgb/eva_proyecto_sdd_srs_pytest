import tkinter as tk
from datetime import date, timedelta
from tkinter import messagebox, ttk

from app.database import obtener_conexion
from app.services.servicio_equipo import ServicioEquipo
from app.services.servicio_prestamo import ServicioPrestamo
from app.services.servicio_usuario import ServicioUsuario


class InterfazPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(
            "Gestión de préstamos de laboratorio"
        )
        self.geometry("1100x700")
        self.minsize(980, 620)

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

        self.nombre_usuario = tk.StringVar()
        self.apellido_usuario = tk.StringVar()
        self.correo_usuario = tk.StringVar()

        self._crear_campo(
            formulario,
            "Nombre",
            self.nombre_usuario,
            0,
        )

        self._crear_campo(
            formulario,
            "Apellido",
            self.apellido_usuario,
            1,
        )

        self._crear_campo(
            formulario,
            "Correo",
            self.correo_usuario,
            2,
            ancho=32,
        )

        ttk.Button(
            formulario,
            text="Registrar",
            command=self._registrar_usuario,
        ).grid(
            row=1,
            column=3,
            padx=(10, 0),
            sticky="ew",
        )

        for columna in range(3):
            formulario.columnconfigure(
                columna,
                weight=1,
            )

        self.tabla_usuarios = (
            self._crear_tabla(
                self.tab_usuarios,
                columnas=(
                    "id",
                    "nombre",
                    "apellido",
                    "correo",
                ),
                titulos=(
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

        self.nombre_equipo = tk.StringVar()
        self.codigo_equipo = tk.StringVar()
        self.descripcion_equipo = (
            tk.StringVar()
        )

        self._crear_campo(
            formulario,
            "Nombre",
            self.nombre_equipo,
            0,
        )

        self._crear_campo(
            formulario,
            "Código",
            self.codigo_equipo,
            1,
            ancho=16,
        )

        self._crear_campo(
            formulario,
            "Descripción",
            self.descripcion_equipo,
            2,
            ancho=40,
        )

        ttk.Button(
            formulario,
            text="Registrar",
            command=self._registrar_equipo,
        ).grid(
            row=1,
            column=3,
            padx=(10, 0),
            sticky="ew",
        )

        for columna in range(3):
            formulario.columnconfigure(
                columna,
                weight=1,
            )

        self.tabla_equipos = (
            self._crear_tabla(
                self.tab_equipos,
                columnas=(
                    "id",
                    "nombre",
                    "codigo",
                    "descripcion",
                    "estado",
                ),
                titulos=(
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

        hoy = date.today()

        self.usuario_id = tk.StringVar()
        self.equipo_id = tk.StringVar()

        self.fecha_prestamo = tk.StringVar(
            value=hoy.isoformat()
        )

        self.fecha_devolucion = tk.StringVar(
            value=(
                hoy
                + timedelta(days=7)
            ).isoformat()
        )

        self._crear_campo(
            formulario,
            "ID usuario",
            self.usuario_id,
            0,
            ancho=12,
        )

        self._crear_campo(
            formulario,
            "ID equipo",
            self.equipo_id,
            1,
            ancho=12,
        )

        self._crear_campo(
            formulario,
            "Fecha préstamo",
            self.fecha_prestamo,
            2,
            ancho=16,
        )

        self._crear_campo(
            formulario,
            "Fecha devolución",
            self.fecha_devolucion,
            3,
            ancho=16,
        )

        ttk.Button(
            formulario,
            text="Crear préstamo",
            command=self._crear_prestamo,
        ).grid(
            row=1,
            column=4,
            padx=(10, 0),
            sticky="ew",
        )

        for columna in range(4):
            formulario.columnconfigure(
                columna,
                weight=1,
            )

        devolucion = ttk.Frame(
            self.tab_prestamos,
            padding=(0, 10, 0, 0),
        )

        devolucion.pack(
            fill="x"
        )

        self.prestamo_devolver = (
            tk.StringVar()
        )

        ttk.Label(
            devolucion,
            text="ID préstamo a devolver",
        ).pack(
            side="left"
        )

        ttk.Entry(
            devolucion,
            textvariable=(
                self.prestamo_devolver
            ),
            width=12,
        ).pack(
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
                columnas=(
                    "id",
                    "usuario",
                    "equipo",
                    "inicio",
                    "fin",
                    "estado",
                ),
                titulos=(
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

        self.consulta_prestamo = (
            tk.StringVar()
        )

        ttk.Label(
            barra,
            text="ID préstamo",
        ).pack(
            side="left"
        )

        ttk.Entry(
            barra,
            textvariable=(
                self.consulta_prestamo
            ),
            width=12,
        ).pack(
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

        self.lbl_resultado_consulta = (
            ttk.Label(
                self.tab_consultas,
                text=(
                    "Ingrese un ID o consulte "
                    "los préstamos atrasados."
                ),
                padding=(0, 12),
            )
        )

        self.lbl_resultado_consulta.pack(
            anchor="w"
        )

        self.tabla_atrasados = (
            self._crear_tabla(
                self.tab_consultas,
                columnas=(
                    "id",
                    "usuario",
                    "equipo",
                    "inicio",
                    "fin",
                    "estado",
                ),
                titulos=(
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
    def _crear_campo(
        padre,
        texto,
        variable,
        columna,
        ancho=24,
    ):
        separacion = (
            (10, 0)
            if columna
            else (0, 0)
        )

        ttk.Label(
            padre,
            text=texto,
        ).grid(
            row=0,
            column=columna,
            sticky="w",
            padx=separacion,
        )

        ttk.Entry(
            padre,
            textvariable=variable,
            width=ancho,
        ).grid(
            row=1,
            column=columna,
            sticky="ew",
            padx=separacion,
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

        barra_vertical = ttk.Scrollbar(
            contenedor,
            orient="vertical",
            command=tabla.yview,
        )

        barra_horizontal = ttk.Scrollbar(
            contenedor,
            orient="horizontal",
            command=tabla.xview,
        )

        tabla.configure(
            yscrollcommand=(
                barra_vertical.set
            ),
            xscrollcommand=(
                barra_horizontal.set
            ),
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
                width=140,
                minwidth=90,
            )

        tabla.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        barra_vertical.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        barra_horizontal.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        contenedor.rowconfigure(
            0,
            weight=1,
        )

        contenedor.columnconfigure(
            0,
            weight=1,
        )

        return tabla

    def _registrar_usuario(self):
        try:
            usuario = (
                self.usuarios
                .registrar_usuario(
                    self.nombre_usuario.get(),
                    self.apellido_usuario.get(),
                    self.correo_usuario.get(),
                )
            )

            self._limpiar_variables(
                self.nombre_usuario,
                self.apellido_usuario,
                self.correo_usuario,
            )

            self._actualizar_usuarios()

            messagebox.showinfo(
                "Correcto",
                (
                    f"Usuario "
                    f"{usuario.id} registrado."
                ),
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
                    self.nombre_equipo.get(),
                    self.codigo_equipo.get(),
                    self.descripcion_equipo.get(),
                )
            )

            self._limpiar_variables(
                self.nombre_equipo,
                self.codigo_equipo,
                self.descripcion_equipo,
            )

            self._actualizar_equipos()

            messagebox.showinfo(
                "Correcto",
                (
                    f"Equipo "
                    f"{equipo.id} registrado."
                ),
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
                    self.usuario_id.get(),
                    self.equipo_id.get(),
                    self.fecha_prestamo.get(),
                    self.fecha_devolucion.get(),
                )
            )

            self._limpiar_variables(
                self.usuario_id,
                self.equipo_id,
            )

            self._actualizar_equipos()
            self._actualizar_prestamos()

            messagebox.showinfo(
                "Correcto",
                (
                    f"Préstamo "
                    f"{prestamo.id} creado."
                ),
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
                    self.prestamo_devolver.get()
                )
            )

            self._limpiar_variables(
                self.prestamo_devolver
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
                    self.consulta_prestamo.get()
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
                    f"Usuario "
                    f"{prestamo.usuario_id} | "
                    f"Equipo "
                    f"{prestamo.equipo_id} | "
                    f"{prestamo.fecha_prestamo} "
                    f"a "
                    f"{prestamo.fecha_devolucion} "
                    f"| Estado: "
                    f"{prestamo.estado}"
                )
            )

            self._actualizar_prestamos()

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
                "Préstamos atrasados: "
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
            self.prestamos
            .listar_prestamos()
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
        for elemento in (
            tabla.get_children()
        ):
            tabla.delete(
                elemento
            )

    @staticmethod
    def _limpiar_variables(
        *variables,
    ):
        for variable in variables:
            variable.set("")

    def _cerrar(self):
        self.conexion.close()
        self.destroy()