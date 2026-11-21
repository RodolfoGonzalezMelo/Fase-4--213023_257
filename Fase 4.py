# ============================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA
# PROGRAMACIÓN - FASE 4
# SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES,
# SERVICIOS Y RESERVAS - SOFTWARE FJ
# AUTOR: RODOLFO GONZALEZ MELO - CEAD TUNJA
# ============================================================

from abc import ABC, abstractmethod
from datetime import datetime
import logging

# ============================================================
# CONFIGURACIÓN DE LOGS
# ============================================================

logging.basicConfig(
    filename="eventos.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ============================================================
# EXCEPCIONES PERSONALIZADAS
# ============================================================

class ClienteError(Exception):
    """Errores relacionados con clientes"""
    pass


class ServicioError(Exception):
    """Errores relacionados con servicios"""
    pass


class ReservaError(Exception):
    """Errores relacionados con reservas"""
    pass


class DatoInvalidoError(Exception):
    """Errores generados por datos incorrectos o incompletos."""
    pass


class OperacionNoPermitidaError(Exception):
    """Errores por operaciones que no están permitidas."""
    pass


class ServicioNoDisponibleError(ServicioError):
    """Errores cuando un servicio no está disponible."""
    pass


# ============================================================
# CLASE ABSTRACTA PERSONA
# ============================================================

class Persona(ABC):
    """
    Clase abstracta base para todas las personas
    del sistema.
    """

    @abstractmethod
    def mostrar_info(self):
        pass


# ============================================================
# CLIENTE
# ============================================================

class Cliente(Persona):

    def __init__(self, nombre, identificacion, correo):
        try:
            self.validar_nombre(nombre)
            self.validar_identificacion(identificacion)
            self.validar_correo(correo)
        except (ClienteError, AttributeError, TypeError) as error:
            registrar_log(
                f"Error al crear cliente: {error}",
                "error"
            )
            raise DatoInvalidoError(
                "Los datos del cliente son inválidos"
            ) from error

        self.__nombre = nombre
        self.__identificacion = identificacion
        self.__correo = correo

    # --------------------------------------------------------

    @staticmethod
    def validar_nombre(nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ClienteError(
                "El nombre es obligatorio"
            )

        if len(nombre) < 3:
            raise ClienteError(
                "El nombre es demasiado corto"
            )

    # --------------------------------------------------------

    @staticmethod
    def validar_identificacion(identificacion):
        if not isinstance(identificacion, str) or not identificacion.isdigit():
            raise ClienteError(
                "La identificación debe ser numérica"
            )

        if len(identificacion) < 5:
            raise ClienteError(
                "La identificación debe tener mínimo 5 dígitos"
            )

    # --------------------------------------------------------

    @staticmethod
    def validar_correo(correo):
        if not isinstance(correo, str):
            raise ClienteError(
                "Correo electrónico inválido"
            )

        correo = correo.strip()

        if "@" not in correo or correo.count("@") != 1:
            raise ClienteError(
                "Correo electrónico inválido"
            )

        if "." not in correo:
            raise ClienteError(
                "Correo electrónico inválido"
            )

    # --------------------------------------------------------

    @property
    def nombre(self):
        return self.__nombre

    @property
    def identificacion(self):
        return self.__identificacion

    @property
    def correo(self):
        return self.__correo

    # --------------------------------------------------------

    def mostrar_info(self):

        return (
            f"{self.__nombre} - "
            f"{self.__identificacion}"
        )

    # --------------------------------------------------------

    def __str__(self):

        return (
            f"Cliente: {self.__nombre}"
        )


# ============================================================
# CLASE ABSTRACTA SERVICIO
# ============================================================

class Servicio(ABC):

    def __init__(self, nombre, tarifa):
        try:
            tarifa = float(tarifa)
        except (TypeError, ValueError) as error:
            raise DatoInvalidoError(
                "La tarifa debe ser un valor numérico"
            ) from error

        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioError("Nombre de servicio obligatorio")

        if tarifa <= 0:
            raise ServicioError("La tarifa debe ser mayor a cero")

        self.nombre = nombre
        self.tarifa = round(tarifa, 2)
        self.disponible = True

    # --------------------------------------------------------

    @abstractmethod
    def calcular_costo(self, horas):
        pass

    # --------------------------------------------------------

    @abstractmethod
    def descripcion(self):
        pass

    @abstractmethod
    def validar_parametros(self, horas):
        pass

    # --------------------------------------------------------

    def cambiar_disponibilidad(
        self,
        estado
    ):

        self.disponible = estado


# ============================================================
# RESERVA DE SALAS
# ============================================================

class ReservaSala(Servicio):

    def calcular_costo(self, horas):
        self.validar_parametros(horas)

        return self.tarifa * horas

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or isinstance(horas, bool):
            raise DatoInvalidoError("Las horas deben ser numéricas")
        if horas <= 0:
            raise ServicioError("Horas inválidas")

    def descripcion(self):

        return (
            "Servicio de reserva de salas"
        )


# ============================================================
# ALQUILER DE EQUIPOS
# ============================================================

class AlquilerEquipos(Servicio):

    def calcular_costo(self, horas):
        self.validar_parametros(horas)

        seguro = 20000

        return (
            self.tarifa * horas
        ) + seguro

    def descripcion(self):

        return (
            "Servicio de alquiler de equipos"
        )

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or isinstance(horas, bool):
            raise DatoInvalidoError("Las horas deben ser numéricas")
        if horas <= 0:
            raise ServicioError("Horas inválidas")


# ============================================================
# ASESORÍA ESPECIALIZADA
# ============================================================

class AsesoriaEspecializada(Servicio):

    def calcular_costo(self, horas):
        self.validar_parametros(horas)

        subtotal = (
            self.tarifa * horas
        )

        iva = subtotal * 0.19

        return subtotal + iva

    def descripcion(self):

        return (
            "Servicio de asesoría profesional"
        )

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or isinstance(horas, bool):
            raise DatoInvalidoError("Las horas deben ser numéricas")
        if horas <= 0:
            raise ServicioError("Horas inválidas")


# ============================================================
# RESERVA
# ============================================================

class Reserva:

    contador = 1

    def __init__(
            self,
            cliente,
            servicio,
            horas
    ):
        if not isinstance(
                cliente,
                Cliente
        ):
            raise ReservaError(
                "Cliente inválido"
            )

        if not isinstance(
                servicio,
                Servicio
        ):
            raise ReservaError(
                "Servicio inválido"
            )

        if not isinstance(horas, (int, float)) or isinstance(horas, bool):
            raise DatoInvalidoError(
                "Las horas deben ser numéricas"
            )

        if horas <= 0:
            raise ReservaError(
                "Horas inválidas"
            )

        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                "Servicio no disponible"
            )

        self.codigo = Reserva.contador
        Reserva.contador += 1

        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas

        self.fecha = datetime.now()

        self.estado = "Pendiente"

    # --------------------------------------------------------

    def confirmar(self):
        if self.estado == "Cancelada":
            raise OperacionNoPermitidaError(
                "Una reserva cancelada no puede confirmarse"
            )
        self.estado = "Confirmada"

        logging.info(
            f"Reserva {self.codigo} confirmada"
        )

    # --------------------------------------------------------

    def cancelar(self):
        if self.estado == "Procesada":
            raise OperacionNoPermitidaError(
                "Una reserva procesada no puede cancelarse"
            )
        if self.estado == "Cancelada":
            raise OperacionNoPermitidaError(
                "La reserva ya se encuentra cancelada"
            )
        self.estado = "Cancelada"

        self.servicio.disponible = True

        logging.info(
            f"Reserva {self.codigo} cancelada"
        )

    # --------------------------------------------------------

    def procesar(self):

        if self.estado != "Confirmada":

            raise ReservaError(
                "La reserva debe estar confirmada"
            )

        self.estado = "Procesada"

        self.servicio.disponible = False

        logging.info(
            f"Reserva {self.codigo} procesada"
        )

    # --------------------------------------------------------
    # Simulación de sobrecarga solicitada
    # --------------------------------------------------------

    def calcular_total(
            self,
            descuento=0,
            impuesto=0,
            cargo_extra=0
    ):
        if any(
            not isinstance(valor, (int, float))
            or isinstance(valor, bool)
            for valor in (descuento, impuesto, cargo_extra)
        ):
            raise DatoInvalidoError(
                "Descuento, impuesto y cargo extra deben ser numéricos"
            )
        if descuento < 0 or descuento > 100:
            raise ReservaError(
                "El descuento debe estar entre 0 y 100"
            )
        if impuesto < 0:
            raise ReservaError(
                "El impuesto no puede ser negativo"
            )
        if cargo_extra < 0:
            raise ReservaError(
                "El cargo extra no puede ser negativo"
            )
        total = (
            self.servicio.calcular_costo(
                self.horas
            )
        )

        if descuento > 0:

            total -= (
                total * descuento / 100
            )

        if impuesto > 0:

            total += (
                total * impuesto / 100
            )

        total += cargo_extra

        return round(total, 2)

    # --------------------------------------------------------

    def obtener_resumen(self):

        return (
            f"{self.codigo} | "
            f"{self.cliente.nombre} | "
            f"{self.servicio.nombre} | "
            f"{self.estado}"
        )


# ============================================================
# ESTRUCTURAS EN MEMORIA
# ============================================================

clientes = []
servicios = []
reservas = []


# ============================================================
# FUNCIONES DE APOYO
# ============================================================

def validar_cliente_duplicado(
        identificacion):

    for cliente in clientes:

        if cliente.identificacion == identificacion:

            raise ClienteError(
                "El cliente ya existe"
            )


def validar_servicio_duplicado(
        nombre):

    for servicio in servicios:

        if (
            servicio.nombre.lower()
            ==
            nombre.lower()
        ):

            raise ServicioError(
                "Servicio ya registrado"
            )


def registrar_log(
        mensaje,
        nivel="info"
):

    if nivel == "info":
        logging.info(mensaje)

    elif nivel == "warning":
        logging.warning(mensaje)

    elif nivel == "error":
        logging.error(mensaje)
# ============================================================
# INTERFAZ GRÁFICA
# ============================================================

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class Aplicacion:

    def __init__(self, ventana):

        self.ventana = ventana

        self.ventana.title(
            "SOFTWARE FJ"
        )

        self.ventana.geometry(
            "850x550"
        )

        self.ventana.resizable(
            False,
            False
        )

        # ====================================================
        # MENU PRINCIPAL
        # ====================================================

        self.crear_menu()

        # ====================================================
        # TITULO
        # ====================================================

        titulo = tk.Label(
            self.ventana,
            text="SOFTWARE FJ - SISTEMA INTEGRAL DE GESTIÓN",
            font=("Arial", 18, "bold")
        )

        titulo.pack(
            pady=10
        )

        # ====================================================
        # NOTEBOOK
        # ====================================================

        self.notebook = ttk.Notebook(
            self.ventana
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

        self.crear_tab_clientes()
        self.crear_tab_servicios()
        self.crear_tab_reservas()

    # ========================================================
    # MENU
    # ========================================================

    def crear_menu(self):

        barra = tk.Menu(
            self.ventana
        )

        self.ventana.config(
            menu=barra
        )

        # ----------------------

        menu_archivo = tk.Menu(
            barra,
            tearoff=0
        )

        barra.add_cascade(
            label="Archivo",
            menu=menu_archivo
        )

        menu_archivo.add_command(
            label="Salir",
            command=self.salir
        )

        # ----------------------

        menu_herramientas = tk.Menu(
            barra,
            tearoff=0
        )

        barra.add_cascade(
            label="Herramientas",
            menu=menu_herramientas
        )

        menu_herramientas.add_command(
            label="Limpiar Información",
            command=self.limpiar_datos
        )

        menu_herramientas.add_separator()

        menu_herramientas.add_command(
            label="Cargar Datos de Prueba",
            command=self.cargar_datos_prueba
        )

        # ----------------------

        menu_ayuda = tk.Menu(
            barra,
            tearoff=0
        )

        barra.add_cascade(
            label="Ayuda",
            menu=menu_ayuda
        )

        menu_ayuda.add_command(
            label="Acerca de",
            command=self.acerca_de
        )

    # ========================================================
    # TABLA CLIENTES
    # ========================================================

    def crear_tab_clientes(self):

        tk.Label(
            self.tab_clientes,
            text="Nombre"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.txt_nombre = tk.Entry(
            self.tab_clientes,
            width=40
        )

        self.txt_nombre.grid(
            row=0,
            column=1
        )

        tk.Label(
            self.tab_clientes,
            text="Identificación"
        ).grid(
            row=1,
            column=0
        )

        self.txt_identificacion = tk.Entry(
            self.tab_clientes,
            width=40
        )

        self.txt_identificacion.grid(
            row=1,
            column=1
        )

        tk.Label(
            self.tab_clientes,
            text="Correo"
        ).grid(
            row=2,
            column=0
        )

        self.txt_correo = tk.Entry(
            self.tab_clientes,
            width=40
        )

        self.txt_correo.grid(
            row=2,
            column=1
        )

        tk.Button(
            self.tab_clientes,
            text="Registrar Cliente",
            bg="green",
            fg="white",
            command=self.registrar_cliente
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            pady=10
        )

        self.tv_clientes = ttk.Treeview(
            self.tab_clientes,
            columns=(
                "nombre",
                "identificacion",
                "correo"
            ),
            show="headings",
            height=15
        )

        self.tv_clientes.heading(
            "nombre",
            text="Nombre"
        )

        self.tv_clientes.heading(
            "identificacion",
            text="Identificación"
        )

        self.tv_clientes.heading(
            "correo",
            text="Correo"
        )

        self.tv_clientes.column(
            "nombre",
            width=250
        )

        self.tv_clientes.column(
            "identificacion",
            width=150
        )

        self.tv_clientes.column(
            "correo",
            width=300
        )

        self.tv_clientes.grid(
            row=5,
            column=0,
            columnspan=5,
            padx=20,
            pady=20
        )

    # ========================================================
    # REGISTRAR CLIENTE
    # ========================================================

    def registrar_cliente(self):

        try:

            validar_cliente_duplicado(
                self.txt_identificacion.get()
            )

            cliente = Cliente(
                self.txt_nombre.get(),
                self.txt_identificacion.get(),
                self.txt_correo.get()
            )

            clientes.append(
                cliente
            )

            self.tv_clientes.insert(
                "",
                tk.END,
                values=(
                    cliente.nombre,
                    cliente.identificacion,
                    cliente.correo
                )
            )

            self.actualizar_combos()

            registrar_log(
                f"Cliente registrado: {cliente.nombre}"
            )

            self.txt_nombre.delete(
                0,
                tk.END
            )

            self.txt_identificacion.delete(
                0,
                tk.END
            )

            self.txt_correo.delete(
                0,
                tk.END
            )

            messagebox.showinfo(
                "Correcto",
                "Cliente registrado correctamente"
            )

        except Exception as e:

            registrar_log(
                str(e),
                "error"
            )

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ========================================================
    # TABLA SERVICIOS
    # ========================================================

    def crear_tab_servicios(self):

        tk.Label(
            self.tab_servicios,
            text="Nombre Servicio"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.txt_servicio = tk.Entry(
            self.tab_servicios,
            width=40
        )

        self.txt_servicio.grid(
            row=0,
            column=1
        )

        tk.Label(
            self.tab_servicios,
            text="Tarifa"
        ).grid(
            row=1,
            column=0
        )

        self.txt_tarifa = tk.Entry(
            self.tab_servicios,
            width=40
        )

        self.txt_tarifa.grid(
            row=1,
            column=1
        )

        tk.Label(
            self.tab_servicios,
            text="Tipo"
        ).grid(
            row=2,
            column=0
        )

        self.cmb_tipo_servicio = ttk.Combobox(
            self.tab_servicios,
            state="readonly",
            values=[
                "Sala",
                "Equipos",
                "Asesoria"
            ]
        )

        self.cmb_tipo_servicio.grid(
            row=2,
            column=1
        )

        tk.Button(
            self.tab_servicios,
            text="Registrar Servicio",
            bg="blue",
            fg="white",
            command=self.registrar_servicio
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            pady=10
        )

        self.tv_servicios = ttk.Treeview(
            self.tab_servicios,
            columns=(
                "nombre",
                "tipo",
                "tarifa"
            ),
            show="headings",
            height=15
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
            columnspan=5,
            padx=20,
            pady=20
        )

    # ========================================================
    # REGISTRAR SERVICIO
    # ========================================================

    def registrar_servicio(self):
        try:
            tarifa = float(
                self.txt_tarifa.get()
            )
        except (TypeError, ValueError) as error:
            registrar_log(
                "La tarifa del servicio no es numérica",
                "error"
            )
            messagebox.showerror(
                "Error",
                "La tarifa debe ser un valor numérico"
            )
            return

        try:

            validar_servicio_duplicado(
                self.txt_servicio.get()
            )

            tipo = self.cmb_tipo_servicio.get()

            if tipo == "Sala":

                servicio = ReservaSala(
                    self.txt_servicio.get(),
                    tarifa
                )

            elif tipo == "Equipos":

                servicio = AlquilerEquipos(
                    self.txt_servicio.get(),
                    tarifa
                )

            elif tipo == "Asesoria":

                servicio = AsesoriaEspecializada(
                    self.txt_servicio.get(),
                    tarifa
                )

            else:

                raise ServicioError(
                    "Seleccione un tipo válido"
                )

            servicios.append(
                servicio
            )

            self.tv_servicios.insert(
                "",
                tk.END,
                values=(
                    servicio.nombre,
                    tipo,
                    servicio.tarifa
                )
            )

            self.actualizar_combos()

            registrar_log(
                f"Servicio registrado: {servicio.nombre}"
            )

            messagebox.showinfo(
                "Correcto",
                "Servicio registrado correctamente"
            )

        except Exception as e:

            registrar_log(
                str(e),
                "error"
            )

            messagebox.showerror(
                "Error",
                str(e)
            )
    # ========================================================
    # TABLA RESERVAS
    # ========================================================

    def crear_tab_reservas(self):

        tk.Label(
            self.tab_reservas,
            text="Cliente"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.cmb_cliente = ttk.Combobox(
            self.tab_reservas,
            state="readonly",
            width=40
        )

        self.cmb_cliente.grid(
            row=0,
            column=1
        )

        tk.Label(
            self.tab_reservas,
            text="Servicio"
        ).grid(
            row=1,
            column=0
        )

        self.cmb_servicio = ttk.Combobox(
            self.tab_reservas,
            state="readonly",
            width=40
        )

        self.cmb_servicio.grid(
            row=1,
            column=1
        )

        tk.Label(
            self.tab_reservas,
            text="Horas"
        ).grid(
            row=2,
            column=0
        )

        self.txt_horas = tk.Entry(
            self.tab_reservas,
            width=42
        )

        self.txt_horas.grid(
            row=2,
            column=1
        )

        tk.Button(
            self.tab_reservas,
            text="Crear Reserva",
            bg="green",
            fg="white",
            command=self.crear_reserva
        ).grid(
            row=3,
            column=0,
            pady=10
        )

        tk.Button(
            self.tab_reservas,
            text="Procesar Reserva",
            bg="blue",
            fg="white",
            command=self.procesar_reserva
        ).grid(
            row=3,
            column=1,
            pady=10
        )

        tk.Button(
            self.tab_reservas,
            text="Cancelar Reserva",
            bg="red",
            fg="white",
            command=self.cancelar_reserva
        ).grid(
            row=3,
            column=2,
            pady=10
        )

        self.tv_reservas = ttk.Treeview(
            self.tab_reservas,
            columns=(
                "codigo",
                "cliente",
                "servicio",
                "estado",
                "valor"
            ),
            show="headings",
            height=15
        )

        self.tv_reservas.heading(
            "codigo",
            text="Código"
        )

        self.tv_reservas.heading(
            "cliente",
            text="Cliente"
        )

        self.tv_reservas.heading(
            "servicio",
            text="Servicio"
        )

        self.tv_reservas.heading(
            "estado",
            text="Estado"
        )

        self.tv_reservas.heading(
            "valor",
            text="Valor"
        )

        self.tv_reservas.grid(
            row=5,
            column=0,
            columnspan=6,
            padx=20,
            pady=20
        )

    # ========================================================
    # CREAR RESERVA
    # ========================================================

    def crear_reserva(self):
        try:

            if self.cmb_cliente.current() == -1:
                raise ReservaError(
                    "Seleccione un cliente"
                )

            if self.cmb_servicio.current() == -1:
                raise ReservaError(
                    "Seleccione un servicio"
                )

            try:
                horas = int(
                    self.txt_horas.get()
                )
            except (TypeError, ValueError) as error:
                raise DatoInvalidoError(
                    "Las horas deben ser un número entero"
                ) from error

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

            reserva.confirmar()

            reservas.append(
                reserva
            )

            self.tv_reservas.insert(
                "",
                tk.END,
                values=(
                    reserva.codigo,
                    cliente.nombre,
                    servicio.nombre,
                    reserva.estado,
                    reserva.calcular_total()
                )
            )

            registrar_log(
                f"Reserva {reserva.codigo} creada"
            )

            self.txt_horas.delete(
                0,
                tk.END
            )

            messagebox.showinfo(
                "Correcto",
                "Reserva registrada"
            )

        except Exception as e:

            registrar_log(
                str(e),
                "error"
            )

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ========================================================
    # PROCESAR RESERVA
    # ========================================================

    def procesar_reserva(self):

        seleccionado = self.tv_reservas.selection()

        if not seleccionado:

            messagebox.showwarning(
                "Aviso",
                "Seleccione una reserva"
            )

            return

        item = seleccionado[0]

        indice = self.tv_reservas.index(
            item
        )

        try:

            reserva = reservas[indice]

            reserva.procesar()

            self.tv_reservas.item(
                item,
                values=(
                    reserva.codigo,
                    reserva.cliente.nombre,
                    reserva.servicio.nombre,
                    reserva.estado,
                    reserva.calcular_total()
                )
            )

            registrar_log(
                f"Reserva {reserva.codigo} procesada"
            )

            messagebox.showinfo(
                "Correcto",
                "Reserva procesada"
            )

        except Exception as e:

            registrar_log(
                str(e),
                "error"
            )

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ========================================================
    # CANCELAR RESERVA
    # ========================================================

    def cancelar_reserva(self):

        seleccionado = self.tv_reservas.selection()

        if not seleccionado:

            messagebox.showwarning(
                "Aviso",
                "Seleccione una reserva"
            )

            return

        item = seleccionado[0]

        indice = self.tv_reservas.index(
            item
        )

        try:

            reserva = reservas[indice]

            reserva.cancelar()

            self.tv_reservas.item(
                item,
                values=(
                    reserva.codigo,
                    reserva.cliente.nombre,
                    reserva.servicio.nombre,
                    reserva.estado,
                    reserva.calcular_total()
                )
            )

            registrar_log(
                f"Reserva {reserva.codigo} cancelada"
            )

            messagebox.showinfo(
                "Correcto",
                "Reserva cancelada"
            )

        except Exception as e:

            registrar_log(
                str(e),
                "error"
            )

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ========================================================
    # ACTUALIZAR COMBOS
    # ========================================================

    def actualizar_combos(self):

        if hasattr(
            self,
            "cmb_cliente"
        ):
            self.cmb_cliente["values"] = [
                cliente.nombre
                for cliente in clientes
            ]

        if hasattr(
            self,
            "cmb_servicio"
        ):
            self.cmb_servicio["values"] = [
                servicio.nombre
                for servicio in servicios
            ]

    # ========================================================
    # LIMPIAR INFORMACIÓN
    # ========================================================

    def limpiar_datos(self):

        clientes.clear()
        servicios.clear()
        reservas.clear()

        for item in self.tv_clientes.get_children():
            self.tv_clientes.delete(item)

        for item in self.tv_servicios.get_children():
            self.tv_servicios.delete(item)

        for item in self.tv_reservas.get_children():
            self.tv_reservas.delete(item)

        self.actualizar_combos()

        registrar_log(
            "Sistema limpiado"
        )

        messagebox.showinfo(
            "Correcto",
            "Información eliminada"
        )

    # ========================================================
    # ACERCA DE
    # ========================================================

    def acerca_de(self):

        messagebox.showinfo(
            "Acerca de",
            "SOFTWARE FJ\n\n"
            "Sistema Integral de Gestión\n"
            "Clientes - Servicios - Reservas\n\n"
            "Autor - Rodolfo Gonzalez Melo\n\n"
            "Curso Programación\n"
            "UNAD - Fase 4\n\n"
            "Desarrollado en Python"
        )

    # ========================================================
    # SALIR
    # ========================================================

    def salir(self):

        respuesta = messagebox.askyesno(
            "Salir",
            "¿Desea cerrar la aplicación?"
        )

        if respuesta:

            registrar_log(
                "Aplicación cerrada"
            )

            self.ventana.destroy()

    # ========================================================
    # 10 OPERACIONES DE PRUEBA
    # ========================================================

    def cargar_datos_prueba(self):
        operaciones = 0
        try:
            clientes.clear()
            servicios.clear()
            reservas.clear()
            Reserva.contador = 1

            for item in self.tv_clientes.get_children():
                self.tv_clientes.delete(item)
            for item in self.tv_servicios.get_children():
                self.tv_servicios.delete(item)
            for item in self.tv_reservas.get_children():
                self.tv_reservas.delete(item)

            c1 = Cliente("Juan Perez", "12345", "juan@gmail.com")
            clientes.append(c1)
            operaciones += 1

            c2 = Cliente("Maria Gomez", "54321", "maria@gmail.com")
            clientes.append(c2)
            operaciones += 1

            s1 = ReservaSala("Sala Ejecutiva", 50000)
            s2 = AlquilerEquipos("Portátiles", 30000)
            s3 = AsesoriaEspecializada("Redes", 80000)
            servicios.extend([s1, s2, s3])
            operaciones += 3

            for cliente in (c1, c2):
                self.tv_clientes.insert(
                    "", tk.END,
                    values=(cliente.nombre, cliente.identificacion, cliente.correo)
                )

            for servicio, tipo in (
                (s1, "Sala"),
                (s2, "Equipos"),
                (s3, "Asesoria"),
            ):
                self.tv_servicios.insert(
                    "", tk.END,
                    values=(servicio.nombre, tipo, servicio.tarifa)
                )

            reserva = Reserva(c1, s1, 2)
            reserva.confirmar()
            reservas.append(reserva)
            operaciones += 1
            self.tv_reservas.insert(
                "", tk.END,
                values=(
                    reserva.codigo,
                    reserva.cliente.nombre,
                    reserva.servicio.nombre,
                    reserva.estado,
                    reserva.calcular_total(descuento=10),
                ),
            )

        except Exception as error:
            registrar_log(f"Fallo al cargar datos válidos: {error}", "error")
            return
        else:
            registrar_log("Seis operaciones válidas creadas")

        operaciones_invalidas = (
            lambda: Cliente("", "111", "correo"),
            lambda: ReservaSala("", -500),
            lambda: Reserva(c1, s1, 0),
        )
        for operacion in operaciones_invalidas:
            try:
                operacion()
            except Exception as error:
                registrar_log(f"Operación inválida controlada: {error}", "error")
            else:
                registrar_log(
                    "Una operación marcada como inválida fue aceptada",
                    "warning"
                )
            finally:
                operaciones += 1

        try:
            reserva.cancelar()
            operaciones += 1
        except Exception as error:
            registrar_log(str(error), "error")
        finally:
            self.actualizar_combos()
            registrar_log(
                f"Prueba finalizada con {operaciones} operaciones simuladas"
            )
            messagebox.showinfo(
                "Pruebas",
                f"Se ejecutaron {operaciones} operaciones."
            )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    registrar_log(
        "Aplicación iniciada"
    )

    root = tk.Tk()

    app = Aplicacion(
        root
    )

    root.mainloop()

    registrar_log(
        "Aplicación finalizada"
    )
