import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import pandas as pd
import json
from tkinter import messagebox , Toplevel, filedialog
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import qrcode

ventanaPrincipal = ctk.CTk()
ventanaPrincipal.geometry("1366x768")
ventanaPrincipal.title("El ANDEN")
ventanaPrincipal.resizable(False, False)
ventanaPrincipal.attributes("-fullscreen", True)

# Variables / Listas / Diccionarios
Pantalla = "pantalla principal"
HojasMenu = ["Menu" , "Entradas" , "Principal" , "Bebidas", "Postres"]
HojasPrecios = ["Precios" , "HojaFutbol5" , "HojaFutbol8" , "HojaTenis" , "HojaPadel"]
Entradas = {}
Principales = {}
Bebidas = {}
Postres = {}
Futbol5 = {}
Futbol8 = {}
Padel = {}
Tenis = {}
# ----------  INSTALAR PRIMERO LA FUENTE PARA QUE SE VEA EL PROGRAMA COMO DEBERIA SER, EN LA CARPETA SE ENCUENTRA EL ARCHIVO .TTF PARA INSTALAR CORRECTAMENTE LA FUENTE ----------      

#--------------FUNCIONES-------------#

# ---------- GENERALES ---------
def PonerFondo(ImagenRuta , Ventana):
    """Establece la imagen de fondo en la ventana principal."""
    Imagen = Image.open(ImagenRuta)
    ImagenTk = ImageTk.PhotoImage(Imagen)
    LabelFondo = ctk.CTkLabel(Ventana, image=ImagenTk,text="")
    LabelFondo.image = ImagenTk  
    LabelFondo.place(x=0, y=0)

def PantallaPrincipal():
    PonerFondo("src/Imagenes/Fondos/PantallaPrincipal.png" , ventanaPrincipal)
    BotonesSideBar()

def BotonesSideBar():
    """Muestra los botones en la pantalla principal."""
    ImgLogo = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonLogo.png"), size=(50, 70))
    BotonLogo = ctk.CTkButton(ventanaPrincipal, 
        text="",
        command= PantallaPrincipal,        
        image=ImgLogo,
        width=50,
        height=70,
        fg_color="#2FB166",
        border_width=0,
        corner_radius=0,
        hover_color="#2FB166"
        )
    BotonLogo.place(x=10, y=10)
    
    ImgPerfil = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonIcono.png"), size=(50, 50))
    BotonPerfil = ctk.CTkButton(ventanaPrincipal, 
        text="",        
        image=ImgPerfil,
        command=Perfil,
        width=50,
        height=50,
        fg_color="#2FB166",
        border_width=0,
        corner_radius=0,
        hover_color="#2FB166"
        )
    BotonPerfil.place(x=10, y=85)
    
    ImgPrecios = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonPrecios.png"), size=(50, 50))
    BotonPrecios = ctk.CTkButton(ventanaPrincipal, 
        text="",        
        image=ImgPrecios,
        command=Precios,
        width=50,
        height=50,
        fg_color="#2FB166",
        border_width=0,
        corner_radius=0,
        hover_color="#2FB166"
        )
    BotonPrecios.place(x=10, y=170)

    ImgFutbol = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonFutbol.png"), size=(50, 50))
    BotonFutbol = ctk.CTkButton(ventanaPrincipal, 
        text="",        
        image=ImgFutbol,
        command=PantallaFutbol,
        width=50,
        height=50,
        fg_color="#2FB166",
        border_width=0,
        corner_radius=0,
        hover_color="#2FB166"
        )
    BotonFutbol.place(x=10, y=255)
    
    ImgTenis = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonTenis.png"), size=(50, 50))
    BotonTenis = ctk.CTkButton(ventanaPrincipal, 
        text="",        
        image=ImgTenis,
        command=PantallaTenis,
        width=50,
        height=50,
        fg_color="#2FB166",
        border_width=0,
        corner_radius=0,
        hover_color="#2FB166"
        )
    BotonTenis.place(x=10, y=340)
    
    ImgPadel = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonPadel.png"), size=(50, 50))
    BotonPadel = ctk.CTkButton(ventanaPrincipal, 
        text="",        
        image=ImgPadel,
        command=PantallaPadel,
        width=50,
        height=50,
        fg_color="#2FB166",
        border_width=0,
        corner_radius=0,
        hover_color="#2FB166"
        )
    BotonPadel.place(x=10, y=425)
    
    ImgRestaurant = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonRestaurant.png"), size=(50, 50))
    BotonRestaurant = ctk.CTkButton(ventanaPrincipal, 
        text="",        
        image=ImgRestaurant,
        command=Restaurant,
        width=50,
        height=50,
        fg_color="#2FB166",
        border_width=0,
        corner_radius=0,
        hover_color="#2FB166"
        )
    BotonRestaurant.place(x=10, y=510)
    
    ImgShop = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonShop.png"), size=(50, 50))
    BotonShop = ctk.CTkButton(ventanaPrincipal, 
        text="",
        image=ImgShop, 
        command=Beneficios,
        width=50,
        height=50,
        fg_color="#2FB166",
        border_width=0,
        corner_radius=0,
        hover_color="#2FB166"
        )
    BotonShop.place(x=10, y=595)
    
    ImgCerrar = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonCerrar.png"), size=(50, 50))
    BotonCerrar = ctk.CTkButton(ventanaPrincipal, 
        text="",        
        image=ImgCerrar,
        command=Cerrar,
        width=50,
        height=50,
        fg_color="#2FB166",
        border_width=0,
        corner_radius=0,
        hover_color="#2FB166"
        )
    BotonCerrar.place(x=10, y=680)

def Cerrar():
    respuesta = messagebox.askyesno("Cerrar Programa", "Seguro quieres cerrar el programa?")
    if respuesta:
        ventanaPrincipal.destroy()

def Siguiente(TipoHoja):
    global iMenu , FondoMenu , iPrecios ,  FondoPrecios
    if TipoHoja == "HojasMenu":
        iMenu += 1
        FondoMenu = "src/Imagenes/Fondos/" + HojasMenu[iMenu] + ".png"
        PonerFondo(FondoMenu, ventanaMenu)
        BotonesMenu(TipoHoja)
        MostrarMenu()
    if TipoHoja == "HojasPrecios":
        iPrecios += 1
        FondoPrecios = "src/Imagenes/Fondos/" + HojasPrecios[iPrecios] + ".png"
        PonerFondo(FondoPrecios, ventanaPrecios)
        BotonesMenu(TipoHoja)
        MostrarPrecios()

def Atras(TipoHoja):
    global iMenu , FondoMenu , iPrecios ,  FondoPrecios
    if TipoHoja == "src/Imagenes/Fondos/HojasMenu":
        iMenu -= 1
        FondoMenu = "src/Imagenes/Fondos/" + HojasMenu[iMenu] + ".png"
        PonerFondo(FondoMenu, ventanaMenu)
        BotonesMenu(TipoHoja)
        MostrarMenu()
    if TipoHoja == "src/Imagenes/Fondos/HojasPrecios":
        iPrecios -= 1
        FondoPrecios = "src/Imagenes/Fondos/" + HojasPrecios[iPrecios] + ".png"
        PonerFondo(FondoPrecios, ventanaPrecios)
        BotonesMenu(TipoHoja)
        MostrarPrecios()

def CargarArchivo(NombreArchivo):
    try:
        with open(NombreArchivo, "r") as Archivo:
            return json.load(Archivo)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        messagebox.showerror("Error", f"Error al leer el archivo: {e}")
        return []
# ---------- REGISTRO E INICIO DE SESION ---------
def MailRegistrado(Usuario):
    """Verifica si el Mail de usuario ya está registrado."""
    MailOcupado = False
    try:
        with open("src/JSON/Usuarios.json", "r") as Archivo:
            Lineas = Archivo.read()
        Archivo = json.loads(Lineas)
        for Datos in Archivo:
            if Usuario.lower() == Datos["Mail"].lower():
                MailOcupado = True
                break
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo de usuarios no se encontró.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
    return MailOcupado

def FondoIniciarSesion():
    global Pantalla
    PonerFondo("src/Imagenes/Fondos/IniciarSesion.png" , ventanaPrincipal)
    Pantalla = "Iniciar Sesion"
    MostrarFormularioIniciarSesion()

def MostrarFormularioCrearCuenta():
    """Muestra el formulario para crear una nueva cuenta."""
    for widget in ventanaPrincipal.winfo_children():
        widget.destroy()  

    PonerFondo("src/Imagenes/Fondos/CrearCuenta.png" , ventanaPrincipal) 

    ImgBack = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonBack.png"), size=(50, 50))
    BotonBack = ctk.CTkButton(ventanaPrincipal, 
        text="",        
        image=ImgBack,
        command=Inicio,
        width=50,
        height=50,
        fg_color="black",
        border_width=0,
        corner_radius=0,
        )
    BotonBack.place(x=10, y=20)
    
    UsuarioCa = ctk.CTkEntry(
        ventanaPrincipal, 
        width=400, 
        font=("Lalezar", 25),
        placeholder_text="Ingrese el usuario",
        fg_color="white",
        corner_radius=0,
        border_color="white",
        text_color="Black"
    )
    UsuarioCa.place(x=515, y=345)

    MailCa = ctk.CTkEntry(
        ventanaPrincipal, 
        width=400, 
        font=("Lalezar", 25),
        placeholder_text="Ingrese el mail",
        fg_color="white",
        corner_radius=0,
        border_color="white",
        text_color="Black"
    )
    MailCa.place(x=515, y=450)

    ContraseñaCa = ctk.CTkEntry(
        ventanaPrincipal, 
        show="*", 
        width=400, 
        font=("Lalezar", 25),
        placeholder_text="Ingrese la contraseña",
        fg_color="white",
        corner_radius=0,
        border_color="white",
        text_color="Black"
    )
    ContraseñaCa.place(x=515, y=550)

    BotonCrearCuenta = ctk.CTkButton(
        ventanaPrincipal,
        text="Crear Cuenta",
        command=lambda: CrearCuenta(UsuarioCa.get(), MailCa.get(), ContraseñaCa.get()),
        font=("Lalezar", 30),
        width=220,
        height=60,
        fg_color="#2FB166",
        corner_radius=0,
        hover_color="#2FB166"
    )
    BotonCrearCuenta.place(x=720, y=670)
    
    BotonIniciarSesion = ctk.CTkButton(
        ventanaPrincipal,
        text="Iniciar Sesión",
        command= MostrarFormularioIniciarSesion,
        font=("Lalezar", 30),
        width=220,
        height=60,
        fg_color="#2FB166",
        corner_radius=0,
        hover_color="#2FB166"
    )
    BotonIniciarSesion.place(x=430, y=670)

