# -------------------------------
# Fase 4 - Sistema Integral de Gestión de Clientes, Servicios y Reservas
# Autor: Rodolfo González Melo
# Curso: Programación - UNAD
# -------------------------------
 
from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk, messagebox
import logging

# =====================================================
# CONFIGURACION DEL LOG
# =====================================================

logging.basicConfig(
    filename="eventos.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =====================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================

class ClienteError(Exception):
    pass

class ServicioError(Exception):
    pass

class ReservaError(Exception):
    pass

# =====================================================
# CLASE ABSTRACTA PERSONA
# =====================================================
class Persona(ABC):

    @abstractmethod
    def mostrar_info(self):
        pass
# =====================================================
# CLIENTE
# =====================================================

class Cliente(Persona):

    def __init__(self, nombre, identificacion, correo):

        if not nombre.strip():
            raise ClienteError(
                "El nombre es obligatorio"
            )

        if not identificacion.isdigit():
            raise ClienteError(
                "La identificación debe ser numérica"
            )

        if len(identificacion) < 5:
            raise ClienteError(
                "La identificación debe tener mínimo 5 dígitos"
            )

        if "@" not in correo:
            raise ClienteError(
                "Correo electrónico inválido"
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

# =====================================================
# SERVICIO ABSTRACTO
# =====================================================

class Servicio(ABC):

    def __init__(self, nombre, tarifa):

        if tarifa <= 0:
            raise ServicioError(
                "La tarifa debe ser mayor a cero"
            )

        self.nombre = nombre
        self.tarifa = tarifa

    @abstractmethod
    def calcular_costo(self, horas):
        pass

    @abstractmethod
    def descripcion(self):
        pass

# =====================================================
# SERVICIOS ESPECIFICOS
# =====================================================

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

# =====================================================
# RESERVA
# =====================================================

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
        total = self.servicio.calcular_costo(
            self.horas
        )
        if descuento > 0:
            total -= total * descuento / 100

        return round(total, 2)

# =====================================================
# LISTAS EN MEMORIA
# =====================================================

clientes = []
servicios = []
reservas = []

# =====================================================
# INTERFAZ GRAFICA
# =====================================================

class Aplicacion:

    def __init__(self, ventana):
        self.ventana = ventana

        self.ventana.title(
            "Software FJ"
        )

        self.ventana.geometry(
            "1200x700"
        )

        self.ventana.resizable(
            False,
            False
        )

        # ==========================================
        # MENU PRINCIPAL
        # ==========================================

        barra_menu = tk.Menu(
            self.ventana
        )

        self.ventana.config(
            menu=barra_menu
        )

        # Archivo
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

        # Herramientas

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

        # Ayuda
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
            self.ventana,
            text="SOFTWARE FJ - SISTEMA DE GESTION",
            font=("Arial", 18, "bold")
        )

        titulo.pack(
            pady=10
        )

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

    # =================================================
    # CLIENTES
    # =================================================

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

        self.nombre_cliente = tk.Entry(
            self.tab_clientes,
            width=35
        )

        self.nombre_cliente.grid(
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

        self.id_cliente = tk.Entry(
            self.tab_clientes,
            width=35
        )

        self.id_cliente.grid(
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

        self.correo_cliente = tk.Entry(
            self.tab_clientes,
            width=35
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
                "id",
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
            padx=10,
            pady=20
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

            self.actualizar_combos()

            self.nombre_cliente.delete(0, tk.END)
            self.id_cliente.delete(0, tk.END)
            self.correo_cliente.delete(0, tk.END)

            logging.info(
                "Cliente registrado"
            )

            messagebox.showinfo(
                "Correcto",
                "Cliente registrado correctamente"
            )

    # =================================================
    # SERVICIOS
    # =================================================

    def crear_tab_servicios(self):
        tk.Label(
            self.tab_servicios,
            text="Nombre del Servicio"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.nombre_servicio = tk.Entry(
            self.tab_servicios,
            width=35
        )

        self.nombre_servicio.grid(
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

        self.tarifa_servicio = tk.Entry(
            self.tab_servicios,
            width=35
        )

        self.tarifa_servicio.grid(
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

        self.tipo_servicio = ttk.Combobox(
            self.tab_servicios,
            values=[
                "Sala",
                "Equipos",
                "Asesoria"
            ],
            state="readonly"
        )

        self.tipo_servicio.grid(
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
            padx=10,
            pady=20
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
                    servicio.tarifa
                )
            )

            self.actualizar_combos()

            self.nombre_servicio.delete(0, tk.END)
            self.tarifa_servicio.delete(0, tk.END)

            logging.info(
                "Servicio registrado"
            )

            messagebox.showinfo(
                "Correcto",
                "Servicio registrado"
            )

    # =================================================
    # RESERVAS
    # =================================================

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
            state="readonly"
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
            state="readonly"
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

        self.horas_reserva = tk.Entry(
            self.tab_reservas
        )

        self.horas_reserva.grid(
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
            text="Cancelar Reserva",
            bg="red",
            fg="white",
            command=self.cancelar_reserva
        ).grid(
            row=3,
            column=1,
            pady=10
        )

        self.tv_reservas = ttk.Treeview(
            self.tab_reservas,
            columns=(
                "cliente",
                "servicio",
                "estado",
                "valor"
            ),
            show="headings",
            height=15
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
            columnspan=5,
            padx=10,
            pady=20
        )

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

            horas = int(
                self.horas_reserva.get()
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
            reservas.append(reserva)
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
                "Proceso de reserva finalizado"
            )

    def cancelar_reserva(self):
        seleccionado = self.tv_reservas.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Aviso",
                "Seleccione una reserva"
            )

            return
        item = seleccionado[0]
        valores = self.tv_reservas.item(
            item,
            "values"
        )

        nuevos = (
            valores[0],
            valores[1],
            "Cancelada",
            valores[3]
        )

        self.tv_reservas.item(
            item,
            values=nuevos
        )

        logging.info(
            "Reserva cancelada"
        )

        messagebox.showinfo(
            "Correcto",
            "Reserva cancelada"
        )

    # =================================================
    # UTILIDADES
    # =================================================

    def actualizar_combos(self):

        if hasattr(self, "cmb_cliente"):
            self.cmb_cliente["values"] = [
                c.nombre for c in clientes
            ]

        if hasattr(self, "cmb_servicio"):
            self.cmb_servicio["values"] = [
                s.nombre for s in servicios
            ]

    def salir_aplicacion(self):

        if messagebox.askyesno(
            "Salir",
            "¿Desea salir de la aplicación?"
        ):

            logging.info(
                "Aplicación cerrada"
            )

            self.ventana.destroy()

    def acerca_de(self):

        messagebox.showinfo(
            "Acerca de",
            "SOFTWARE FJ\n\n"
            "Sistema Integral de Gestión\n"
            "Clientes - Servicios - Reservas\n"
            "Autor: Rodolfo González Melo\n"
            "Curso: Programación - UNAD\n"
            "Desarrollado en Python con Tkinter\n\n"
        )

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

        logging.info(
            "Información eliminada"
        )

        messagebox.showinfo(
            "Correcto",
            "Datos eliminados"
        )

    def cargar_datos_prueba(self):

        try:
            c1 = Cliente(
                "Juan Perez",
                "12345",
                "juan@gmail.com"
            )

            c2 = Cliente(
                "Maria Gomez",
                "54321",
                "maria@gmail.com"
            )

            clientes.extend([c1, c2])

            s1 = ReservaSala(
                "Sala Ejecutiva",
                50000
            )

            s2 = AlquilerEquipos(
                "Portatiles",
                25000
            )

            s3 = AsesoriaEspecializada(
                "Redes",
                80000
            )

            servicios.extend(
                [s1, s2, s3]
            )

            self.tv_clientes.insert(
                "",
                tk.END,
                values=(
                    c1.nombre,
                    c1.identificacion,
                    c1.correo
                )
            )

            self.tv_clientes.insert(
                "",
                tk.END,
                values=(
                    c2.nombre,
                    c2.identificacion,
                    c2.correo
                )
            )

            self.tv_servicios.insert(
                "",
                tk.END,
                values=(
                    s1.nombre,
                    "Sala",
                    s1.tarifa
                )
            )

            self.tv_servicios.insert(
                "",
                tk.END,
                values=(
                    s2.nombre,
                    "Equipos",
                    s2.tarifa
                )
            )

            self.tv_servicios.insert(
                "",
                tk.END,
                values=(
                    s3.nombre,
                    "Asesoria",
                    s3.tarifa
                )
            )

            self.actualizar_combos()

            logging.info(
                "Datos de prueba cargados"
            )

            messagebox.showinfo(
                "Correcto",
                "Datos de prueba cargados"
            )

        except Exception as e:
            logging.error(
                str(e)
            )

    # =================================================
    # FINALIZAR CONSTRUCCIÓN
    # =================================================
        self.crear_tab_servicios()
        self.crear_tab_reservas()

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    logging.info(
        "Aplicación iniciada"
    )

    root = tk.Tk()

    app = Aplicacion(root)

    app.crear_tab_servicios()
    app.crear_tab_reservas()

    root.mainloop()

    logging.info(
        "Aplicación finalizada"
    )        
