import json
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import messagebox, Toplevel, filedialog , simpledialog
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def CargarArchivo(NombreArchivo):
    try:
        with open(NombreArchivo, "r") as Archivo:
            return json.load(Archivo)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("Error", f"Error al leer el archivo: {e}")
        return []

def PantallaAdministrador():
    global ventanaAdministrador
    ventanaAdministrador = ctk.CTk()
    ventanaAdministrador.geometry("500x600")
    ventanaAdministrador.title("El ANDEN - Administracion")
    ventanaAdministrador.resizable(False, False)
    ventanaAdministrador.attributes("-fullscreen", False)
    ventanaAdministrador.configure(fg_color="black")

def BotonesAdministrador():
    texto = ctk.CTkLabel(
                ventanaAdministrador,
                text="Administrador",
                text_color="white",
                width=150,
                height=100,
                font=("Lalezar", 50),
                anchor=ctk.W,
                justify='left'
            )
    texto.place(x=100, y=5)

    BotonDisponibilidad = ctk.CTkButton(
        ventanaAdministrador,
        text="Lugares Restaurante",
        command=VerDisponibilidad,
        border_width=2,
        border_color="#2FB166",
        font=("Lalezar", 20),
        width=200,
        height=20,
        fg_color="black",
        corner_radius=50,
        hover_color="black"
    )
    BotonDisponibilidad.place(x=150, y=100)

    BotonCanchas = ctk.CTkButton(
        ventanaAdministrador,
        text="Ver Canchas", 
        command=SeleccionDeporte,
        border_width=2,
        border_color="#2FB166",
        font=("Lalezar", 20),
        width=200,
        height=20,
        fg_color="black",
        corner_radius=50,
        hover_color="black"
    )
    BotonCanchas.place(x=150, y=150)

    BotonPreciosCanchas = ctk.CTkButton(
        ventanaAdministrador,
        text="Precios Canchas",
        command=GestionarPreciosCanchas,
        border_width=2,
        border_color="#2FB166",
        font=("Lalezar", 20),
        width=200,
        height=20,
        fg_color="black",
        corner_radius=50,
        hover_color="black"
    )
    BotonPreciosCanchas.place(x=150, y=200)

    BotonVerReservas = ctk.CTkButton(
        ventanaAdministrador,
        text="Ver Reservas",
        command=lambda:SeleccionTipoReserva("Ver"),
        border_width=2,
        border_color="#2FB166",
        font=("Lalezar", 20),
        width=200,
        height=20,
        fg_color="black",
        corner_radius=50,
        hover_color="black"
    )
    BotonVerReservas.place(x=150, y=250)

    BotonEliminarReservas = ctk.CTkButton(
        ventanaAdministrador,
        text="Eliminar Reserva",
        command=lambda:SeleccionTipoReserva("Cancelar"),
        border_width=2,
        border_color="#2FB166",
        font=("Lalezar", 20),
        width=200,
        height=20,
        fg_color="black",
        corner_radius=50,
        hover_color="black"
    )
    BotonEliminarReservas.place(x=150, y=300)

    BotonGestionarMenu = ctk.CTkButton(
        ventanaAdministrador,
        text="Gestionar Menu",
        command=GestionarMenu,
        border_width=2,
        border_color="#2FB166",
        font=("Lalezar", 20),
        width=200,
        height=20,
        fg_color="black",
        corner_radius=50,
        hover_color="black"
    )
    BotonGestionarMenu.place(x=150, y=350)

def Administrador():
    PantallaAdministrador()
    BotonesAdministrador()

def EnviarMail(Destinatario , CuerpoMensaje , Asunto):
    EmailRemitente = "elandenreservas@gmail.com"
    EmailDestinatario = Destinatario
    Contraseña = "lgug poom mjsz wrhj"
    Mensaje = MIMEMultipart()
    Mensaje["From"] = EmailRemitente
    Mensaje["To"] = EmailDestinatario
    Mensaje["Subject"] = Asunto
    Cuerpo = CuerpoMensaje
   
    Mensaje.attach(MIMEText(Cuerpo, "plain"))
    try:
        if EmailDestinatario == "":
            messagebox.showerror("ERROR", "No registraste ningun mail")
        else:
            servidor_smtp = smtplib.SMTP("smtp.gmail.com", 587)
            servidor_smtp.starttls() 
            servidor_smtp.login(EmailRemitente, Contraseña)
            texto_mensaje = Mensaje.as_string()
            servidor_smtp.sendmail(EmailRemitente, EmailDestinatario, texto_mensaje)
            servidor_smtp.quit()
            messagebox.showinfo("Exito", "Correo enviado con éxito.")
    except Exception as e:
        messagebox.showerror("ERROR" , f"Error al enviar el correo: {e}")