def MostrarFormularioIniciarSesion():
    """Muestra el formulario para iniciar sesión."""
    for widget in ventanaPrincipal.winfo_children():
        widget.destroy()  

    PonerFondo("src/Imagenes/Fondos/IniciarSesion.png" , ventanaPrincipal) 

    ImgBack = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonBack.png"), size=(50, 50))
    BotonBack = ctk.CTkButton(ventanaPrincipal, 
        text="",        
        image=ImgBack,
        command=Inicio,
        width=50,
        height=50,
        fg_color="black",
        border_width=0,
        corner_radius=0,
        )
    BotonBack.place(x=10, y=20)

    Mail = ctk.CTkEntry(
        ventanaPrincipal, 
        width=400, 
        font=("Lalezar", 25),
        placeholder_text="Ingrese el mail",
        fg_color="white",
        corner_radius=0,
        border_color="white",
        text_color="Black"
    )
    Mail.place(x=515, y=435) 

    Contraseña = ctk.CTkEntry(
        ventanaPrincipal, 
        show="*", 
        width=400, 
        font=("Lalezar", 25),
        placeholder_text="Ingrese la contraseña",
        fg_color="white",
        corner_radius=0,
        border_color="white",
        text_color="Black"
    )
    Contraseña.place(x=515, y=535)

    BotonIniciarSesion = ctk.CTkButton(
        ventanaPrincipal,
        text="Iniciar Sesión",
        command=lambda: IniciarSesion(Mail.get(), Contraseña.get()),
        font=("Lalezar", 30),
        width=220,
        height=60,
        fg_color="#2FB166",
        corner_radius=0,
        hover_color="#2FB166"
    )
    BotonIniciarSesion.place(x=720, y=670)

    BotonCrearCuenta = ctk.CTkButton(
        ventanaPrincipal,
        text="Crear Cuenta",
        command=MostrarFormularioCrearCuenta,
        font=("Lalezar", 30),
        width=220,
        height=60,
        fg_color="#2FB166",
        corner_radius=0,
        hover_color="#2FB166"
    )
    BotonCrearCuenta.place(x=430, y=670)

def IniciarSesion(Mail, Contraseña):
    """Inicia sesión verificando las credenciales del usuario."""
    global NombreUsuario, MailUsuario , PuntosClub , ImagenPerfil
    SesionIniciada = False
    try:
        with open("src/JSON/Usuarios.json", "r") as Archivo:
            Lineas = Archivo.read()
        Datos = json.loads(Lineas)
        for UsuarioRegistrado in Datos:
            if Mail.lower() == UsuarioRegistrado["Mail"].lower():
                if Contraseña == UsuarioRegistrado["Clave"]:
                    NombreUsuario = UsuarioRegistrado["Usuario"]
                    MailUsuario = UsuarioRegistrado["Mail"]
                    PuntosClub = UsuarioRegistrado["Puntos"]
                    ImagenPerfil = UsuarioRegistrado["Imagen"]
                    messagebox.showinfo("Éxito", "Inicio de Sesión Exitoso")
                    SesionIniciada = True
                    PonerFondo("src/Imagenes/Fondos/PantallaPrincipal.png" , ventanaPrincipal)
                    BotonesSideBar()
                    break
        if not SesionIniciada:
            messagebox.showerror("Error", "Mail o Contraseña Incorrectos")
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo de usuarios no se encontró.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

def CrearCuenta(Usuario, Mail, Contraseña):
    """Crea una nueva cuenta de usuario."""
    global NombreUsuario, MailUsuario , PuntosClub , ImagenPerfil
    MailOcupado = MailRegistrado(Mail)
    if not MailOcupado:
        try:
            with open("src/JSON/Usuarios.json", "r") as Archivo:
                try:
                    Datos = json.load(Archivo)
                except json.JSONDecodeError:
                    Datos = []
        except FileNotFoundError:
            Datos = []
        NombreUsuario = Usuario
        MailUsuario = Mail
        PuntosClub = 0
        ImagenPerfil = "src/Imagenes/FotosPerfil/Inicial.png"
        Datos.append({"Usuario": NombreUsuario, "Mail": MailUsuario, "Clave": Contraseña, "Imagen" : ImagenPerfil , "Puntos" : PuntosClub})
        DatosJson = json.dumps(Datos, indent=4)
        try:
            with open("src/JSON/Usuarios.json", "w") as Contenido:
                Contenido.write(DatosJson)
            messagebox.showinfo("Éxito", "El usuario ha sido registrado con éxito.")
            PonerFondo("src/Imagenes/Fondos/PantallaPrincipal.png" , ventanaPrincipal)
            BotonesSideBar()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al registrar el usuario: {e}")
    else:
        messagebox.showerror("Error", "Este mail ya esta registrado")

# ---------- PERFIL ---------
def Perfil():
    PonerFondo("src/Imagenes/Fondos/Perfil.png" , ventanaPrincipal)
    BotonesSideBar()
    BotonesPerfil()
    MostrarDatosPerfil()
    MostrarImagenPerfil()
    BotonesModificarDatos()

def MostrarDatosPerfil():
    global NombreUsuario , MailUsuario , PuntosClub , DatosPerfil
    DatosPerfil = (
                f"Nombre: {NombreUsuario}\n"
                f"Mail: {MailUsuario}\n"
                f"Contraseña: ******\n"
                f"Puntos: {PuntosClub}\n"
            )
    texto = ctk.CTkLabel(
                ventanaPrincipal,
                text = DatosPerfil,
                text_color = "white",
                bg_color="#2FB166",
                width = 620,
                height= 100,
                fg_color="#2FB166",
                font=("Lalezar", 18),
                anchor=ctk.W,
                justify='left'
            )
    texto.place(x=495, y=185)

def BotonesPerfil():
    BotonCambiarFoto = ctk.CTkButton(
    ventanaPrincipal,
    text="Cambiar",
    text_color="white",
    width=100,
    height=30,
    fg_color="#2FB166",
    bg_color="#2FB166",
    corner_radius=0,
    hover_color="#2FB166",
    command=CargarImagenPerfil,
    font=("Lalezar", 18)
    )
    BotonCambiarFoto.place(x=260, y=345)

    BotonVerReservas = ctk.CTkButton(
        ventanaPrincipal,
        text="Ver Reservas",
        text_color="white",
        width=220,
        height=60,
        fg_color="#2FB166",
        corner_radius=0,
        hover_color="#2FB166",
        command=lambda:SeleccionTipoReserva("Ver"),
        font=("Lalezar", 25)
    )
    BotonVerReservas.place(x=575, y=460)
    
    BotonCancelarReserva = ctk.CTkButton(
    ventanaPrincipal,
    text="Cancelar Reserva",
    text_color="white",
    width=220,
    height=60,
    fg_color="#2FB166",
    corner_radius=0,
    hover_color="#2FB166",
    command=lambda:SeleccionTipoReserva("Cancelar"),
    font=("Lalezar", 25)
    )
    BotonCancelarReserva.place(x=575, y=570)

    BotonCerrarSesion = ctk.CTkButton(
    ventanaPrincipal,
    text="Cerrar Sesion",
    text_color="white",
    width=220,
    height=60,
    fg_color="#2FB166",
    corner_radius=0,
    hover_color="#2FB166",
    command=CerrarSesion,
    font=("Lalezar", 25)
    )
    BotonCerrarSesion.place(x=575, y=675)

def BotonesModificarDatos():
    BotonCambiarNombre = ctk.CTkButton(
        ventanaPrincipal, 
        command=cambiarNombre,
        text="Cambiar",
        text_color="white",
        fg_color="#2FB166",
        bg_color="#2FB166",
        width=50,
        height=20,
        font=("Lalezar", 15),
        corner_radius=0,
        hover_color="#2FB166"
        )

    BotonCambiarNombre.place(x=1050, y=185)

    BotonCambiarMail = ctk.CTkButton(
        ventanaPrincipal, 
        command=cambiarGmail,
        text="Cambiar",
        text_color="white",
        fg_color="#2FB166",
        bg_color="#2FB166",
        width=50,
        height=20,
        font=("Lalezar", 15),
        corner_radius=0,
        hover_color="#2FB166"
        )
    BotonCambiarMail.place(x=1050, y=210)
    BotonCambiarClave = ctk.CTkButton(
        ventanaPrincipal, 
        command=cambiarContraseña,
        text="Cambiar",
        text_color="white",
        fg_color="#2FB166",
        bg_color="#2FB166",
        width=50,
        height=20,
        font=("Lalezar", 15),
        corner_radius=0,
        hover_color="#2FB166"
        )
    BotonCambiarClave.place(x=1050, y=240)

def cambiarNombre():
    global NombreUsuario
    VentanaCambiarNombre = ctk.CTkToplevel(ventanaPrincipal)
    VentanaCambiarNombre.geometry("250x100")
    VentanaCambiarNombre.title("Cambiar Datos")
    VentanaCambiarNombre.resizable(False, False)
    VentanaCambiarNombre.transient(ventanaPrincipal)  
    VentanaCambiarNombre.lift()  
    VentanaCambiarNombre.focus_set()  
    VentanaCambiarNombre.grab_set()
    LabelNuevoNombre = ctk.CTkLabel(VentanaCambiarNombre, text="Ingresar Nuevo Nombre")
    LabelNuevoNombre.place(x=50, y=5)


    EntradaNombre = ctk.CTkEntry(
        VentanaCambiarNombre,
        height=20,
        width=120,
        corner_radius=0,
        font=("Lalezar", 12),
        )
    EntradaNombre.place(x=65, y=40)

    def Guardar():
        global NombreUsuario
        NuevoNombre = EntradaNombre.get()
        guardarNombre(NuevoNombre)
        NombreUsuario = NuevoNombre
        messagebox.showinfo("Cambios Realizados","El Nombre se modifico correctamente")
        VentanaCambiarNombre.destroy()
        Perfil()

    BotonGuardar = ctk.CTkButton(
        VentanaCambiarNombre, 
        text="Guardar", 
        command=Guardar,
        height=20,
        width=50,
        text_color="white",
        fg_color="#2FB166",
        bg_color="#2FB166",
        corner_radius=0,
        font=("Lalezar", 12),
        )
    BotonGuardar.place(x=100, y=70)

