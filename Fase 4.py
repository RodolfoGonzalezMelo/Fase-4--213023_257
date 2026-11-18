from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk, messagebox
import logging

# ==================================================
# CONFIGURACION LOG
# ==================================================

logging.basicConfig(
    filename="eventos.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ==================================================
# EXCEPCIONES
# ==================================================

class ClienteError(Exception):
    pass

class ServicioError(Exception):
    pass

class ReservaError(Exception):
    pass

# ==================================================
# CLASE ABSTRACTA
# ==================================================

class Persona(ABC):

    @abstractmethod
    def mostrar_info(self):
        pass

# ==================================================
# CLIENTE
# ==================================================

class Cliente(Persona):

    def __init__(self, nombre, identificacion, correo):

        if not nombre.strip():
            raise ClienteError(
                "El nombre no puede estar vacío"
            )

        if not identificacion.isdigit():
            raise ClienteError(
                "La identificación debe ser numérica"
            )

        if len(identificacion) < 5:
            raise ClienteError(
                "Identificación demasiado corta"
            )

        if "@" not in correo:
            raise ClienteError(
                "Correo inválido"
            )

        self.__nombre = nombre
        self.__identificacion = identificacion
        self.__correo = correo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def identificacion(self):
        return self.__identificacion

    @property
    def correo(self):
        return self.__correo

    def mostrar_info(self):
        return f"{self.nombre} - {self.identificacion}"

# ==================================================
# SERVICIOS
# ==================================================

class Servicio(ABC):

    def __init__(self, nombre, tarifa):

        if tarifa <= 0:
            raise ServicioError(
                "La tarifa debe ser mayor que cero"
            )

        self.nombre = nombre
        self.tarifa = tarifa

    @abstractmethod
    def calcular_costo(self, horas):
        pass

    @abstractmethod
    def descripcion(self):
        pass

class ReservaSala(Servicio):

    def calcular_costo(self, horas):
        return self.tarifa * horas

    def descripcion(self):
        return "Reserva de Sala"

class AlquilerEquipos(Servicio):

    def calcular_costo(self, horas):
        return (self.tarifa * horas) + 20000

    def descripcion(self):
        return "Alquiler de Equipos"

class AsesoriaEspecializada(Servicio):

    def calcular_costo(self, horas):
        return (self.tarifa * horas) * 1.19

    def descripcion(self):
        return "Asesoría Especializada"

# ==================================================
# RESERVA
# ==================================================

class Reserva:

    def __init__(self, cliente, servicio, horas):

        if horas <= 0:
            raise ReservaError(
                "Las horas deben ser mayores a cero"
            )

        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "Pendiente"

    def confirmar(self):
        self.estado = "Confirmada"

    def cancelar(self):
        self.estado = "Cancelada"

    def calcular_total(self, descuento=0):

        valor = self.servicio.calcular_costo(self.horas)

        if descuento > 0:
            valor -= valor * descuento / 100

        return round(valor, 2)

# ==================================================
# DATOS EN MEMORIA
# ==================================================

clientes = []
servicios = []
reservas = []

# ==================================================
# INTERFAZ
# ==================================================

class Aplicacion:

    def __init__(self, ventana):

        self.ventana = ventana

        self.ventana.title(
            "Software FJ"
        )

        self.ventana.geometry(
            "1100x700"
        )

        self.ventana.resizable(
            False,
            False
        )
        # ==========================================
# BARRA DE MENÚ
# ==========================================

barra_menu = tk.Menu(self.ventana)

self.ventana.config(menu=barra_menu)

# MENÚ ARCHIVO

menu_archivo = tk.Menu(
    barra_menu,
    tearoff=0
)

barra_menu.add_cascade(
    label="Archivo",
    menu=menu_archivo
)

menu_archivo.add_command(
    label="Salir",
    command=self.salir_aplicacion
)

# MENÚ HERRAMIENTAS

menu_herramientas = tk.Menu(
    barra_menu,
    tearoff=0
)

barra_menu.add_cascade(
    label="Herramientas",
    menu=menu_herramientas
)

menu_herramientas.add_command(
    label="Cargar Datos de Prueba",
    command=self.cargar_datos_prueba
)

menu_herramientas.add_separator()

menu_herramientas.add_command(
    label="Limpiar Todo",
    command=self.limpiar_datos
)

# MENÚ AYUDA

menu_ayuda = tk.Menu(
    barra_menu,
    tearoff=0
)

barra_menu.add_cascade(
    label="Ayuda",
    menu=menu_ayuda
)

menu_ayuda.add_command(
    label="Acerca de",
    command=self.acerca_de
)

        titulo = tk.Label(
            ventana,
            text="SOFTWARE FJ - GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS",
            font=("Arial", 16, "bold")
        )

        titulo.pack(
            pady=10
        )

        self.notebook = ttk.Notebook(
            ventana
        )

        self.notebook.pack(
            fill="both",
            expand=True
        )

        self.tab_clientes = ttk.Frame(
            self.notebook
        )

        self.tab_servicios = ttk.Frame(
            self.notebook
        )

        self.tab_reservas = ttk.Frame(
            self.notebook
        )

        self.notebook.add(
            self.tab_clientes,
            text="Clientes"
        )

        self.notebook.add(
            self.tab_servicios,
            text="Servicios"
        )

        self.notebook.add(
            self.tab_reservas,
            text="Reservas"
        )

        self.crear_pestana_clientes()
        self.crear_pestana_servicios()
        self.crear_pestana_reservas()

    # ==============================================
    # CLIENTES
    # ==============================================

    def crear_pestana_clientes(self):

        tk.Label(
            self.tab_clientes,
            text="Nombre"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.nombre_cliente = tk.Entry(
            self.tab_clientes
        )

        self.nombre_cliente.grid(
            row=0,
            column=1
        )

        tk.Label(
            self.tab_clientes,
            text="Identificación"
        ).grid(row=1, column=0)

        self.id_cliente = tk.Entry(
            self.tab_clientes
        )

        self.id_cliente.grid(
            row=1,
            column=1
        )

        tk.Label(
            self.tab_clientes,
            text="Correo"
        ).grid(row=2, column=0)

        self.correo_cliente = tk.Entry(
            self.tab_clientes
        )

        self.correo_cliente.grid(
            row=2,
            column=1
        )

        tk.Button(
            self.tab_clientes,
            text="Registrar Cliente",
            bg="green",
            fg="white",
            command=self.registrar_cliente
        ).grid(row=3,
               column=0,
               columnspan=2,
               pady=10)

        self.tv_clientes = ttk.Treeview(
            self.tab_clientes,
            columns=("nombre", "id", "correo"),
            show="headings",
            height=15
        )

        self.tv_clientes.heading(
            "nombre",
            text="Nombre"
        )

        self.tv_clientes.heading(
            "id",
            text="Identificación"
        )

        self.tv_clientes.heading(
            "correo",
            text="Correo"
        )

        self.tv_clientes.grid(
            row=5,
            column=0,
            columnspan=4,
            padx=10
        )

    def registrar_cliente(self):

        try:

            cliente = Cliente(
                self.nombre_cliente.get(),
                self.id_cliente.get(),
                self.correo_cliente.get()
            )

        except Exception as e:

            logging.error(str(e))

            messagebox.showerror(
                "Error",
                str(e)
            )

        else:

            clientes.append(cliente)

            self.tv_clientes.insert(
                "",
                tk.END,
                values=(
                    cliente.nombre,
                    cliente.identificacion,
                    cliente.correo
                )
            )

            logging.info(
                "Cliente registrado correctamente"
            )

            self.actualizar_combos()

            self.nombre_cliente.delete(0, tk.END)
            self.id_cliente.delete(0, tk.END)
            self.correo_cliente.delete(0, tk.END)

            messagebox.showinfo(
                "Correcto",
                "Cliente registrado"
            )

    # ==============================================
    # SERVICIOS
    # ==============================================

    def crear_pestana_servicios(self):

        tk.Label(
            self.tab_servicios,
            text="Nombre Servicio"
        ).grid(row=0, column=0)

        self.nombre_servicio = tk.Entry(
            self.tab_servicios
        )

        self.nombre_servicio.grid(
            row=0,
            column=1
        )

        tk.Label(
            self.tab_servicios,
            text="Tarifa"
        ).grid(row=1, column=0)

        self.tarifa_servicio = tk.Entry(
            self.tab_servicios
        )

        self.tarifa_servicio.grid(
            row=1,
            column=1
        )

        tk.Label(
            self.tab_servicios,
            text="Tipo"
        ).grid(row=2, column=0)

        self.tipo_servicio = ttk.Combobox(
            self.tab_servicios,
            values=[
                "Sala",
                "Equipos",
                "Asesoria"
            ]
        )

        self.tipo_servicio.grid(
            row=2,
            column=1
        )

        tk.Button(
            self.tab_servicios,
            text="Crear Servicio",
            command=self.registrar_servicio
        ).grid(
            row=3,
            column=0,
            columnspan=2
        )

        self.tv_servicios = ttk.Treeview(
            self.tab_servicios,
            columns=("nombre", "tipo", "tarifa"),
            show="headings"
        )

        self.tv_servicios.heading(
            "nombre",
            text="Nombre"
        )

        self.tv_servicios.heading(
            "tipo",
            text="Tipo"
        )

        self.tv_servicios.heading(
            "tarifa",
            text="Tarifa"
        )

        self.tv_servicios.grid(
            row=5,
            column=0,
            columnspan=5
        )

    def registrar_servicio(self):

        try:

            try:
                tarifa = float(
                    self.tarifa_servicio.get()
                )
            except ValueError as e:

                raise ServicioError(
                    "La tarifa debe ser numérica"
                ) from e

            tipo = self.tipo_servicio.get()

            if tipo == "Sala":
                servicio = ReservaSala(
                    self.nombre_servicio.get(),
                    tarifa
                )

            elif tipo == "Equipos":
                servicio = AlquilerEquipos(
                    self.nombre_servicio.get(),
                    tarifa
                )

            elif tipo == "Asesoria":
                servicio = AsesoriaEspecializada(
                    self.nombre_servicio.get(),
                    tarifa
                )

            else:
                raise ServicioError(
                    "Seleccione un tipo válido"
                )

        except Exception as e:

            logging.error(str(e))

            messagebox.showerror(
                "Error",
                str(e)
            )

        else:

            servicios.append(servicio)

            self.tv_servicios.insert(
                "",
                tk.END,
                values=(
                    servicio.nombre,
                    tipo,
                    tarifa
                )
            )

            self.actualizar_combos()

            messagebox.showinfo(
                "Correcto",
                "Servicio registrado"
            )

    # ==============================================
    # RESERVAS
    # ==============================================

    def crear_pestana_reservas(self):

        tk.Label(
            self.tab_reservas,
            text="Cliente"
        ).grid(row=0, column=0)

        self.cmb_cliente = ttk.Combobox(
            self.tab_reservas
        )

        self.cmb_cliente.grid(
            row=0,
            column=1
        )

        tk.Label(
            self.tab_reservas,
            text="Servicio"
        ).grid(row=1, column=0)

        self.cmb_servicio = ttk.Combobox(
            self.tab_reservas
        )

        self.cmb_servicio.grid(
            row=1,
            column=1
        )

        tk.Label(
            self.tab_reservas,
            text="Horas"
        ).grid(row=2, column=0)

        self.horas = tk.Entry(
            self.tab_reservas
        )

        self.horas.grid(
            row=2,
            column=1
        )

        tk.Button(
            self.tab_reservas,
            text="Confirmar Reserva",
            bg="green",
            fg="white",
            command=self.crear_reserva
        ).grid(
            row=3,
            column=0
        )

        self.tv_reservas = ttk.Treeview(
            self.tab_reservas,
            columns=(
                "cliente",
                "servicio",
                "estado",
                "valor"
            ),
            show="headings"
        )

        for columna in (
                "cliente",
                "servicio",
                "estado",
                "valor"):
            self.tv_reservas.heading(
                columna,
                text=columna.upper()
            )

        self.tv_reservas.grid(
            row=5,
            column=0,
            columnspan=5
        )

    def crear_reserva(self):

        try:

            if self.cmb_cliente.current() == -1:
                raise ReservaError(
                    "Seleccione cliente"
                )

            if self.cmb_servicio.current() == -1:
                raise ReservaError(
                    "Seleccione servicio"
                )

            horas = int(
                self.horas.get()
            )

            cliente = clientes[
                self.cmb_cliente.current()
            ]

            servicio = servicios[
                self.cmb_servicio.current()
            ]

            reserva = Reserva(
                cliente,
                servicio,
                horas
            )

        except Exception as e:

            logging.error(str(e))

            messagebox.showerror(
                "Error",
                str(e)
            )

        else:

            reserva.confirmar()

            reservas.append(
                reserva
            )

            self.tv_reservas.insert(
                "",
                tk.END,
                values=(
                    cliente.nombre,
                    servicio.nombre,
                    reserva.estado,
                    reserva.calcular_total()
                )
            )

            logging.info(
                "Reserva creada"
            )

            messagebox.showinfo(
                "Correcto",
                "Reserva confirmada"
            )

        finally:

            logging.info(
                "Proceso reserva finalizado"
            )

    # ==============================================

    def actualizar_combos(self):

        self.cmb_cliente["values"] = [
            c.nombre for c in clientes
        ]

        self.cmb_servicio["values"] = [
            s.nombre for s in servicios
        ]

# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    logging.info(
        "Aplicación iniciada"
    )

    root = tk.Tk()

    app = Aplicacion(root)

    root.mainloop()

    logging.info(
        "Aplicación finalizada"
    )