def SeleccionTipoReserva(DestinoReserva):
    global ventanaSeleccion
    ventanaSeleccion = Toplevel(ventanaAdministrador)
    ventanaSeleccion.title("Tipo de Reserva")
    ventanaSeleccion.geometry("200x300")
    ventanaSeleccion.resizable(False, False)
    ventanaSeleccion.transient(ventanaAdministrador)  
    ventanaSeleccion.lift()  
    ventanaSeleccion.focus_set()  
    ventanaSeleccion.grab_set()
    ventanaSeleccion.configure(background="black")

    Funcion = {"Cancelar": EliminarReserva, "Ver": VerReservas}.get(DestinoReserva)
    if Funcion is None:
        messagebox.showerror("ERROR", "Acción de reserva no válida.")
        return


    texto = ctk.CTkLabel(
        ventanaSeleccion,
        text="Seleccione el Tipo de Reserva",
        text_color="white",
        width=100,
        height=20,
        font=("Lalezar", 15),
        anchor="center",
        justify='center'
    )
    texto.pack(pady=20)

    BotonCanchas = ctk.CTkButton(
        ventanaSeleccion, 
        text="Canchas", 
        width=150, 
        height=50,  
        command=lambda: Funcion("Canchas"), 
        fg_color="#2FB166", 
        text_color="white"
    )
    BotonCanchas.pack(pady=20)

    BotonRestaurante = ctk.CTkButton(
        ventanaSeleccion, 
        text="Restaurante", 
        width=150, 
        height=50,  
        command=lambda: Funcion("Restaurante"), 
        fg_color="#2FB166", 
        text_color="white"
    )
    BotonRestaurante.pack(pady=20)

def CargarDatosJSON():
    try:
        with open(ArchivoJSON, 'r') as archivo:
            return json.load(archivo)
    except FileNotFoundError:

        return [
            {
                "Lunes": {"Lugares Disponibles": 50, "Lugares Ocupados": 0},
                "Martes": {"Lugares Disponibles": 50, "Lugares Ocupados": 0},
                "Miercoles": {"Lugares Disponibles": 50, "Lugares Ocupados": 0},
                "Jueves": {"Lugares Disponibles": 50, "Lugares Ocupados": 0},
                "Viernes": {"Lugares Disponibles": 50, "Lugares Ocupados": 0},
                "Sabado": {"Lugares Disponibles": 50, "Lugares Ocupados": 0},
                "Domingo": {"Lugares Disponibles": 50, "Lugares Ocupados": 0}
            }
        ]

def GuardarDatosJSON(datos):
    with open(ArchivoJSON, 'w') as archivo:
        json.dump(datos, archivo, indent=4)

def PantallaReservas():
    global ventanaReservas
    ventanaReservas = Toplevel(ventanaAdministrador)
    ventanaReservas.title("Reservas")
    ventanaReservas.geometry("950x650")
    ventanaReservas.resizable(False, False)
    ventanaReservas.attributes("-fullscreen", False)
    ventanaReservas.configure(background="black")

def TablaReservas():
    global FrameTablaReservas
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview.Heading", background="#2FB166", foreground="black")
    style.configure(
        "Custom.Treeview", 
        background="black",
        foreground="white",
        fieldbackground="black",
        highlightthickness=0,
        highlightbackground="black", 
        bd=1,
        relief="solid"
    )
    style.map("Custom.Treeview", background=[("selected", "#2FB166")])

    FrameTablaReservas = ctk.CTkFrame(ventanaReservas, fg_color="black")
    FrameTablaReservas.pack(fill="both", expand=True)

    tree = ttk.Treeview(FrameTablaReservas, style="Custom.Treeview")
    tree.pack(fill="both", expand=True, side="left")

    scrollbar = ttk.Scrollbar(FrameTablaReservas, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

def FramesReservas():
    global FrameBusquedaReservas
    FrameBusquedaReservas = ctk.CTkFrame(ventanaReservas, fg_color="black", bg_color="black")
    FrameBusquedaReservas.pack(pady=10, fill="x", side="bottom")

def LeerReservasJSON(ArchivoJSON):
    try:
        with open(ArchivoJSON, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)
        return pd.DataFrame(data)
    except FileNotFoundError:
        messagebox.showerror("ERROR" , f" El archivo {ArchivoJSON} no fue encontrado.")
        return pd.DataFrame()
    except json.JSONDecodeError:
        messagebox.showerror("ERROR" , "El archivo no es un JSON válido.")
        return pd.DataFrame()

def MostrarDatosReservas(df):
    for widget in FrameTablaReservas.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(FrameTablaReservas, style="Custom.Treeview")
    tree.pack(fill="both", expand=True, side="left")

    scrollbar = ttk.Scrollbar(FrameTablaReservas, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    AnchoColumnass = {
        "Numero Reserva": 30,
        "Deporte": 20,
        "Cancha": 50,
        "Nombre": 20,
        "Gmail": 600,
        "Dia": 20,
        "Horario": 20,
        "Precio": 20,
        "Estado": 30,
    }

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=AnchoColumnass.get(col, 100), anchor="center")

    tree.tag_configure("data_row", background="black", foreground="white")

    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row), tags=("data_row",))

def BuscarReserva():
    NumeroReserva = BuscarNumero.get()
    Cancha = BuscarCancha.get()
    Dia = BuscarDia.get()
    Deporte = BuscarDeporte.get()
    Mail = BuscarMail.get()
    Estado = BuscarEstado.get()

    resultado = HojasReservas
    if NumeroReserva:
        resultado = resultado[resultado['Numero Reserva'].astype(str) == NumeroReserva]
    if Cancha:
        resultado = resultado[resultado['Cancha'].str.contains(Cancha, case=False)]
    if Dia:
        resultado = resultado[resultado['Dia'].str.contains(Dia, case=False)]
    if Deporte:
        resultado = resultado[resultado['Deporte'].str.contains(Deporte, case=False)]
    if Mail:
        resultado = resultado[resultado['Mail'].str.contains(Mail, case=False)]
    if Estado:
        resultado = resultado[resultado['Estado'].str.contains(Estado, case=False)]
    
    MostrarDatosReservas(resultado)