def guardarNombre(NuevoNombre):
    global MailUsuario
    try:
        with open("src/JSON/Usuarios.json", "r") as archivo:
            datos = json.load(archivo)

        UsuarioEncontrado = False
        for UsuarioRegistrado in datos:
            if UsuarioRegistrado["Mail"] == MailUsuario:
                UsuarioRegistrado["Usuario"] = NuevoNombre
                UsuarioEncontrado = True
                break
        if not UsuarioEncontrado:
            messagebox.showwarning("Advertencia", "Usuario no encontrado.")
        with open("src/JSON/Usuarios.json", "w") as archivo:
            json.dump(datos, archivo, indent=4)
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo de usuarios no se encontro.")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "El archivo de usuarios está corrupto.")

def cambiarGmail():
    global MailUsuario
    NuevaVentana = ctk.CTkToplevel(ventanaPrincipal)
    NuevaVentana.geometry("250x100")
    NuevaVentana.title("Cambiar Datos")
    NuevaVentana.resizable(False, False)
    NuevaVentana.transient(ventanaPrincipal)  
    NuevaVentana.lift()  
    NuevaVentana.focus_set()  
    NuevaVentana.grab_set()
    LabelNuevoMail = ctk.CTkLabel(NuevaVentana, text="Ingrese Nuevo Mail")
    LabelNuevoMail.place(x=50, y=5)

    EntradaMail = ctk.CTkEntry(
        NuevaVentana,
        height=20,
        width=120,
        corner_radius=0,
        font=("Lalezar", 12),
        )
    EntradaMail.place(x=65, y=40)

    def Guardar():
        global MailUsuario
        NuevoMail = EntradaMail.get()
        guardarMail(NuevoMail)
        MailUsuario = NuevoMail
        messagebox.showinfo("Cambios Realizados","El Mail se modifico correctamente")
        NuevaVentana.destroy()
        Perfil()

    BotonGuardar = ctk.CTkButton(
        NuevaVentana,
        text="Guardar", 
        command=Guardar,
        height=20,
        width=50,
        text_color="white",
        fg_color="#2FB166",
        bg_color="#2FB166",
        corner_radius=0,
        font=("Lalezar", 12),
        )
    BotonGuardar.place(x=100, y=70)

def guardarMail(nuevoMail):
    global MailUsuario
    try:
        with open("src/JSON/Usuarios.json", "r") as archivo:
            datos = json.load(archivo)

        UsuarioEncontrado = False
        for UsuarioRegistrado in datos:
            if UsuarioRegistrado["Mail"] == MailUsuario:
                UsuarioRegistrado["Mail"] = nuevoMail
                UsuarioEncontrado = True
                break
        if not UsuarioEncontrado:
            messagebox.showwarning("Advertencia", "Usuario no encontrado.")
        with open("src/JSON/Usuarios.json", "w") as archivo:
            json.dump(datos, archivo, indent=4)
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo de usuarios no se encontro.")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "El archivo de usuarios está corrupto.")

def cambiarContraseña():
    VentanaCambiarContraseña = ctk.CTkToplevel(ventanaPrincipal)
    VentanaCambiarContraseña.geometry("250x100")
    VentanaCambiarContraseña.title("Cambiar Datos")
    VentanaCambiarContraseña.resizable(False, False)
    VentanaCambiarContraseña.transient(ventanaPrincipal)  
    VentanaCambiarContraseña.lift()  
    VentanaCambiarContraseña.focus_set()  
    VentanaCambiarContraseña.grab_set()

    LabelNuevaContraseña = ctk.CTkLabel(VentanaCambiarContraseña, text="Ingrese Nueva Contraseña")
    LabelNuevaContraseña.place(x=50, y=5)

    EntradaContraseña = ctk.CTkEntry(
        VentanaCambiarContraseña,
        show="*",
        height=20,
        width=120,
        corner_radius=0,
        font=("Lalezar", 12),
        )
    EntradaContraseña.place(x=65, y=40)

    def Guardar():
        NuevaClave = EntradaContraseña.get()
        guardarContraseña(NuevaClave)
        messagebox.showinfo("Cambios Realizados","La Contraseña se modifico correctamente")
        VentanaCambiarContraseña.destroy()

    BotonGuardar = ctk.CTkButton(
        VentanaCambiarContraseña,
        text="Guardar", 
        command=Guardar,
        height=20,
        width=50,
        text_color="white",
        fg_color="#2FB166",
        bg_color="#2FB166",
        corner_radius=0,
        font=("Lalezar", 12),
        )
    BotonGuardar.place(x=100, y=70)

def guardarContraseña(nuevaClave):
    global MailUsuario
    try:
        with open("src/JSON/Usuarios.json", "r") as archivo:
            datos = json.load(archivo)

        UsuarioEncontrado = False
        for UsuarioRegistrado in datos:
            if UsuarioRegistrado["Mail"] == MailUsuario:
                UsuarioRegistrado["Clave"] = nuevaClave
                UsuarioEncontrado = True
                break
        if not UsuarioEncontrado:
            messagebox.showwarning("Advertencia", "Usuario no encontrado.")
        with open("src/JSON/Usuarios.json", "w") as archivo:
            json.dump(datos, archivo, indent=4)
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo de usuarios no se encontro.")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "El archivo de usuarios está corrupto.")