def VerReservas(TipoReservaSeleccionado):
    global HojasReservas, FrameBusquedaReservas, FrameTablaReservas
    if TipoReservaSeleccionado is None:
        messagebox.showerror("ERROR", "Debe seleccionar un tipo de reserva.")
        return
    ventanaSeleccion.destroy()
    if TipoReservaSeleccionado == "Canchas":
        NombreArchivoReservas = "src/JSON/Reservas.json"
    elif TipoReservaSeleccionado == "Restaurante":
        NombreArchivoReservas = "src/JSON/ReservasRestaurante.json"
    PantallaReservas()
    TablaReservas()
    FramesReservas()
    HojasReservas = LeerReservasJSON(NombreArchivoReservas)

    if not HojasReservas.empty:
        MostrarDatosReservas(HojasReservas)
    else:
        messagebox.showerror("ERROR" , "No hay datos disponibles.")

    global BuscarDeporte, BuscarCancha, BuscarDia, BuscarNumero, BuscarMail, BuscarEstado
    BuscarNumero = ctk.CTkEntry(
        FrameBusquedaReservas, 
        width=125,
        height=30,  
        placeholder_text="Número de Reserva",
        placeholder_text_color="white",
        text_color="white",
        border_width=2,
        border_color="#2FB166",
        fg_color="#2FB166"
    )
    BuscarNumero.pack(side="left", padx=10)

    BuscarDeporte = ctk.CTkEntry(
        FrameBusquedaReservas, 
        width=125, 
        height=30,
        placeholder_text="Deporte", 
        placeholder_text_color="white", 
        text_color="white", 
        border_width=2, 
        border_color="#2FB166", 
        fg_color="#2FB166"
    )
    BuscarDeporte.pack(side="left", padx=10)

    BuscarDia = ctk.CTkEntry(
        FrameBusquedaReservas, 
        width=125,
        height=30, 
        placeholder_text="Dia",
        placeholder_text_color="white",
        text_color="white",
        border_width=2,
        border_color="#2FB166",
        fg_color="#2FB166"
    )
    BuscarDia.pack(side="left", padx=10)

    BuscarCancha = ctk.CTkEntry(
        FrameBusquedaReservas, 
        width=125,
        height=30, 
        placeholder_text="Cancha",
        placeholder_text_color="white",
        text_color="white",
        border_width=2,
        border_color="#2FB166",
        fg_color="#2FB166"
    )
    BuscarCancha.pack(side="left", padx=10)

    BuscarMail = ctk.CTkEntry(
        FrameBusquedaReservas, 
        width=125,
        height=30, 
        placeholder_text="Mail",
        placeholder_text_color="white",
        text_color="white",
        border_width=2,
        border_color="#2FB166",
        fg_color="#2FB166"
    )
    BuscarMail.pack(side="left", padx=10)

    BuscarEstado = ctk.CTkEntry(
        FrameBusquedaReservas, 
        width=125,
        height=30, 
        placeholder_text="Estado",
        placeholder_text_color="white",
        text_color="white",
        border_width=2,
        border_color="#2FB166",
        fg_color="#2FB166"
    )
    BuscarEstado.pack(side="left", padx=10)

    if NombreArchivoReservas == "src/JSON/ReservasRestaurante.json":
        BuscarCancha.pack_forget()
        BuscarDeporte.pack_forget()
        BuscarEstado.pack_forget()

    BotonBuscar = ctk.CTkButton(
        FrameBusquedaReservas, 
        text="Buscar", 
        width=175,
        height=30,  
        command=BuscarReserva, 
        fg_color="#2FB166", 
        text_color="white"
    )
    BotonBuscar.pack(side="left", padx=10)
    ventanaReservas.mainloop()

def VentanaTexto():
    global PestañaTexto, EntradaTexto, TextoIngresado
    TextoIngresado = None
    PestañaTexto = Toplevel(ventanaAdministrador)
    PestañaTexto.geometry("400x150")
    PestañaTexto.title("Texto")
    PestañaTexto.resizable(False, False)
    PestañaTexto.configure(background="black")
    
    EntradaTexto = ctk.CTkEntry(
        PestañaTexto,
        width=300,
        height=50,
        font=("Lalezar", 20),
        placeholder_text=f"Ingrese el Numero de Reserva",
        fg_color="white",
        corner_radius=10,
        border_color="white",
        text_color="Black"
    )
    EntradaTexto.place(x=50, y=25)

    def confirmar_y_cerrar():
        global TextoIngresado
        TextoIngresado = EntradaTexto.get()
        PestañaTexto.destroy()
    
    BotonConfirmar = ctk.CTkButton(
        PestañaTexto, 
        command=confirmar_y_cerrar,
        text="Confirmar",
        width=100,
        height=25,
        fg_color="#2FB166",
        font=("Lalezar", 15),
        corner_radius=10,
        hover_color="#2FB166"
    )
    BotonConfirmar.place(x=150, y=100)
    
    PestañaTexto.wait_window()

def ObtenerMailUsuario():
    global MailUsuario
    with open(NombreArchivoReservas, 'r') as file:
        Reservas = json.load(file)
    for reserva in Reservas:
        for Clave , Valor in reserva.items():
            if Clave == "Numero Reserva":
                if Valor == NumeroIngresado:
                    for Clave , Valor in reserva.items():
                        if Clave == "Mail":
                            MailUsuario = Valor

def EliminarReserva(TipoReservaSeleccionado):
    global NumeroIngresado , NombreArchivoReservas
    if TipoReservaSeleccionado is None:
        messagebox.showerror("ERROR", "Debe seleccionar un tipo de reserva.")
        return
    ventanaSeleccion.destroy()
    if TipoReservaSeleccionado == "Canchas":
        NombreArchivoReservas = "src/JSON/Reservas.json"
    elif TipoReservaSeleccionado == "Restaurante":
        NombreArchivoReservas = "src/JSON/ReservasRestaurante.json"    
    
    VentanaTexto()

    if TextoIngresado is not None:
        NumeroIngresado = TextoIngresado
        ObtenerMailUsuario()
        ReestablecerDatosReserva(NumeroIngresado)
        mensaje = (f"Su reserva de numero {NumeroIngresado} a sido eliminada por El Admin")
        EnviarMail(MailUsuario , mensaje , "Reserva Eliminada")
        messagebox.showinfo("Exito" , "Reserva eliminada exitosamente")
    else:
        messagebox.showerror("ERROR" , "Número de reserva no encontrado")
            
def ReestablecerDatosReserva(NumeroIngresado):
    global ArchivoJSON
    try:
        with open(NombreArchivoReservas, 'r') as file:
            ArchivoReservas = json.load(file)

        if NombreArchivoReservas == "src/JSON/Reservas.json":
            for reserva in ArchivoReservas:
                if reserva['Numero Reserva'] == str(NumeroIngresado):
                    DeporteReserva = reserva['Deporte']
                    DiaReserva = reserva['Dia']
                    HorarioReserva = reserva['Horario']
                    CanchaReserva = reserva['Cancha']
                    ArchivoDeporte = DeporteReserva + ".json"
                    with open(ArchivoDeporte, 'r') as file:
                        Archivo = json.load(file)

                    for Datos in Archivo:
                        for Cancha, Dias in Datos.items():
                            if Cancha == CanchaReserva:
                                for Dia, Horarios in Dias.items():
                                    if Dia == DiaReserva:
                                        for Horario, Estado in Horarios.items():
                                            if Horario == HorarioReserva and Estado == "Reservada":
                                                Horarios[Horario] = "Disponible"
                                                messagebox.showinfo("Exito" , f"El estado de la {CanchaReserva} de {DeporteReserva}, el dia {DiaReserva} a las {HorarioReserva} ha sido cambiado a 'Disponible'")
                    with open(ArchivoDeporte, 'w') as file:
                        json.dump(Archivo, file, indent=4)
        if NombreArchivoReservas == "ReservasRestaurante.json":
             for reserva in ArchivoReservas:
                if reserva['Numero Reserva'] == str(NumeroIngresado):
                    DiaReserva = reserva['Dia']
                    CantidadComensales = reserva['Numero de comensales']
                    ArchivoJSON = 'src/JSON/Restaurante.json'
                    DiasData = CargarDatosJSON()[0]
                    DiasData[DiaReserva]["Lugares Disponibles"] += CantidadComensales
                    DiasData[DiaReserva]["Lugares Ocupados"] -= CantidadComensales
                    GuardarDatosJSON([DiasData])
        ArchivoReservas = [reserva for reserva in ArchivoReservas if reserva['Numero Reserva'] != NumeroIngresado]
        with open(NombreArchivoReservas, 'w') as f:
            json.dump(ArchivoReservas, f, indent=4)


    except FileNotFoundError:
        messagebox.showerror("ERROR" ,"El archivo no se encontró. Verifica la ruta del archivo.")
    except json.JSONDecodeError:
        messagebox.showerror("ERROR" ,"Error al decodificar el archivo JSON. Asegúrate de que el formato sea correcto.")
    except KeyError as e:
        messagebox.showerror("ERROR" ,f"Error de clave: {e}. Asegúrate de que la clave existe en el archivo JSON.")
    except Exception as e:
        messagebox.showerror("ERROR" ,f"Ocurrió un error inesperado: {e}")

def PantallaCanchas(Deporte):
    global ventanaCanchas
    ventanaCanchas = Toplevel(ventanaAdministrador)
    ventanaCanchas.title(f"Canchas {Deporte}")
    ventanaCanchas.geometry("950x650")
    ventanaCanchas.resizable(False, False)
    ventanaCanchas.attributes("-fullscreen", False)
    ventanaCanchas.configure(background="black")

def LeerCanchasJSON(ArchivoJSON):
    try:
        with open(ArchivoJSON, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)
        return data
    except FileNotFoundError:
        messagebox.showerror("ERROR" , f" El archivo {ArchivoJSON} no fue encontrado.")
        return {}
    except json.JSONDecodeError:
        messagebox.showerror("ERROR" , "El archivo no es un JSON válido.")
        return {}