def MostrarImagenPerfil():
    global ImagenPerfil
    if ImagenPerfil:
        try:
            image = Image.open(ImagenPerfil)
            image = image.resize((185, 185), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            LabelImagenPerfil = ctk.CTkLabel(ventanaPrincipal, image=photo, text="")
            LabelImagenPerfil.image = photo
            LabelImagenPerfil.place(x=220, y=125)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")

def CargarImagenPerfil():
    global ImagenPerfil
    file_path = filedialog.askopenfilename(title="Selecciona una imagen", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    if file_path:
        try:
            size = (185, 185)
            image = Image.open(file_path)
            image = image.resize(size, Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            LabelImagenPerfil = ctk.CTkLabel(ventanaPrincipal, image=photo, text="")
            LabelImagenPerfil.image = photo
            LabelImagenPerfil.place(x=220, y=125)

            ImagenPerfil = file_path

            ActualizarImagenEnJSON(ImagenPerfil)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")

def ActualizarImagenEnJSON(ImagenNueva):
    global NombreUsuario
    try:
        with open("src/JSON/Usuarios.json", "r") as Archivo:
            Datos = json.load(Archivo)

        # Buscar al usuario y actualizar su imagen
        for UsuarioRegistrado in Datos:
            if UsuarioRegistrado["Usuario"] == NombreUsuario:
                UsuarioRegistrado["Imagen"] = ImagenNueva
                break

        # Guardar los cambios en el archivo JSON
        with open("src/JSON/Usuarios.json", "w") as Archivo:
            json.dump(Datos, Archivo, indent=4)
        
        messagebox.showinfo("Éxito", "La imagen de perfil ha sido actualizada.")

    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo de usuarios no se encontró.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al actualizar la imagen: {e}")

def CerrarSesion():
    global NombreUsuario , MailUsuario
    
    respuesta = messagebox.askyesno("Cerrar Sesion", "Seguro quieres cerrar sesion?")
    if respuesta:
        Inicio()

# ---------- GESTION RESERVAS ---------
def PantallaVerReservas():
    global ventanaReservas
    ventanaReservas = Toplevel(ventanaPrincipal)
    ventanaReservas.title("Reservas")
    ventanaReservas.geometry("950x650")
    ventanaReservas.resizable(False, False)
    ventanaReservas.configure(background="black")

def LeerReservasJSON(ArchivoJSON):
    try:
        with open(ArchivoJSON, "r", encoding="utf-8") as archivo:
            data = json.load(archivo) 
        return pd.DataFrame(data)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        messagebox.showerror("ERROR" , f"Error al leer el archivo: {e}")
        return pd.DataFrame()

def TablaReservas(NombreArchivoReservas):
    global FrameBusqueda, FrameTabla
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
    FrameTabla = ctk.CTkFrame(ventanaReservas, fg_color="black")
    FrameTabla.pack(fill="both", expand=True)

    FrameBusqueda = ctk.CTkFrame(ventanaReservas, fg_color="black")
    FrameBusqueda.pack(pady=10)

    global BuscarDeporte, BuscarCancha, BuscarDia, BuscarNumero
    BuscarNumero = ctk.CTkEntry(
        FrameBusqueda, 
        width=175,
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
        FrameBusqueda, 
        width=175, 
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
        FrameBusqueda, 
        width=175,
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
        FrameBusqueda, 
        width=175,
        height=30, 
        placeholder_text="Cancha",
        placeholder_text_color="white",
        text_color="white",
        border_width=2,
        border_color="#2FB166",
        fg_color="#2FB166"
    )
    BuscarCancha.pack(side="left", padx=10)

    if NombreArchivoReservas == "src/JSON/ReservasRestaurante.json":
        BuscarCancha.pack_forget()
        BuscarDeporte.pack_forget()

    BotonBuscar = ctk.CTkButton(FrameBusqueda, text="Buscar", width=175,
                                height=30, command=BuscarReserva,
                                fg_color="#2FB166", text_color="white", bg_color="black")
    BotonBuscar.pack(side="left", padx=10)

def MostrarDatos(df):
    global FrameTabla
    for widget in FrameTabla.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(FrameTabla, style="Custom.Treeview")
    tree.pack(fill="both", expand=True, side="left")

    scrollbar = ttk.Scrollbar(FrameTabla, orient="vertical", command=tree.yview)
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
    global MailUsuario
    Hojas = LeerReservasJSON(NombreArchivoReservas)
    FiltroNumeroReserva = BuscarNumero.get()
    FiltroCancha = BuscarCancha.get()
    FiltroDia = BuscarDia.get()
    FiltroDeporte = BuscarDeporte.get()

    resultado = Hojas[Hojas['Mail'] == MailUsuario]
    if FiltroNumeroReserva:
        resultado = resultado[resultado['Numero Reserva'].astype(str) == FiltroNumeroReserva]
    if FiltroCancha:
        resultado = resultado[resultado['Cancha'].str.contains(FiltroCancha, case=False)]
    if FiltroDia:
        resultado = resultado[resultado['Dia'].str.contains(FiltroDia, case=False)]
    if FiltroDeporte:
        resultado = resultado[resultado['Deporte'].str.contains(FiltroDeporte, case=False)]
    
    MostrarDatos(resultado)

def VerReservas(TipoReservaSeleccionado):
    global MailUsuario
    if TipoReservaSeleccionado is None:
        messagebox.showerror("ERROR", "Debe seleccionar un tipo de reserva.")
        return
    ventanaSeleccion.destroy()
    if TipoReservaSeleccionado == "Canchas":
        NombreArchivoReservas = "src/JSON/Reservas.json"
    elif TipoReservaSeleccionado == "Restaurante":
        NombreArchivoReservas = "src/JSON/ReservasRestaurante.json"
    PantallaVerReservas()
    TablaReservas(NombreArchivoReservas)
    Hojas = LeerReservasJSON(NombreArchivoReservas)
    if not Hojas.empty:
        MostrarDatos(Hojas[Hojas['Mail'] == MailUsuario])
    else:
        messagebox.showerror("ERROR" , "No hay datos disponibles.")

def SeleccionTipoReserva(DestinoReserva):
    global ventanaSeleccion
    ventanaSeleccion = Toplevel(ventanaPrincipal)
    ventanaSeleccion.title("Tipo de Reserva")
    ventanaSeleccion.geometry("200x300")
    ventanaSeleccion.resizable(False, False)
    ventanaSeleccion.transient(ventanaPrincipal)  
    ventanaSeleccion.lift()  
    ventanaSeleccion.focus_set()  
    ventanaSeleccion.grab_set()
    ventanaSeleccion.configure(background="black")

    Funcion = {"Cancelar": CancelarReserva, "Ver": VerReservas}.get(DestinoReserva)
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

# ---------- CANCELAR RESERVAS ---------
def VentanaTexto():
    global PestañaTexto, EntradaTexto, TextoIngresado
    TextoIngresado = None
    PestañaTexto = Toplevel(ventanaPrincipal)
    PestañaTexto.geometry("400x150")
    PestañaTexto.title("Datos")
    PestañaTexto.resizable(False, False)
    PestañaTexto.configure(background="black")
    
    if not Mail:
        Dato = "Número de Reserva"
        Mostrar = ""
    else: 
        Dato = "Contraseña"
        Mostrar = "*"
    
    EntradaTexto = ctk.CTkEntry(
        PestañaTexto,
        width=300,
        show=Mostrar ,
        height=50,
        font=("Lalezar", 20),
        placeholder_text=f"Ingrese su {Dato}",
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

def CancelarReserva(TipoReservaSeleccionado):
    global Mail, Usuario, NumeroIngresado , NombreArchivoReservas
    Mail = False
    Usuario = False
    if TipoReservaSeleccionado is None:
        messagebox.showerror("ERROR", "Debe seleccionar un tipo de reserva.")
        return
    ventanaSeleccion.destroy()
    if TipoReservaSeleccionado == "Canchas":
        NombreArchivoReservas = "Reservas.json"
    elif TipoReservaSeleccionado == "Restaurante":
        NombreArchivoReservas = "ReservasRestaurante.json"

    VentanaTexto()
    
    if TextoIngresado is not None:
        NumeroIngresado = TextoIngresado
        VerificarMail()
        if Mail:
            VentanaTexto()
            VerificarUsuario()
            if Usuario:
                ReestablecerDatosReserva(NumeroIngresado)
            messagebox.showinfo("Exito" , "Reserva cancelada exitosamente")
            Mensaje = (f"Se a cancelado con exito su reserva de numero {NumeroIngresado}")
            EnviarMail(MailUsuario , Mensaje , "Reserva Cancelada")
        else:
            messagebox.showerror("ERROR" , "La verificación de usuario falló, la reserva no se cancela")
    else:
        messagebox.showerror("ERROR" , "Correo no verificado o número de reserva no encontrado")

def ReestablecerDatosReserva(NumeroIngresado):
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
                    ArchivoDeporte = "src/JSON/" + DeporteReserva + ".json"
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
        if NombreArchivoReservas == "src/JSON/ReservasRestaurante.json":
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

def VerificarMail():
    global Mail
    Mail = False
    with open(NombreArchivoReservas, 'r') as file:
        Reservas = json.load(file)

    for reserva in Reservas:
        if reserva['Numero Reserva'] == str(NumeroIngresado):
            if reserva['Mail'] == MailUsuario:
                messagebox.showinfo("" , "Correo verificado")
                Mail = True
                return
            else:
                messagebox.showerror("ERROR" , "El correo ingresado no coincide con la reserva")
                return
    
    messagebox.showerror("ERROR" , "Número de reserva no encontrado")

def VerificarUsuario():
    global Usuario
    Usuario = False
    
    with open("src/JSON/Usuarios.json", 'r') as file:
        Usuarios = json.load(file)

    for usuario in Usuarios:
        if usuario['Mail'] == MailUsuario:
            if TextoIngresado is not None:
                ClaveIngresada = TextoIngresado
                if usuario['Clave'] == ClaveIngresada:
                    messagebox.showinfo("" , "Clave verificada")
                    Usuario = True
                    return
                else:
                    messagebox.showerror("ERROR" , "Clave incorrecta")
                    return

    messagebox.showerror("ERROR" , "Usuario no encontrado")

# ---------- MENU ---------
def CargarMenu():
    global FondoMenu
    Archivo = CargarArchivo("src/JSON/Menu.json")
    for Menu in Archivo:
        for Hoja, Productos in Menu.items():
            if Hoja == "Entradas":
                for Producto, Precio in Productos.items():
                    Entradas[Producto] = Precio
            elif Hoja == "Principal":
                for Producto, Precio in Productos.items():
                    Principales[Producto] = Precio
            elif Hoja == "Bebidas":
                for Producto, Precio in Productos.items():
                    Bebidas[Producto] = Precio
            elif Hoja == "Postres":
                for Producto, Precio in Productos.items():
                    Postres[Producto] = Precio

def MostrarMenu():
    global FondoMenu
    YProductos = 118
    YPrecios = 118
    if FondoMenu == "src/Imagenes/Fondos/Entradas.png":
        for Producto, Precio in Entradas.items():
            Productos = ctk.CTkLabel(
                ventanaMenu,
                text=f"{Producto}",
                text_color="black",
                fg_color="#2FB166",
                bg_color="#2FB166",
                corner_radius=0,
                font=("Lalezar", 20),
                anchor=ctk.W,
                justify='left'
            )
            Productos.place(x=75, y=YProductos)
            YProductos += 50
            Precios = ctk.CTkLabel(
                ventanaMenu,
                text=f"${Precio}",
                text_color="black",
                fg_color="#2FB166",
                bg_color="#2FB166",
                corner_radius=0,
                font=("Lalezar", 20),
                anchor=ctk.W,
                justify='right'
            )
            Precios.place(x=270, y=YPrecios)
            YPrecios += 50
    elif FondoMenu == "src/Imagenes/Fondos/Principal.png":
        for Producto, Precio in Principales.items():
            Productos = ctk.CTkLabel(
                ventanaMenu,
                text=f"{Producto}",
                text_color="black",
                fg_color="#2FB166",
                bg_color="#2FB166",
                corner_radius=0,
                font=("Lalezar", 20),
                anchor=ctk.W,
                justify='left'
            )
            Productos.place(x=75, y=YProductos)
            YProductos += 50
            Precios = ctk.CTkLabel(
                ventanaMenu,
                text=f"${Precio}",
                text_color="black",
                fg_color="#2FB166",
                bg_color="#2FB166",
                corner_radius=0,
                font=("Lalezar", 20),
                anchor=ctk.W,
                justify='right'
            )
            Precios.place(x=270, y=YPrecios)
            YPrecios += 50
    elif FondoMenu == "src/Imagenes/Fondos/Bebidas.png":
        for Producto, Precio in Bebidas.items():
            Productos = ctk.CTkLabel(
                ventanaMenu,
                text=f"{Producto}",
                text_color="black",
                fg_color="#2FB166",
                bg_color="#2FB166",
                corner_radius=0,
                font=("Lalezar", 20),
                anchor=ctk.W,
                justify='left'
            )
            Productos.place(x=75, y=YProductos)
            YProductos += 50
            Precios = ctk.CTkLabel(
                ventanaMenu,
                text=f"${Precio}",
                text_color="black",
                fg_color="#2FB166",
                bg_color="#2FB166",
                corner_radius=0,
                font=("Lalezar", 20),
                anchor=ctk.W,
                justify='right'
            )
            Precios.place(x=270, y=YPrecios)
            YPrecios += 50
    elif FondoMenu == "src/Imagenes/Fondos/Postres.png":
        for Producto, Precio in Postres.items():
            Productos = ctk.CTkLabel(
                ventanaMenu,
                text=f"{Producto}",
                text_color="black",
                fg_color="#2FB166",
                bg_color="#2FB166",
                corner_radius=0,
                font=("Lalezar", 20),
                anchor=ctk.W,
                justify='left'
            )
            Productos.place(x=75, y=YProductos)
            YProductos += 50
            Precios = ctk.CTkLabel(
                ventanaMenu,
                text=f"${Precio}",
                text_color="black",
                fg_color="#2FB166",
                bg_color="#2FB166",
                corner_radius=0,
                font=("Lalezar", 20),
                anchor=ctk.W,
                justify='right'
            )
            Precios.place(x=270, y=YPrecios)
            YPrecios += 50

def Menu():
    global iMenu , ventanaMenu , FondoMenu
    CargarMenu()
    ventanaMenu = Toplevel(ventanaPrincipal)
    ventanaMenu.geometry("400x600")
    ventanaMenu.title("MENU")
    ventanaMenu.resizable(False, False)
    ventanaMenu.transient(ventanaPrincipal)  
    ventanaMenu.lift()  
    ventanaMenu.focus_set()  
    ventanaMenu.grab_set()

    iMenu = 0
    FondoMenu = "src/Imagenes/Fondos/" + HojasMenu[iMenu] + ".png"
    PonerFondo(FondoMenu, ventanaMenu)
    BotonesMenu("HojasMenu")
    MostrarMenu()

def BotonesMenu(TipoHoja):
    if TipoHoja == "HojasMenu":
        i = iMenu
        ventana = ventanaMenu
        Lista = HojasMenu
    if TipoHoja == "HojasPrecios":
        i = iPrecios
        ventana = ventanaPrecios
        Lista = HojasPrecios

    ImgAtras = ctk.CTkImage(Image.open("src/Imagenes/Botones/Atras.png"), size=(40, 20))
    BotonAtras = ctk.CTkButton(
        ventana, 
        text="",        
        image=ImgAtras,
        command=lambda: Atras(TipoHoja),
        width=40,
        height=20,
        fg_color="black",
        border_width=0,
        bg_color="black",
        corner_radius=0,
        hover_color="black"
    )
    if i == 0:
        BotonAtras.place_forget()
    else:
        BotonAtras.place(x=40, y=565)

    ImgAdelante = ctk.CTkImage(Image.open("src/Imagenes/Botones/Siguiente.png"), size=(40, 20))
    BotonAdelante = ctk.CTkButton(
        ventana, 
        text="",        
        image=ImgAdelante,
        command=lambda: Siguiente(TipoHoja),
        width=40,
        height=20,
        fg_color="black",
        border_width=0,
        bg_color="black",
        corner_radius=0,
        hover_color="black"
    )
    if i == len(Lista) - 1:
        BotonAdelante.place_forget()
    else:
        BotonAdelante.place(x=320, y=565)

def Restaurant():
    PonerFondo("src/Imagenes/Fondos/Restaurante.png" , ventanaPrincipal)
    BotonesSideBar()
    ImgReserva = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonReserva.png"), size=(250, 250))
    BotonReserva = ctk.CTkButton(ventanaPrincipal, 
        text="",        
        image=ImgReserva,
        command=PantallaReservaRestaurante,
        width=50,
        height=50,
        fg_color="#2FB166",
        border_width=0,
        bg_color="black",
        corner_radius=0,
        hover_color="#2FB166"
        )
    BotonReserva.place(x=235, y=300)
    
    ImgMenu = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonMenu.png"), size=(250, 250))
    BotonMenu = ctk.CTkButton(ventanaPrincipal, 
        text="",        
        image=ImgMenu,
        command=Menu,
        width=50,
        height=50,
        fg_color="#2FB166",
        border_width=0,
        border_color="black",
        corner_radius=0,
        hover_color="#2FB166"
        )
    BotonMenu.place(x=920, y=300)    

ArchivoJSON = 'src/JSON/Restaurante.json'
def CargarDatosJSON():
    try:
        with open(ArchivoJSON, 'r') as archivo:
            return json.load(archivo)
    except FileNotFoundError:

        return [
            {
                "Lunes": {"Lugares Disponibles": 50, "Lugares Ocupados": 0},
                "Martes": {"Lugares Disponibles": 50, "Lugares Ocupados": 0},
                "Miércoles": {"Lugares Disponibles": 50, "Lugares Ocupados": 0},
                "Jueves": {"Lugares Disponibles": 50, "Lugares Ocupados": 0},
                "Viernes": {"Lugares Disponibles": 50, "Lugares Ocupados": 0},
                "Sábado": {"Lugares Disponibles": 50, "Lugares Ocupados": 0},
                "Domingo": {"Lugares Disponibles": 50, "Lugares Ocupados": 0}
            }
        ]

def GuardarDatosJSON(datos):
    with open(ArchivoJSON, 'w') as archivo:
        json.dump(datos, archivo, indent=4)

def PantallaReservaRestaurante():
    ventanaReservas = Toplevel(ventanaPrincipal)
    ventanaReservas.geometry("400x600")
    ventanaReservas.title("Reservas")
    ventanaReservas.resizable(False, False)
    ventanaReservas.transient(ventanaPrincipal)  
    ventanaReservas.lift()  
    ventanaReservas.focus_set()  
    ventanaReservas.grab_set()
    PonerFondo("src/Imagenes/Fondos/Reservas 1.png",ventanaReservas)
    
    UsuarioNombre = ctk.CTkEntry(
        ventanaReservas, 
        width=200, 
        height=40,
        font=("Lalezar", 20),
        placeholder_text="Ingrese Nombre",
        fg_color="white",
        corner_radius=0,
        border_color="white",
        text_color="Black"
    )
    UsuarioNombre.place(x=113, y=267)
    
    TelefonoUsuario = ctk.CTkEntry(
        ventanaReservas, 
        width=200, 
        height=40, 
        font=("Lalezar", 20),
        placeholder_text="Ingrese su Telefono",
        fg_color="white",
        corner_radius=0,
        border_color="white",
        text_color="Black"
    )
    TelefonoUsuario.place(x=113, y=345)

    DiasData = CargarDatosJSON()[0]
    DiasSemana = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

    SliderDias = ctk.CTkSlider(ventanaReservas, from_=0, to=6, number_of_steps=6, 
                            bg_color="#2FB166", button_color="blue")
    SliderDias.place(x=105, y=450)

    LabelDia = ctk.CTkLabel(ventanaReservas, text="Día: Jueves", fg_color="#2FB166", bg_color="#2FB166", text_color="white")
    LabelDia.place(x=160, y=470)

    def ActualizarLabelDia():
        valor = int(SliderDias.get())  
        dia = DiasSemana[valor]  
        LabelDia.configure(text=f"Día: {dia}")  

    def MoverSliderDia(event):
        current_value = int(SliderDias.get())  
        if event.keysym == 'Left' or event.keysym == 'Down':
            new_value = max(0, current_value - 1) 
        elif event.keysym == 'Right' or event.keysym == 'Up':
            new_value = min(6, current_value + 1)  

        SliderDias.set(new_value)  
        ActualizarLabelDia() 

    def MostrarValorDia(valor):
        ActualizarLabelDia()
        
    ventanaReservas.bind("<Left>", MoverSliderDia)
    ventanaReservas.bind("<Right>", MoverSliderDia)
    ventanaReservas.bind("<Up>", MoverSliderDia)
    ventanaReservas.bind("<Down>", MoverSliderDia)
    
    SliderDias.configure(command=MostrarValorDia)
    slider_valor = ctk.CTkSlider(ventanaReservas, from_=1, to=20, number_of_steps=20, bg_color="#2FB166", button_color="green")
    slider_valor.place(x=105, y=400)

    LabelValor = ctk.CTkLabel(ventanaReservas, text="Cantidad de comensales: 5", fg_color="#2FB166", bg_color="#2FB166", text_color="white")
    LabelValor.place(x=115, y=415)

    def ActualizarLabelValor():
        valor = int(slider_valor.get())
        LabelValor.configure(text=f"Cantidad de comensales: {valor}")

    def MoverSliderValor(event):
        current_value = slider_valor.get()
        if event.keysym == 'Left' or event.keysym == 'Down':
            new_value = max(0, current_value - 1)
        elif event.keysym == 'Right' or event.keysym == 'Up':
            new_value = min(100, current_value + 1)

        slider_valor.set(new_value)
        ActualizarLabelValor()


    ventanaReservas.bind("<Left>", MoverSliderValor)
    ventanaReservas.bind("<Right>", MoverSliderValor)
    ventanaReservas.bind("<Up>", MoverSliderValor)
    ventanaReservas.bind("<Down>", MoverSliderValor)

    slider_valor.configure(command=lambda valor: ActualizarLabelValor())

    DiaElegidoRes=SliderDias.get()
    CantidadElegidaRes=slider_valor.get()
    

    def reservaconexito():
        global datosRestaurante
        NombrePersona = UsuarioNombre.get()  
        TelefonoPersona = TelefonoUsuario.get()  
        valor_dia = int(SliderDias.get())  
        DiaSeleccionado = DiasSemana[valor_dia]  
        CantidadComensales = int(slider_valor.get())  

        if NombrePersona=="" and TelefonoPersona==""  :
                    messagebox.showerror("Error", "Nombre o Telefono no ingresado.")

        
        elif DiasData[DiaSeleccionado]["Lugares Disponibles"] >= CantidadComensales and  NombrePersona!="" and TelefonoPersona!=""      :
            DiasData[DiaSeleccionado]["Lugares Disponibles"] -= CantidadComensales
            DiasData[DiaSeleccionado]["Lugares Ocupados"] += CantidadComensales
            
            respuesta = messagebox.showinfo("Éxito", "Reserva realizada con éxito")
            
            if respuesta:
                GuardarDatosJSON([DiasData])
                
                NumeroReserva = GenerarNumeroReserva()

                datosRestaurante = (
                    f"Numero Reserva: {NumeroReserva}\n"
                    f"Nombre: {NombrePersona}\n"
                    f"Telefono: {TelefonoPersona}\n"
                    f"Mail: {MailUsuario}\n"
                    f"Día: {DiaSeleccionado}\n"
                    f"Numero de comensales: {CantidadComensales} \n"
                )

                datosReserva = {
                    "Numero Reserva": NumeroReserva,
                    "Nombre": NombrePersona,
                    "Telefono": TelefonoPersona,
                    "Mail": MailUsuario,
                    "Dia": DiaSeleccionado,
                    "Numero de comensales": CantidadComensales
                }

                try:
                    with open("src/JSON/ReservasRestaurante.json", "r") as archivo:
                        DatosReserva = json.load(archivo)
                except (FileNotFoundError, json.JSONDecodeError):
                    DatosReserva = []

                DatosReserva.append(datosReserva)

                try:
                    with open("src/JSON/ReservasRestaurante.json", "w") as archivo:
                        json.dump(DatosReserva, archivo, indent=4)
                    messagebox.showinfo("Éxito", "Reserva Confirmada")
                except IOError as e:
                    messagebox.showerror(f"Error al escribir el archivo: {e}")
                EnviarMail(MailUsuario, datosRestaurante , "Reserva Confirmada")
                
                ventanaReservas.destroy()
            elif NombrePersona=="" and TelefonoPersona==""  :
                    messagebox.showerror("Error", "Nombre o Apellido no ingresado.")
            else:
                messagebox.showerror("Error", "No hay suficientes lugares disponibles.")

    botonReserva= ctk.CTkButton(ventanaReservas, 
        text="Reservar",        
        command=reservaconexito,
        width=100,
        height=50,
        fg_color="#2FB166",
        border_width=0,
        border_color="black",
        corner_radius=0,
        hover_color="#2FB166",
        font=("Lalezar",25)
        )
    botonReserva.place(x=145, y=530) 

# ---------- PRECIOS ---------
def PantallaPrecios():
    global ventanaPrecios
    ventanaPrecios = Toplevel(ventanaPrincipal)
    ventanaPrecios.geometry("400x600")
    ventanaPrecios.title("Precios")
    ventanaPrecios.resizable(False, False)
    ventanaPrecios.transient(ventanaPrincipal)  
    ventanaPrecios.lift()  
    ventanaPrecios.focus_set()  
    ventanaPrecios.grab_set()

def Precios():
    global iPrecios , FondoPrecios
    CargarPrecios()
    PantallaPrecios()
    iPrecios = 0
    FondoPrecios = "src/Imagenes/Fondos/" + HojasPrecios[iPrecios] + ".png"
    PonerFondo(FondoPrecios, ventanaPrecios)
    BotonesMenu("HojasPrecios")

def CargarPrecios():
    global FondoPrecios
    Archivo = CargarArchivo("src/JSON/Precios.json")
    for Precios in Archivo:
        for Hoja , Info in Precios.items():
            if Hoja == "Futbol 5":
                for Horario , Precio in Info.items():
                    Futbol5[Horario] = Precio
            elif Hoja == "Futbol 8":
                for Horario , Precio in Info.items():
                    Futbol8[Horario] = Precio
            elif Hoja == "Tenis":
                for Horario , Precio in Info.items():
                    Tenis[Horario] = Precio
            elif Hoja == "Padel":
                for Horario , Precio in Info.items():
                    Padel[Horario] = Precio

def MostrarPrecios():
    global FondoPrecios
    YHorarios = 118
    YPrecios = 118
    if FondoPrecios == "src/Imagenes/Fondos/HojaFutbol5.png":
        for Producto, Precio in Futbol5.items():
            Horarios = ctk.CTkLabel(
                ventanaPrecios,
                text=f"{Producto}",
                text_color="black",
                fg_color="#2FB166",
                bg_color="#2FB166",
                corner_radius=0,
                font=("Lalezar", 20),
                anchor=ctk.W,
                justify='left'
            )
            Horarios.place(x=75, y=YHorarios)
            YHorarios += 50
            Precios = ctk.CTkLabel(
                ventanaPrecios,
                text=f"${Precio}",
                text_color="black",
                fg_color="#2FB166",
                bg_color="#2FB166",
                corner_radius=0,
                font=("Lalezar", 20),
                anchor=ctk.W,
                justify='right'
            )
            Precios.place(x=270, y=YPrecios)
            YPrecios += 50
    elif FondoPrecios == "src/Imagenes/Fondos/HojaFutbol8.png":
        for Producto, Precio in Futbol8.items():
            Horarios = ctk.CTkLabel(
                ventanaPrecios,
                text=f"{Producto}",
                text_color="black",
                fg_color="#2FB166",
                bg_color="#2FB166",
                corner_radius=0,
                font=("Lalezar", 20),
                anchor=ctk.W,
                justify='left'
            )
            Horarios.place(x=75, y=YHorarios)
            YHorarios += 50
            Precios = ctk.CTkLabel(
                ventanaPrecios,
                text=f"${Precio}",
                text_color="black",
                fg_color="#2FB166",
                bg_color="#2FB166",
                corner_radius=0,
                font=("Lalezar", 20),
                anchor=ctk.W,
                justify='right'
            )
            Precios.place(x=270, y=YPrecios)
            YPrecios += 50
    elif FondoPrecios == "src/Imagenes/Fondos/HojaTenis.png":
        for Producto, Precio in Tenis.items():
            Horarios = ctk.CTkLabel(
                ventanaPrecios,
                text=f"{Producto}",
                text_color="black",
                fg_color="#2FB166",
                bg_color="#2FB166",
                corner_radius=0,
                font=("Lalezar", 20),
                anchor=ctk.W,
                justify='left'
            )
            Horarios.place(x=75, y=YHorarios)
            YHorarios += 50
            Precios = ctk.CTkLabel(
                ventanaPrecios,
                text=f"${Precio}",
                text_color="black",
                fg_color="#2FB166",
                bg_color="#2FB166",
                corner_radius=0,
                font=("Lalezar", 20),
                anchor=ctk.W,
                justify='right'
            )
            Precios.place(x=270, y=YPrecios)
            YPrecios += 50
    elif FondoPrecios == "src/Imagenes/Fondos/HojaPadel.png":
        for Producto, Precio in Padel.items():
            Horarios = ctk.CTkLabel(
                ventanaPrecios,
                text=f"{Producto}",
                text_color="black",
                fg_color="#2FB166",
                bg_color="#2FB166",
                corner_radius=0,
                font=("Lalezar", 20),
                anchor=ctk.W,
                justify='left'
            )
            Horarios.place(x=75, y=YHorarios)
            YHorarios += 50
            Precios = ctk.CTkLabel(
                ventanaPrecios,
                text=f"${Precio}",
                text_color="black",
                fg_color="#2FB166",
                bg_color="#2FB166",
                corner_radius=0,
                font=("Lalezar", 20),
                anchor=ctk.W,
                justify='right'
            )
            Precios.place(x=270, y=YPrecios)
            YPrecios += 50

# ---------- BENEFICIOS ---------
def CrearBoton(x, y, text, command):
    button = ctk.CTkButton(
        ventanaPrincipal,
        text=text, 
        width=25,
        height=25,
        fg_color="#2FB166",
        bg_color="#2FB166",
        hover_color="#2FB163",  
        text_color="Black",
        command=command,
        font=("Lalezar", 20),
        corner_radius=0,
    )
    button.place(x=x, y=y) 
    return button  

def MostrarBotonesBeneficios():
    global PuntosClub
    pack2Hamburguesas = CrearBoton(240, 665,125,lambda: VerificarSaldo(125,"Hamburguesa"))  
    ppadel = CrearBoton(550, 665, "150", lambda: VerificarSaldo(150,"Padel 1 hora"))
    tenis1 = CrearBoton(860, 665, "150", lambda: VerificarSaldo(150,"Tenis 1 hora"))
    f5l = CrearBoton(1170, 665, "150", lambda: VerificarSaldo(150,"Futbol 1 hora"))
    papas = CrearBoton(240, 357, "30", lambda: VerificarSaldo(30,"Papas"))
    gorra = CrearBoton(550, 357, "75", lambda: VerificarSaldo(75,"Gorra Personalizada"))
    short = CrearBoton(860, 357, "100", lambda: VerificarSaldo(100,"Short Personalizado"))
    camiseta = CrearBoton(1170, 357, "125", lambda: VerificarSaldo(125,"Camizeta personalizada"))
    LabelPuntos = ctk.CTkLabel(
        ventanaPrincipal,
        text=PuntosClub, 
        text_color="BLACK",
        width=20,
        height=20,
        fg_color="#2FB166",
        font=("Lalezar", 20),
        anchor=ctk.W,
        justify='left'
    )
    LabelPuntos.place(x=1200, y=37)

    carrito=ctk.CTkButton(ventanaPrincipal,text="Carrito🛒",command=MostrarRecibo,font=("Lalezar",20), width=20,
        height=20,fg_color="#2FB166",text_color="black",corner_radius=0,hover_color="#2FB166",bg_color="#2FB166")
    carrito.place(x=1175, y=95)

def SaldoSuficiente():
    respuesta = messagebox.askyesno("Exito", "Compra realizada con exito \n ¿Deseas ver el recibo?")
    if respuesta:
        MostrarRecibo()        

def SaldoInsuficiente():
    messagebox.showerror("Error", f"Fondos Insuficientes")

def Beneficios():
    PonerFondo("src/Imagenes/Fondos/Beneficios.png" , ventanaPrincipal)
    BotonesSideBar()
    MostrarBotonesBeneficios()    

def ReciboPuntos():
    messagebox.showinfo("Exito", f"Compra realizada con exito")
    PonerFondo("src/Imagenes/Fondos/RECIBO FINAL.png" , ventanaPrincipal)

def VerificarSaldo(precio, nombre):
    compras.append((nombre, precio)) 
    messagebox.showinfo(f"Compra registrada: {nombre} - {precio}")
    messagebox.showinfo("Información", f"Has agregado {nombre} al carrito.")

def Pagar():
    global PuntosClub
    total = sum(precio for nombre, precio in compras)

    if PuntosClub < total:
        SaldoInsuficiente()
        compras.clear()
    else:
        PuntosClub -= total  
        ActualizarPuntos() 
        compras.clear() 
        messagebox.showinfo("Éxito", "Pago realizado con éxito.")

def ActualizarPuntos():
    global NombreUsuario , PuntosClub
    try:
        with open("src/JSON/Usuarios.json", "r") as Archivo:
            Datos = json.load(Archivo)
        for UsuarioRegistrado in Datos:
            if UsuarioRegistrado["Usuario"] == NombreUsuario:
                UsuarioRegistrado["Puntos"] = PuntosClub
                break
        with open("src/JSON/Usuarios.json", "w") as Archivo:
            json.dump(Datos, Archivo, indent=4)

    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo de usuarios no se encontró.")

def MostrarRecibo():
    ReciboVentana = Toplevel(ventanaPrincipal)
    ReciboVentana.title("Recibo de Compras")
    ReciboVentana.geometry("220x300")
    ReciboVentana.resizable(False, False)

    TextoRecibo = "\n".join(f"{nombre}: ${precio}" for nombre, precio in compras)
    LabelRecibo = tk.Label(ReciboVentana, text=TextoRecibo, width=40, justify="left", font=("Lalezar", 12))
    LabelRecibo.pack(pady=10)

    BotonSeguirComprando = ctk.CTkButton(ReciboVentana, text="Seguir Comprando", command=ReciboVentana.destroy)
    BotonSeguirComprando.pack(pady=5)

    BotonPagar = ctk.CTkButton(ReciboVentana, text="Pagar", command=lambda: [Pagar(), ReciboVentana.destroy()])
    BotonPagar.pack(pady=5)

# ---------- RESERVA DE CANCHAS ----------

global Cancha 

def GenerarNumeroReserva():
    return "".join([str(random.randint(0, 9)) for _ in range(4)])

def CargarCanchas(DeporteElegido):
    global NombreArchivo , ListaCanchas
    PonerFondo(f"src/Imagenes/Fondos/{DeporteElegido}.png" , ventanaPrincipal)
    BotonesSideBar()
    MostrarBotonReservas(DeporteElegido)
    DiaElegido = Dia.get()
    HorarioElegido = Horario.get()

    if DiaElegido != "Seleccione un Dia" and HorarioElegido != "Seleccione un Horario":
        NombreArchivo = f"src/JSON/{DeporteElegido}.json"
        ListaCanchas = CargarArchivo(NombreArchivo)
        if not ListaCanchas:
            return
        CanchasDisponibles = MostrarCanchasDisponibles(ListaCanchas, DiaElegido, HorarioElegido)
        Cancha.configure(values=CanchasDisponibles)

def PantallaFutbol():
    global DeporteElegido
    DeporteElegido = "Futbol"
    CargarCanchas(DeporteElegido)

def PantallaTenis():
    global DeporteElegido
    DeporteElegido = "Tenis"
    CargarCanchas(DeporteElegido)

def PantallaPadel():
    global DeporteElegido
    DeporteElegido = "Padel"
    CargarCanchas(DeporteElegido)

def MostrarBotonReservas(DeporteElegido):
    global Dia, Horario, Cancha

    OpcionesDia = [
        "Seleccione un Dia", 
        "Lunes", "Martes", "Miercoles", 
        "Jueves", "Viernes", "Sabado", "Domingo"]
    OpcionesHorario = [
        "Seleccione un Horario",                
        "08:00", "09:00" , "10:00", "11:00", "12:00", 
        "13:00", "14:00", "15:00", "16:00", "17:00", 
        "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"
        ]

    Dia = ctk.CTkOptionMenu(
        ventanaPrincipal, 
        values=OpcionesDia, 
        fg_color="#2FB166", 
        text_color="white", 
        height=45, 
        width=230, 
        bg_color="#2FB166",
        button_color="#2FB166",
        font=("Lalezar", 15),
        corner_radius=0,
        command=lambda *args: ActualizarCanchas(DeporteElegido),
        button_hover_color="#2FB166",
        dropdown_hover_color="#2FB166"
    )
    Dia.place(x=170, y=365)

    Horario = ctk.CTkOptionMenu(
        ventanaPrincipal,
        values=OpcionesHorario,
        fg_color="#2FB166",
        font=("Lalezar", 15),
        text_color="white",
        height=45,
        width=230,
        bg_color="#2FB166",
        button_color="#2FB166",
        corner_radius=0,
        command=lambda *args: ActualizarCanchas(DeporteElegido),
        button_hover_color="#2FB166",
        dropdown_hover_color="#2FB166"
    )
    Horario.place(x=570, y=365)

    Cancha = ctk.CTkOptionMenu( 
        ventanaPrincipal,
        values=["Seleccione una Cancha"],
        fg_color="#2FB166",
        font=("Lalezar", 15),
        text_color="white",
        height=45,
        bg_color="#2FB166",
        button_color="#2FB166",
        width=230,
        corner_radius=0,
        button_hover_color="#2FB166",
        dropdown_hover_color="#2FB166"
    )
    Cancha.place(x=1045, y=365)

    BotonSiguiente = ctk.CTkButton(
        ventanaPrincipal,
        text="SIGUIENTE",
        text_color="white",
        width=220,
        height=60,
        fg_color="#2FB166",
        corner_radius=0,
        hover_color="#065F2B",
        command=Reserva,
        font=("Lalezar", 20)
    )
    BotonSiguiente.place(x=580, y=660)

def ActualizarCanchas(DeporteElegido):
    global ListaCanchas , NombreArchivo
    """Actualiza las canchas disponibles según el día, horario y deporte seleccionados."""
    global CanchaElegida, DiaElegido, HorarioElegido
    DiaElegido = Dia.get()
    HorarioElegido = Horario.get()
    
    if DiaElegido != "Seleccione un Dia" and HorarioElegido != "Seleccione un Horario":
        NombreArchivo = DeporteElegido + ".json"
        ListaCanchas = CargarArchivo(NombreArchivo)
        if not ListaCanchas:
            return
        CanchasDisponibles = MostrarCanchasDisponibles(ListaCanchas, DiaElegido, HorarioElegido)
        Cancha.configure(values=CanchasDisponibles)
    CanchaElegida = Cancha.get()

def MostrarCanchasDisponibles(ListaCanchas, DiaElegido, HorarioElegido):
    CanchasDisponibles = []
    for Canchas in ListaCanchas:
        for Cancha, Datos in Canchas.items():
                if Datos[DiaElegido][HorarioElegido] == "Disponible":
                    CanchasDisponibles.append(Cancha)
    if CanchasDisponibles:
        return CanchasDisponibles
    else:
        messagebox.showerror("Ocupado" , f"No hay canchas disponibles para el {DiaElegido} a las {HorarioElegido}.")
        return []

def CargarDatosReserva():
    global Numero , Precio
    try:
        with open("src/JSON/Reservas.json", "r") as Archivo:
            DatosReserva = json.load(Archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        DatosReserva = []
    DatosReserva.append({
        "Numero Reserva": Numero,
        "Deporte": DeporteElegido,
        "Cancha": CanchaElegida,
        "Nombre": NombreUsuario,
        "Mail": MailUsuario,
        "Dia": DiaElegido,
        "Horario": HorarioElegido,
        "Precio": Precio,
        "Estado": "Pendiente"
    })
    try:
        with open("src/JSON/Reservas.json", "w") as Archivo:
            json.dump(DatosReserva, Archivo, indent=4)
    except IOError as e:
        messagebox.showerror(f"Error al escribir el archivo: {e}") 

def DesignarPrecios():
    global PrecioF5Dia, PrecioF5Noche , PrecioF8Dia, PrecioF8Noche , PrecioPadelDia, PrecioPadelNoche , PrecioTenisDia, PrecioTenisNoche
    Archivo = CargarArchivo("Precios.json")
    for Datos in Archivo:
        for Deporte, Dias in Datos.items():
            if Deporte == "Futbol 5":
                PrecioF5Dia = Dias.get("Dia")
                PrecioF5Noche = Dias.get("Noche")
            if Deporte == "Futbol 8":
                PrecioF8Dia = Dias.get("Dia")
                PrecioF8Noche = Dias.get("Noche")
            if Deporte == "Padel":
                PrecioPadelDia = Dias.get("Dia")
                PrecioPadelNoche = Dias.get("Noche")
            if Deporte == "Tenis":
                PrecioTenisDia = Dias.get("Dia")
                PrecioTenisNoche = Dias.get("Noche")

def EstablecerPrecio():
    global CanchaElegida, DiaElegido, HorarioElegido, DeporteElegido , Precio
    Precio = 0
    DesignarPrecios()
    Dia = ( 
        "08:00", "09:00", "10:00", "11:00", 
        "12:00", "13:00", "14:00", "15:00", 
        "16:00", "17:00"
    )
    Noche = (
        "18:00", "19:00", "20:00", "21:00", 
        "22:00", "23:00", "00:00"
    )
    CanchasFutbol5 = ("Cancha 1 (F5)" , "Cancha 2 (F5)" , "Cancha 3 (F5)" , "Cancha 4 (F5)" )
    CanchasFutbol8 = ("Cancha 5 (F8)" , "Cancha 6 (F8)")
    if DeporteElegido == "Futbol":
        if CanchaElegida in CanchasFutbol5:
                if HorarioElegido in Dia:
                    Precio = PrecioF5Dia
                if HorarioElegido in Noche:
                    Precio = PrecioF5Noche
        if CanchaElegida in CanchasFutbol8:
                if HorarioElegido in Dia:
                    Precio = PrecioF8Dia
                if HorarioElegido in Noche:
                    Precio = PrecioF8Noche
    if DeporteElegido == "Padel":
        if HorarioElegido in Dia:
            Precio = PrecioPadelDia
        if HorarioElegido in Noche:
            Precio = PrecioPadelNoche
    if DeporteElegido== "Tenis":
        if HorarioElegido in Dia:
            Precio = PrecioTenisDia
        if HorarioElegido in Noche:
            Precio = PrecioTenisNoche
    return Precio

def VentanaPago(Precio):
    global PagoRealizado, PrecioRestante, EstadoReserva, ActualizarEstadoReserva
    PrecioRestante = Precio
    
    CargarDatosReserva()  

    def ActualizarEstadoReserva(estado, NumeroReserva):
        """Actualiza el estado de la reserva en el archivo JSON"""
        try:
            with open("src/JSON/reservas.json", "r") as archivo:
                reservas = json.load(archivo)

            ReservaEncontrada = False
            for reserva in reservas:
                if str(reserva["Numero Reserva"]) == str(NumeroReserva): 
                    reserva["Estado"] = estado  
                    ReservaEncontrada = True
                    break

            if not ReservaEncontrada:
                messagebox.showerror("Error", "Reserva no encontrada.")
                return

            with open("src/JSON/reservas.json", "w") as archivo:
                json.dump(reservas, archivo, indent=4)

        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo de reservas.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar el estado de la reserva: {e}")

    def ProcesarSeña():
        global PagoRealizado, EstadoReserva, PrecioRestante
        Seña = Precio / 3
        Seña = round(Seña)
        EstadoReserva = "Señada"
        PrecioRestante = Precio - Seña
        PagoRealizado = True
        ActualizarEstadoReserva(EstadoReserva, Numero)
        MostrarQR()
        ventanaPago.destroy()

    def ProcesarPagoTotal():
        global PagoRealizado, EstadoReserva
        EstadoReserva = "Pagada"
        PagoRealizado = True
        ActualizarEstadoReserva(EstadoReserva, Numero)
        MostrarQR()
        ventanaPago.destroy()

    ventanaPago = ctk.CTkToplevel(ventanaPrincipal)
    ventanaPago.title("Confirmar Pago") 
    ventanaPago.geometry("400x300")
    ventanaPago.resizable(False, False)
    ventanaPago.transient(ventanaPrincipal)  
    ventanaPago.lift()  
    ventanaPago.focus_set()  
    ventanaPago.grab_set()
    etiquetaPago = ctk.CTkLabel(
        ventanaPago,
        text=f"Total a pagar: ${Precio}", 
        font=("Lalezar", 20)
    )
    etiquetaPago.pack(pady=20)

    botonSeñar = ctk.CTkButton(
        ventanaPago, 
        text="Señar", 
        command=ProcesarSeña, 
        width=220, height=60, fg_color="#2FB166", font=("Lalezar", 20), corner_radius=0)
    botonSeñar.pack(pady=10)

    botonPagarTotal = ctk.CTkButton(ventanaPago, text="Pagar Total", command=ProcesarPagoTotal, width=220, height=60, fg_color="#2FB166", font=("Lalezar", 20), corner_radius=0)
    botonPagarTotal.pack(pady=10)

    ventanaPago.mainloop()

def MostrarQR():
    """Genera un QR con los detalles del pago (incluyendo el resto a pagar)"""
    global EstadoReserva, PrecioRestante , ventanaQR

    ventanaQR = Toplevel(ventanaPrincipal)
    ventanaQR.title("QR") 
    ventanaQR.geometry("400x400")
    ventanaQR.resizable(False, False)
    ventanaQR.transient(ventanaPrincipal)  
    ventanaQR.configure(background="black")
    ventanaQR.lift()  
    ventanaQR.focus_set()  
    ventanaQR.grab_set()

    if EstadoReserva == "Señada":
        monto = PrecioRestante
    else:
        monto = Precio  

    DataQR = f"Transferir ${monto} a la cuenta: 123-456-789"
    qr = qrcode.make(DataQR)

    qr_image_path = "qr_pago.png"
    qr.save(qr_image_path)

    imagen_pil = Image.open(qr_image_path)

    imagenQR = ctk.CTkImage(light_image=imagen_pil, dark_image=imagen_pil, size=(200, 200))

    LabelQR = ctk.CTkLabel(ventanaQR, image=imagenQR)
    LabelQR.place(x=100, y=50)

    botonConfirmarPago = ctk.CTkButton(
        ventanaQR, 
        text="Confirmar Pago", 
        command=ConfirmarPago, 
        width=100, height=60, 
        fg_color="#2FB166", 
        font=("Lalezar", 20), 
        corner_radius=20)
    botonConfirmarPago.place(x=150, y=300)

def ConfirmarPago():
    global PagoRealizado, EstadoReserva, Numero, DatosReserva, Precio
    ventanaQR.destroy()
    if not PagoRealizado:
        messagebox.showerror("Error", "Debe realizar el pago antes de confirmar la reserva.")
        return
    if EstadoReserva == "Señada":
        messagebox.showinfo("Reserva Señada", "Reserva señada con éxito. El resto del pago se debe abonar previo a jugar")
    elif EstadoReserva == "Pagada":
        messagebox.showinfo("Reserva Confirmada", "Reserva pagada y confirmada con éxito.")
    botonConfirmarReserva = ctk.CTkButton(
        ventanaPrincipal, 
        text="Confirmar Reserva", 
        command=ConfirmarReserva, 
        width=220, 
        height=60, 
        fg_color="#2FB166", 
        font=("Lalezar", 20), 
        corner_radius=0
        )
    botonConfirmarReserva.place(x=570, y=660)   

def ConfirmarReserva():
    global DatosReserva , PuntosClub
    PuntosClub = PuntosClub+10
    try:
        with open("src/JSON/Usuarios.json", "r") as Archivo:
            Datos = json.load(Archivo)

        for UsuarioRegistrado in Datos:
            if UsuarioRegistrado["Usuario"] == NombreUsuario:
                UsuarioRegistrado["Puntos"] = PuntosClub
                break

        with open("src/JSON/Usuarios.json", "w") as Archivo:
            json.dump(Datos, Archivo, indent=4)
        
        messagebox.showinfo("Éxito", "Los puntos han sido actualizados.")

    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo de usuarios no se encontró.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al actualizar los puntos: {e}")
    
    for Canchas in ListaCanchas:
        if CanchaElegida in Canchas:
            Canchas[CanchaElegida][DiaElegido][HorarioElegido] = "Reservada"
            break
    with open(NombreArchivo, "w") as Archivo:
        json.dump(ListaCanchas, Archivo, indent=4)
    messagebox.showinfo("Reserva Confirmada" , "Le enviaremos un mail con los datos de su reserva")
    EnviarMail(MailUsuario , DatosReserva, "Reserva Confirmada")
    PonerFondo("src/Imagenes/Fondos/PantallaPrincipal.png" , ventanaPrincipal )
    BotonesSideBar()

def ActualizarPuntosUsuario():
    global PuntosClub, NombreUsuario
    try:
        with open("src/JSON/Usuarios.json", "r") as Archivo:
            Datos = json.load(Archivo)

        for UsuarioRegistrado in Datos:
            if UsuarioRegistrado["Usuario"] == NombreUsuario:
                UsuarioRegistrado["Puntos"] = PuntosClub
                break

        with open("src/JSON/Usuarios.json", "w") as Archivo:
            json.dump(Datos, Archivo, indent=4)

        messagebox.showinfo("Éxito", "Los puntos han sido actualizados.")
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo de usuarios no se encontró.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al actualizar los puntos: {e}")

def Reserva():
    global CanchaElegida, DiaElegido, HorarioElegido, DeporteElegido, ListaCanchas, NombreArchivo , DatosReserva , Numero , EstadoReserva
    CanchaElegida = Cancha.get()
    DiaElegido = Dia.get()
    HorarioElegido = Horario.get()
    EstadoReserva = "Pendiente"
    PagoRealizado = False

    if CanchaElegida != "Seleccione una Cancha" and DiaElegido != "Seleccione un Dia" and HorarioElegido != "Seleccione un Horario" and DeporteElegido:
        try:
            PonerFondo("src/Imagenes/Fondos/Reserva.png", ventanaPrincipal)
            BotonesSideBar()
            Numero = GenerarNumeroReserva()
            Precio = EstablecerPrecio()
            DatosReserva = (
                f"Numero Reserva: {Numero}\n"
                f"Nombre: {NombreUsuario}\n"
                f"Mail: {MailUsuario}\n"
                f"Deporte: {DeporteElegido}\n"
                f"Día: {DiaElegido}\n"
                f"Horario: {HorarioElegido}\n"
                f"Cancha: {CanchaElegida}\n"
                f"Precio: ${Precio}\n"
                f"Estado: Pendiente\n"
            )
            texto = ctk.CTkLabel(
                ventanaPrincipal,
                text=DatosReserva,
                text_color="white",
                width=350,
                height=350,
                fg_color="#2FB166",
                font=("Lalezar", 20),
                anchor=ctk.W,
                justify='left'
            )
            texto.place(x=510, y=225)

            BotonRealizarPago = ctk.CTkButton(ventanaPrincipal, 
                text="Realizar Pago",
                command=lambda: VentanaPago(Precio), 
                width=220,
                height=60,
                fg_color="#2FB166",
                font=("Lalezar", 20),
                corner_radius=0,
                hover_color="#2FB166"
            )
            
            
            if PagoRealizado:
                BotonRealizarPago.place_forget()
            else:
                BotonRealizarPago.place(x=570, y=660)
            
        except Exception as e:
                messagebox.showerror("ERROR" , f"Error en la reserva: {e}")
    else:
        messagebox.showerror("Error", "Seleccione Datos Validos")


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
# ---------- INICIO ----------
def Inicio():
    global NombreUsuario, MailUsuario, PuntosClub , ImagenPerfil
    NombreUsuario = ""
    MailUsuario = ""
    PonerFondo("src/Imagenes/Fondos/Inicio.png", ventanaPrincipal)
    IniciarSesionButton = ctk.CTkButton(
        ventanaPrincipal,
        text="Iniciar Sesion",
        text_color="white",
        width=220,
        height=60,
        fg_color="#2FB166",
        corner_radius=0,
        hover_color="#2FB166",
        command=FondoIniciarSesion,
        font=("Lalezar", 20)
    )

    CrearCuentaButton = ctk.CTkButton(
        ventanaPrincipal,
        text="Crear Cuenta",
        text_color="white",
        width=220,
        height=60,
        fg_color="#2FB166",
        corner_radius=0,
        hover_color="#2FB166",
        command=MostrarFormularioCrearCuenta,
        font=("Lalezar", 20)
    )
    IniciarSesionButton.place(x=215, y=355)
    CrearCuentaButton.place(x=933, y=355)

    ImgCerrar = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonCerrar.png"), size=(40, 50))
    BotonCerrar = ctk.CTkButton(ventanaPrincipal, 
        text="",        
        image=ImgCerrar,
        command=Cerrar,
        width=50,
        height=20,
        fg_color="#2FB166",
        bg_color="black",
        border_width=0,
        corner_radius=90,
        hover_color="#2FB166"
        )
    BotonCerrar.place(x=10, y=10)

# ---------- MAIN ----------
Inicio()
compras = []
ventanaPrincipal.mainloop()