def ProcesarCanchas(data):
    filas = []

    for info in data:
        for cancha, dias in info.items():
            for dia, horarios in dias.items():
                for hora, estado in horarios.items():
                    fila = {
                        "Cancha": cancha,
                        "Dia": dia,
                        "Horario": hora,
                        "Estado": estado
                    }
                    filas.append(fila)

    return pd.DataFrame(filas)

def TablaCanchas():
    global FrameTablaCanchas
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview.Heading", background="#2FB166", foreground="black")
    style.configure(
        "Custom.Treeview", 
        background="black",
        foreground="white",
        fieldbackground="black",
        highlightthickness=0,
        highlightbackground="black", 
        bd=1,
        relief="solid"
    )
    style.map("Custom.Treeview", background=[("selected", "#2FB166")])

    FrameTablaCanchas = ctk.CTkFrame(ventanaCanchas, fg_color="black")
    FrameTablaCanchas.pack(fill="both", expand=True)

    tree = ttk.Treeview(FrameTablaCanchas, style="Custom.Treeview")
    tree.pack(fill="both", expand=True, side="left")

    scrollbar = ttk.Scrollbar(FrameTablaCanchas, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

def FramesCanchas():
    global FrameBusquedaCanchas
    FrameBusquedaCanchas = ctk.CTkFrame(ventanaCanchas, fg_color="black", bg_color="black")
    FrameBusquedaCanchas.pack(pady=10, fill="x", side="bottom")

def MostrarDatosCanchas(df):
    # Limpiar la tabla actual
    for widget in FrameTablaCanchas.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(FrameTablaCanchas, style="Custom.Treeview")
    tree.pack(fill="both", expand=True, side="left")

    scrollbar = ttk.Scrollbar(FrameTablaCanchas, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    tree["columns"] = ["Cancha", "Dia", "Horario", "Estado"]
    tree["show"] = "headings"

    AnchoColumnas = {
        "Cancha": 30,
        "Dia": 20,
        "Horario": 50,
        "Estado": 20,
    }

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=AnchoColumnas.get(col, 100), anchor="center")

    tree.tag_configure("data_row", background="black", foreground="white")

    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row), tags=("data_row",))

def FiltrarCanchas():
    Cancha = BuscarCancha.get()
    Dia = BuscarDia.get()
    Estado = BuscarEstado.get()
    Horario = BuscarHorario.get()

    resultado = HojasCanchas
    if Cancha:
        resultado = resultado[resultado['Cancha'].str.contains(Cancha, case=False)]
    if Dia:
        resultado = resultado[resultado['Dia'].str.contains(Dia, case=False)]
    if Estado:
        resultado = resultado[resultado['Estado'].str.contains(Estado, case=False)]
    if Horario:
        resultado = resultado[resultado['Horario'].str.contains(Horario, case=False)]
        
    MostrarDatosCanchas(resultado)

def VerCanchas(Deporte):
    global HojasCanchas, FrameBusquedaCanchas, FrameTablaCanchas
    ventanaSeleccion.destroy()
    PantallaCanchas(Deporte)
    TablaCanchas()
    FramesCanchas()
    ArchivoJSON = "src/JSON/" + Deporte + ".json"
    data = LeerCanchasJSON(ArchivoJSON)

    if data:
        HojasCanchas = ProcesarCanchas(data)
        MostrarDatosCanchas(HojasCanchas)
    else:
        messagebox.showerror("ERROR" , "No hay datos disponibles.")

    global BuscarCancha, BuscarDia, BuscarEstado , BuscarHorario
    BuscarDia = ctk.CTkEntry(
        FrameBusquedaCanchas, 
        width=125,
        height=30, 
        placeholder_text="Dia",
        placeholder_text_color="white",
        text_color="white",
        border_width=2,
        border_color="#2FB166",
        fg_color="#2FB166"
    )
    BuscarDia.pack(side="left", padx=10)

    BuscarCancha = ctk.CTkEntry(
        FrameBusquedaCanchas, 
        width=125,
        height=30, 
        placeholder_text="Cancha",
        placeholder_text_color="white",
        text_color="white",
        border_width=2,
        border_color="#2FB166",
        fg_color="#2FB166"
    )
    BuscarCancha.pack(side="left", padx=10)

    BuscarHorario = ctk.CTkEntry(
        FrameBusquedaCanchas, 
        width=125,
        height=30, 
        placeholder_text="Horario",
        placeholder_text_color="white",
        text_color="white",
        border_width=2,
        border_color="#2FB166",
        fg_color="#2FB166"
    )
    BuscarHorario.pack(side="left", padx=10)


    BuscarEstado = ctk.CTkEntry(
        FrameBusquedaCanchas, 
        width=125,
        height=30, 
        placeholder_text="Estado",
        placeholder_text_color="white",
        text_color="white",
        border_width=2,
        border_color="#2FB166",
        fg_color="#2FB166"
    )
    BuscarEstado.pack(side="left", padx=10)

    BotonBuscar = ctk.CTkButton(
        FrameBusquedaCanchas, 
        text="Buscar", 
        width=175,
        height=30,  
        command=FiltrarCanchas, 
        fg_color="#2FB166", 
        text_color="white"
    )
    BotonBuscar.pack(side="left", padx=10)
    ventanaCanchas.mainloop()
    
def SeleccionDeporte():
    global ventanaSeleccion
    ventanaSeleccion = Toplevel(ventanaAdministrador)
    ventanaSeleccion.title("Seleccionar Deporte")
    ventanaSeleccion.geometry("400x300")
    ventanaSeleccion.resizable(False, False)
    ventanaSeleccion.configure(background="black")

    BotonFutbol = ctk.CTkButton(
        ventanaSeleccion, 
        text="Futbol", 
        width=150, 
        height=50,  
        command=lambda: VerCanchas("Futbol"), 
        fg_color="#2FB166", 
        text_color="white"
    )
    BotonFutbol.pack(pady=20)

    BotonTenis = ctk.CTkButton(
        ventanaSeleccion, 
        text="Tenis", 
        width=150, 
        height=50,  
        command=lambda: VerCanchas("Tenis"), 
        fg_color="#2FB166", 
        text_color="white"
    )
    BotonTenis.pack(pady=20)

    BotonPadel = ctk.CTkButton(
        ventanaSeleccion, 
        text="Padel", 
        width=150, 
        height=50,  
        command=lambda: VerCanchas("Padel"), 
        fg_color="#2FB166", 
        text_color="white"
    )
    BotonPadel.pack(pady=20)
    ventanaSeleccion.mainloop()

def LeerPreciosJSON(ArchivoJSON):
    try:
        with open(ArchivoJSON, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)
        return data[0] 
    except FileNotFoundError:
        messagebox.showerror("ERROR" , f" El archivo {ArchivoJSON} no fue encontrado.")
        return {}
    except json.JSONDecodeError:
        messagebox.showerror("ERROR" , "El archivo no es un JSON válido.")
        return {}

def MostrarTablaDePrecios(data):
    global FrameTablaPrecios
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview.Heading", background="#2FB166", foreground="black")
    style.configure(
        "Custom.Treeview", 
        background="black",
        foreground="white",
        fieldbackground="black",
        highlightthickness=0,
        highlightbackground="black", 
        bd=1,
        relief="solid"
    )
    style.map("Custom.Treeview", background=[("selected", "#2FB166")])

    for widget in FrameTablaPrecios.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(FrameTablaPrecios, style="Custom.Treeview")
    tree.pack(fill="both", expand=True, side="left")

    tree["columns"] = ["Deporte", "Dia", "Noche"]
    tree["show"] = "headings"

    AnchoColumnass = {
        "Deporte": 100,
        "Dia": 100,
        "Noche": 100,
    }

    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=AnchoColumnass.get(col, 100), anchor="center")

    for cancha, precios in data.items():
        tree.insert("", "end", values=(cancha, precios["Dia"], precios["Noche"]))

    tree.bind("<Double-1>", lambda event, tree=tree, data=data: EditarPrecio(event, tree, data))

def EditarPrecio(event, tree, data):
    item = tree.selection()[0]
    col = tree.identify_column(event.x)
    col = col.split("#")[-1]
    col = int(col) - 1

    if col > 0:
        PrecioActual = tree.item(item, "values")[col]
        cancha = tree.item(item, "values")[0]

        PrecioNuevo = simpledialog.askstring("Editar Precio", f"Nuevo precio para {cancha} ({'Día' if col == 1 else 'Noche'}):", initialvalue=PrecioActual)

        if PrecioNuevo:
            tree.item(item, values=(cancha, PrecioNuevo if col == 1 else tree.item(item, "values")[1], PrecioNuevo if col == 2 else tree.item(item, "values")[2]))
            
            
            if col == 1:
                data[cancha]["Dia"] = int(PrecioNuevo)
            else:
                data[cancha]["Noche"] = int(PrecioNuevo)

            with open("src/JSON/precios.json", "w", encoding="utf-8") as archivo:
                json.dump([data], archivo, ensure_ascii=False, indent=4)

def PantallaPrecios():
    global ventanaPrecios, FrameTablaPrecios , FrameTextoPrecios
    ventanaPrecios = Toplevel(ventanaAdministrador)
    ventanaPrecios.title("Precios")
    ventanaPrecios.geometry("500x500")
    ventanaPrecios.resizable(False, False)
    ventanaPrecios.configure(background="black")

    FrameTablaPrecios = ctk.CTkFrame(ventanaPrecios, fg_color="black")
    FrameTablaPrecios.pack(fill="both", expand=True)
    
    tree = ttk.Treeview(FrameTablaPrecios, style="Custom.Treeview")
    tree.pack(fill="both", expand=True, side="left")
    
    scrollbar = ttk.Scrollbar(FrameTablaPrecios, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)
    
    FrameTextoPrecios = ctk.CTkFrame(ventanaPrecios, fg_color="black" , bg_color="black")
    FrameTextoPrecios.pack(fill="x", side="bottom", pady=10)

def GestionarPreciosCanchas():
    PantallaPrecios()
    data = LeerPreciosJSON("precios.json")
    if data:
        MostrarTablaDePrecios(data)
    else:
        messagebox.showerror("ERROR" , "No hay datos de precios disponibles.")

    texto = ctk.CTkLabel(
        FrameTextoPrecios,
        text="Doble clic para modificar el precio de las canchas",
        text_color="white",
        width=100,
        height=20,
        font=("Lalezar", 20),
        anchor="center",
        justify='center'
    )
    texto.pack()

    ventanaPrecios.mainloop()

def LeerMenuJSON(ArchivoJSON):
    try:
        with open(ArchivoJSON, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)
        return data[0]
    except FileNotFoundError:
        messagebox.showerror("ERROR" , f"El archivo {ArchivoJSON} no fue encontrado.")
        return {}
    except json.JSONDecodeError:
        messagebox.showerror("ERROR" , "El archivo no es un JSON válido.")
        return {}

def GuardarMenuJSON(data, ArchivoJSON="menu.json"):
    try:
        with open(ArchivoJSON, "w", encoding="utf-8") as archivo:
            json.dump([data], archivo, ensure_ascii=False, indent=4)
    except Exception as e:
        messagebox.showerror("ERROR" , f"Error al guardar el archivo JSON: {e}")

def MostrarTablaDeMenu(data, tipo="Todos"):
    global FrameTablaMenu, tree
    
    for widget in FrameTablaMenu.winfo_children():
        widget.destroy()

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview.Heading", background="#2FB166", foreground="black")
    style.configure(
        "Custom.Treeview", 
        background="black",
        foreground="white",
        fieldbackground="black",
        highlightthickness=0,
        highlightbackground="black", 
        bd=1,
        relief="solid"
    )
    style.map("Custom.Treeview", background=[("selected", "#2FB166")])

    tree = ttk.Treeview(FrameTablaMenu, style="Custom.Treeview")
    tree.pack(fill="both", expand=True, side="left")

    tree["columns"] = ["Tipo", "Producto", "Precio"]
    tree["show"] = "headings"

    AnchoColumnas = {
        "Tipo": 100,
        "Producto": 200,
        "Precio": 100,
    }

    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=AnchoColumnas.get(col, 100), anchor="center")

    productos_a_mostrar = []
    if tipo == "Todos":
        for categoria, productos in data.items():
            for producto, precio in productos.items():
                productos_a_mostrar.append((categoria, producto, precio))
    else:
        productos = data.get(tipo, {})
        for producto, precio in productos.items():
            productos_a_mostrar.append((tipo, producto, precio))

    for tipo, producto, precio in productos_a_mostrar:
        tree.insert("", "end", values=(tipo, producto, precio))

    tree.bind("<Double-1>", lambda event, tree=tree, data=data: EditarPrecioMenu(event, tree, data))


def EditarPrecioMenu(event, tree, data):
    item = tree.selection()[0]
    col = tree.identify_column(event.x)
    col = col.split("#")[-1]
    col = int(col) - 1

    if col == 2:
        producto = tree.item(item, "values")[1]
        tipo = tree.item(item, "values")[0]
        PrecioActual = tree.item(item, "values")[2]

        PrecioNuevo = simpledialog.askstring("Editar Precio", f"Nuevo precio para {producto} ({tipo}):", initialvalue=PrecioActual)

        if PrecioNuevo:
            tree.item(item, values=(tipo, producto, PrecioNuevo))
            for categoria, productos in data.items():
                if tipo == categoria and producto in productos:
                    productos[producto] = int(PrecioNuevo)

            GuardarMenuJSON(data)

def AgregarProducto(data):
    tipo = simpledialog.askstring("Nuevo Producto", "Ingrese el tipo de comida (Entradas, Principal, Bebidas, Postres):")
    if tipo not in data:
        messagebox.showerror("ERROR" , "Tipo no válido.")
        return

    producto = simpledialog.askstring("Nuevo Producto", "Ingrese el nombre del nuevo producto:")
    precio = simpledialog.askstring("Nuevo Producto", "Ingrese el precio del nuevo producto:")

    try:
        precio = int(precio)
    except ValueError:
        messagebox.showerror("ERROR" , "Precio no válido.")
        return

    data[tipo][producto] = precio

    MostrarTablaDeMenu(data)
    GuardarMenuJSON(data)

def PantallaMenu():
    global ventanaMenu, FrameTablaMenu, tree , FrameBusquedaMenu
    ventanaMenu = Toplevel(ventanaAdministrador)
    ventanaMenu.title("Menú de Precios")
    ventanaMenu.geometry("800x600")
    ventanaMenu.resizable(False, False)
    ventanaMenu.attributes("-fullscreen", False)
    ventanaMenu.configure(background="black")

    FrameTablaMenu = ctk.CTkFrame(ventanaMenu, fg_color="black")
    FrameTablaMenu.pack(fill="both", expand=True)

    tree = ttk.Treeview(FrameTablaMenu, style="Custom.Treeview")
    tree.pack(fill="both", expand=True, side="left")

    scrollbar = ttk.Scrollbar(FrameTablaMenu, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)
    
    FrameBusquedaMenu = ctk.CTkFrame(ventanaMenu, fg_color="black", bg_color="black")
    FrameBusquedaMenu.pack(pady=10, fill="x", side="bottom")


def GestionarMenu():
    PantallaMenu()
    MenuData = LeerMenuJSON("src/JSON/Menu.json")
    if MenuData:
        MostrarTablaDeMenu(MenuData)
    else:
        messagebox.showerror("ERROR" , "No hay datos de menú disponibles.")

    tipos = ["Todos", "Entradas", "Principal", "Bebidas", "Postres"]
    for tipo in tipos:
        boton = ctk.CTkButton(
            ventanaMenu,
            text=tipo,
            fg_color="#2FB166" ,
            hover_color="#2FB166" ,
            command=lambda tipo=tipo: MostrarTablaDeMenu(MenuData, tipo),
            width=100,
            height=30,
            corner_radius=20
        )
        boton.pack(side="left", padx=10)
    
    BotonAgregarProducto = ctk.CTkButton(
        ventanaMenu,
        text="Agregar Producto", 
        command=lambda: AgregarProducto(MenuData), 
        fg_color="#2FB166" ,
        hover_color="#2FB166" ,
        width=125,
        height= 30,
        corner_radius=20
        )
    BotonAgregarProducto.pack(side="right", padx=10)
    
    texto = ctk.CTkLabel(
        FrameBusquedaMenu,
        text="Doble clic para modificar el precio de los productos",
        text_color="white",
        width=100,
        height=20,
        font=("Lalezar", 20),
        anchor="center",
        justify='center'
    )
    texto.pack()

    ventanaMenu.mainloop()

def PantallaDisponibilidad():
    global ventanaDisponibilidad, FrameTablaDisponibilidad, FrameTextoDisponibilidad
    ventanaDisponibilidad = Toplevel()
    ventanaDisponibilidad.title("Disponibilidad de Mesas")
    ventanaDisponibilidad.geometry("450x450")
    ventanaDisponibilidad.resizable(False, False)
    ventanaDisponibilidad.configure(background="black")

    FrameTablaDisponibilidad = ctk.CTkFrame(ventanaDisponibilidad, fg_color="black")
    FrameTablaDisponibilidad.pack(fill="both", expand=True)

    FrameTextoDisponibilidad = ctk.CTkFrame(ventanaDisponibilidad, fg_color="black" , bg_color="black")
    FrameTextoDisponibilidad.pack(fill="x", side="bottom", pady=10)

def LeerDisponibilidadJSON(archivo_json):
    try:
        with open(archivo_json, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)
        return data[0]
    except FileNotFoundError:
        messagebox.showerror("ERROR" , f" El archivo {archivo_json} no fue encontrado.")
        return {}
    except json.JSONDecodeError:
        messagebox.showerror("ERROR" , "El archivo no es un JSON válido.")
        return {}

def ProcesarDisponibilidad(data):
    filas = []
    for dia, info in data.items():
        fila = {
            "Día": dia,
            "Lugares Disponibles": info["Lugares Disponibles"],
            "Lugares Ocupados": info["Lugares Ocupados"]
        }
        filas.append(fila)
    return pd.DataFrame(filas)

def MostrarDatosDisponibilidad(data):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview.Heading", background="#2FB166", foreground="black")
    style.configure("Custom.Treeview", background="black", foreground="white", fieldbackground="black")
    style.map("Custom.Treeview", background=[("selected", "#2FB166")])

    for widget in FrameTablaDisponibilidad.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(FrameTablaDisponibilidad, style="Custom.Treeview")
    tree.pack(fill="both", expand=True, side="left")

    scrollbar = ttk.Scrollbar(FrameTablaDisponibilidad, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    tree["columns"] = ["Día", "Lugares Disponibles", "Lugares Ocupados"]
    tree["show"] = "headings"

    ancho_columnas = {"Día": 150, "Lugares Disponibles": 100, "Lugares Ocupados": 100}
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=ancho_columnas.get(col, 100), anchor="center")

    for dia, info in data.items():
        tree.insert("", "end", values=(dia, info["Lugares Disponibles"], info["Lugares Ocupados"]))

    tree.bind("<Double-1>", lambda event, tree=tree, data=data: EditarLugaresDisponibles(event, tree, data))

def EditarLugaresDisponibles(event, tree, data):
    item_id = tree.selection()[0]
    column = tree.identify_column(event.x)
    column = int(column.split("#")[-1]) - 1

    if column == 1:
        dia = tree.item(item_id, "values")[0]
        lugares_actual = tree.item(item_id, "values")[1]
        nuevo_valor = simpledialog.askstring("Editar Lugares Disponibles", f"Nueva cantidad de lugares para {dia}:", initialvalue=lugares_actual)

        if nuevo_valor:
            try:
                nuevo_valor = int(nuevo_valor)
                tree.set(item_id, column="Lugares Disponibles", value=nuevo_valor)

                data[dia]["Lugares Disponibles"] = nuevo_valor

                with open("src/JSON/Restaurante.json", "w", encoding="utf-8") as archivo:
                    json.dump([data], archivo, ensure_ascii=False, indent=4)

            except ValueError:
                messagebox.showerror("ERROR" , "Introduzca un número válido.")

def VerDisponibilidad():
    PantallaDisponibilidad()
    data_disponibilidad = LeerDisponibilidadJSON("src/JSON/Restaurante.json")

    if data_disponibilidad:
        MostrarDatosDisponibilidad(data_disponibilidad)
    else:
        messagebox.showerror("Error", "No hay datos disponibles.")

    texto = ctk.CTkLabel(
        FrameTextoDisponibilidad,
        text="Doble clic para modificar lugares disponibles",
        text_color="white",
        width=100,
        height=20,
        font=("Lalezar", 20),
        anchor="center",
        justify='center'
    )
    texto.pack()

    ventanaDisponibilidad.mainloop()

Administrador()
ventanaAdministrador.mainloop()