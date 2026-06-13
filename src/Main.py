import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
import json
import uuid
import bcrypt
import os
from dotenv import load_dotenv
from tkinter import messagebox, Toplevel, filedialog
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import qrcode

load_dotenv()
EMAIL_REMITENTE = os.getenv("EMAIL_REMITENTE")
EMAIL_CONTRASENA = os.getenv("EMAIL_CONTRASENA")

ventana_principal = ctk.CTk()
ventana_principal.geometry("1366x768")
ventana_principal.title("El ANDEN")
ventana_principal.resizable(False, False)
ventana_principal.attributes("-fullscreen", False)

# Variables globales de sesión
nombre_usuario = ""
mail_usuario = ""
puntos_club = 0
imagen_perfil = ""

# Listas de hojas
hojas_menu = ["Menu", "Entradas", "Principal", "Bebidas", "Postres"]
hojas_precios = ["Precios", "HojaFutbol5", "HojaFutbol8", "HojaTenis", "HojaPadel"]

# Diccionarios de productos
entradas = {}
principales = {}
bebidas = {}
postres = {}
futbol5 = {}
futbol8 = {}
padel = {}
tenis = {}

# Carrito de beneficios
compras = []

# ---------- SESIÓN (validación global) ----------
def sesion_activa():
    """Verifica que haya un usuario logueado antes de navegar."""
    if not mail_usuario:
        messagebox.showerror("Sesión", "Debés iniciar sesión primero.")
        return False
    return True

# ---------- GENERALES ----------
def poner_fondo(imagen_ruta, ventana):
    imagen = Image.open(imagen_ruta)
    imagen_tk = ImageTk.PhotoImage(imagen)
    label_fondo = ctk.CTkLabel(ventana, image=imagen_tk, text="")
    label_fondo.image = imagen_tk
    label_fondo.place(x=0, y=0)

def pantalla_principal():
    poner_fondo("src/Imagenes/Fondos/PantallaPrincipal.png", ventana_principal)
    botones_sidebar()

def botones_sidebar():
    img_logo = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonLogo.png"), size=(50, 70))
    ctk.CTkButton(ventana_principal, text="", command=pantalla_principal,
                  image=img_logo, width=50, height=70, fg_color="#2FB166",
                  border_width=0, corner_radius=0, hover_color="#2FB166").place(x=10, y=10)

    img_perfil = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonIcono.png"), size=(50, 50))
    ctk.CTkButton(ventana_principal, text="", image=img_perfil,
                  command=lambda: perfil() if sesion_activa() else None,
                  width=50, height=50, fg_color="#2FB166",
                  border_width=0, corner_radius=0, hover_color="#2FB166").place(x=10, y=85)

    img_precios = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonPrecios.png"), size=(50, 50))
    ctk.CTkButton(ventana_principal, text="", image=img_precios, command=precios,
                  width=50, height=50, fg_color="#2FB166",
                  border_width=0, corner_radius=0, hover_color="#2FB166").place(x=10, y=170)

    img_futbol = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonFutbol.png"), size=(50, 50))
    ctk.CTkButton(ventana_principal, text="", image=img_futbol,
                  command=lambda: pantalla_futbol() if sesion_activa() else None,
                  width=50, height=50, fg_color="#2FB166",
                  border_width=0, corner_radius=0, hover_color="#2FB166").place(x=10, y=255)

    img_tenis = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonTenis.png"), size=(50, 50))
    ctk.CTkButton(ventana_principal, text="", image=img_tenis,
                  command=lambda: pantalla_tenis() if sesion_activa() else None,
                  width=50, height=50, fg_color="#2FB166",
                  border_width=0, corner_radius=0, hover_color="#2FB166").place(x=10, y=340)

    img_padel = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonPadel.png"), size=(50, 50))
    ctk.CTkButton(ventana_principal, text="", image=img_padel,
                  command=lambda: pantalla_padel() if sesion_activa() else None,
                  width=50, height=50, fg_color="#2FB166",
                  border_width=0, corner_radius=0, hover_color="#2FB166").place(x=10, y=425)

    img_restaurant = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonRestaurant.png"), size=(50, 50))
    ctk.CTkButton(ventana_principal, text="", image=img_restaurant, command=restaurant,
                  width=50, height=50, fg_color="#2FB166",
                  border_width=0, corner_radius=0, hover_color="#2FB166").place(x=10, y=510)

    img_shop = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonShop.png"), size=(50, 50))
    ctk.CTkButton(ventana_principal, text="", image=img_shop,
                  command=lambda: beneficios() if sesion_activa() else None,
                  width=50, height=50, fg_color="#2FB166",
                  border_width=0, corner_radius=0, hover_color="#2FB166").place(x=10, y=595)

    img_cerrar = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonCerrar.png"), size=(50, 50))
    ctk.CTkButton(ventana_principal, text="", image=img_cerrar, command=cerrar,
                  width=50, height=50, fg_color="#2FB166",
                  border_width=0, corner_radius=0, hover_color="#2FB166").place(x=10, y=680)

def cerrar():
    if messagebox.askyesno("Cerrar Programa", "¿Seguro querés cerrar el programa?"):
        ventana_principal.destroy()

def siguiente(tipo_hoja):
    global i_menu, fondo_menu, i_precios, fondo_precios
    if tipo_hoja == "HojasMenu":
        i_menu += 1
        fondo_menu = "src/Imagenes/Fondos/" + hojas_menu[i_menu] + ".png"
        poner_fondo(fondo_menu, ventana_menu)
        botones_menu(tipo_hoja)
        mostrar_menu()
    if tipo_hoja == "HojasPrecios":
        i_precios += 1
        fondo_precios = "src/Imagenes/Fondos/" + hojas_precios[i_precios] + ".png"
        poner_fondo(fondo_precios, ventana_precios)
        botones_menu(tipo_hoja)
        mostrar_precios()

def atras(tipo_hoja):
    global i_menu, fondo_menu, i_precios, fondo_precios
    if tipo_hoja == "HojasMenu":
        i_menu -= 1
        fondo_menu = "src/Imagenes/Fondos/" + hojas_menu[i_menu] + ".png"
        poner_fondo(fondo_menu, ventana_menu)
        botones_menu(tipo_hoja)
        mostrar_menu()
    if tipo_hoja == "HojasPrecios":
        i_precios -= 1
        fondo_precios = "src/Imagenes/Fondos/" + hojas_precios[i_precios] + ".png"
        poner_fondo(fondo_precios, ventana_precios)
        botones_menu(tipo_hoja)
        mostrar_precios()

def cargar_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, "r") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        messagebox.showerror("Error", f"Error al leer el archivo: {e}")
        return []

# ---------- SEGURIDAD: HASH DE CONTRASEÑAS ----------
def hashear_contrasena(contrasena):
    return bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verificar_contrasena(contrasena, hash_guardado):
    try:
        return bcrypt.checkpw(contrasena.encode("utf-8"), hash_guardado.encode("utf-8"))
    except Exception:
        # Compatibilidad con contraseñas antiguas en texto plano
        return contrasena == hash_guardado

# ---------- REGISTRO E INICIO DE SESIÓN ----------
def mail_registrado(mail):
    try:
        with open("src/JSON/Usuarios.json", "r") as archivo:
            datos = json.load(archivo)
        return any(mail.lower() == d["Mail"].lower() for d in datos)
    except (FileNotFoundError, Exception) as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
        return False

def fondo_iniciar_sesion():
    poner_fondo("src/Imagenes/Fondos/IniciarSesion.png", ventana_principal)
    mostrar_formulario_iniciar_sesion()

def mostrar_formulario_crear_cuenta():
    for widget in ventana_principal.winfo_children():
        widget.destroy()
    poner_fondo("src/Imagenes/Fondos/CrearCuenta.png", ventana_principal)

    img_back = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonBack.png"), size=(50, 50))
    ctk.CTkButton(ventana_principal, text="", image=img_back, command=inicio,
                  width=50, height=50, fg_color="black", border_width=0, corner_radius=0).place(x=10, y=20)

    entry_usuario = ctk.CTkEntry(ventana_principal, width=400, font=("Lalezar", 25),
                                 placeholder_text="Ingrese el usuario", fg_color="white",
                                 corner_radius=0, border_color="white", text_color="Black")
    entry_usuario.place(x=515, y=345)

    entry_mail = ctk.CTkEntry(ventana_principal, width=400, font=("Lalezar", 25),
                              placeholder_text="Ingrese el mail", fg_color="white",
                              corner_radius=0, border_color="white", text_color="Black")
    entry_mail.place(x=515, y=450)

    entry_contrasena = ctk.CTkEntry(ventana_principal, show="*", width=400, font=("Lalezar", 25),
                                    placeholder_text="Ingrese la contraseña", fg_color="white",
                                    corner_radius=0, border_color="white", text_color="Black")
    entry_contrasena.place(x=515, y=550)

    ctk.CTkButton(ventana_principal, text="Crear Cuenta",
                  command=lambda: crear_cuenta(entry_usuario.get(), entry_mail.get(), entry_contrasena.get()),
                  font=("Lalezar", 30), width=220, height=60, fg_color="#2FB166",
                  corner_radius=0, hover_color="#2FB166").place(x=720, y=670)

    ctk.CTkButton(ventana_principal, text="Iniciar Sesión", command=mostrar_formulario_iniciar_sesion,
                  font=("Lalezar", 30), width=220, height=60, fg_color="#2FB166",
                  corner_radius=0, hover_color="#2FB166").place(x=430, y=670)

def mostrar_formulario_iniciar_sesion():
    for widget in ventana_principal.winfo_children():
        widget.destroy()
    poner_fondo("src/Imagenes/Fondos/IniciarSesion.png", ventana_principal)

    img_back = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonBack.png"), size=(50, 50))
    ctk.CTkButton(ventana_principal, text="", image=img_back, command=inicio,
                  width=50, height=50, fg_color="black", border_width=0, corner_radius=0).place(x=10, y=20)

    entry_mail = ctk.CTkEntry(ventana_principal, width=400, font=("Lalezar", 25),
                              placeholder_text="Ingrese el mail", fg_color="white",
                              corner_radius=0, border_color="white", text_color="Black")
    entry_mail.place(x=515, y=435)

    entry_contrasena = ctk.CTkEntry(ventana_principal, show="*", width=400, font=("Lalezar", 25),
                                    placeholder_text="Ingrese la contraseña", fg_color="white",
                                    corner_radius=0, border_color="white", text_color="Black")
    entry_contrasena.place(x=515, y=535)

    ctk.CTkButton(ventana_principal, text="Iniciar Sesión",
                  command=lambda: iniciar_sesion(entry_mail.get(), entry_contrasena.get()),
                  font=("Lalezar", 30), width=220, height=60, fg_color="#2FB166",
                  corner_radius=0, hover_color="#2FB166").place(x=720, y=670)

    ctk.CTkButton(ventana_principal, text="Crear Cuenta", command=mostrar_formulario_crear_cuenta,
                  font=("Lalezar", 30), width=220, height=60, fg_color="#2FB166",
                  corner_radius=0, hover_color="#2FB166").place(x=430, y=670)

def iniciar_sesion(mail, contrasena):
    global nombre_usuario, mail_usuario, puntos_club, imagen_perfil
    try:
        with open("src/JSON/Usuarios.json", "r") as archivo:
            datos = json.load(archivo)
        for usuario in datos:
            if mail.lower() == usuario["Mail"].lower():
                if verificar_contrasena(contrasena, usuario["Clave"]):
                    nombre_usuario = usuario["Usuario"]
                    mail_usuario = usuario["Mail"]
                    puntos_club = usuario["Puntos"]
                    imagen_perfil = usuario["Imagen"]
                    messagebox.showinfo("Éxito", "Inicio de Sesión Exitoso")
                    poner_fondo("src/Imagenes/Fondos/PantallaPrincipal.png", ventana_principal)
                    botones_sidebar()
                    return
        messagebox.showerror("Error", "Mail o Contraseña Incorrectos")
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo de usuarios no se encontró.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

def crear_cuenta(usuario, mail, contrasena):
    global nombre_usuario, mail_usuario, puntos_club, imagen_perfil
    if not usuario or not mail or not contrasena:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return
    if mail_registrado(mail):
        messagebox.showerror("Error", "Este mail ya está registrado.")
        return
    try:
        with open("src/JSON/Usuarios.json", "r") as archivo:
            datos = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        datos = []

    nombre_usuario = usuario
    mail_usuario = mail
    puntos_club = 0
    imagen_perfil = "src/Imagenes/FotosPerfil/Inicial.png"
    hash_clave = hashear_contrasena(contrasena)

    datos.append({
        "Usuario": nombre_usuario,
        "Mail": mail_usuario,
        "Clave": hash_clave,
        "Imagen": imagen_perfil,
        "Puntos": puntos_club
    })
    try:
        with open("src/JSON/Usuarios.json", "w") as archivo:
            json.dump(datos, archivo, indent=4)
        messagebox.showinfo("Éxito", "Usuario registrado con éxito.")
        poner_fondo("src/Imagenes/Fondos/PantallaPrincipal.png", ventana_principal)
        botones_sidebar()
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar el usuario: {e}")

# ---------- PERFIL ----------
def perfil():
    poner_fondo("src/Imagenes/Fondos/Perfil.png", ventana_principal)
    botones_sidebar()
    botones_perfil()
    mostrar_datos_perfil()
    mostrar_imagen_perfil()
    botones_modificar_datos()

def mostrar_datos_perfil():
    datos_perfil = (
        f"Nombre: {nombre_usuario}\n"
        f"Mail: {mail_usuario}\n"
        f"Contraseña: ******\n"
        f"Puntos: {puntos_club}\n"
    )
    ctk.CTkLabel(ventana_principal, text=datos_perfil, text_color="white",
                 bg_color="#2FB166", width=620, height=100, fg_color="#2FB166",
                 font=("Lalezar", 18), anchor=ctk.W, justify='left').place(x=495, y=185)

def botones_perfil():
    ctk.CTkButton(ventana_principal, text="Cambiar", text_color="white", width=100, height=30,
                  fg_color="#2FB166", bg_color="#2FB166", corner_radius=0,
                  hover_color="#2FB166", command=cargar_imagen_perfil,
                  font=("Lalezar", 18)).place(x=260, y=345)

    ctk.CTkButton(ventana_principal, text="Ver Reservas", text_color="white", width=220, height=60,
                  fg_color="#2FB166", corner_radius=0, hover_color="#2FB166",
                  command=lambda: seleccion_tipo_reserva("Ver"),
                  font=("Lalezar", 25)).place(x=575, y=460)

    ctk.CTkButton(ventana_principal, text="Cancelar Reserva", text_color="white", width=220, height=60,
                  fg_color="#2FB166", corner_radius=0, hover_color="#2FB166",
                  command=lambda: seleccion_tipo_reserva("Cancelar"),
                  font=("Lalezar", 25)).place(x=575, y=570)

    ctk.CTkButton(ventana_principal, text="Cerrar Sesion", text_color="white", width=220, height=60,
                  fg_color="#2FB166", corner_radius=0, hover_color="#2FB166",
                  command=cerrar_sesion, font=("Lalezar", 25)).place(x=575, y=675)

def botones_modificar_datos():
    for texto, comando, y in [
        ("Cambiar", cambiar_nombre, 185),
        ("Cambiar", cambiar_gmail, 210),
        ("Cambiar", cambiar_contrasena, 240),
    ]:
        ctk.CTkButton(ventana_principal, command=comando, text=texto, text_color="white",
                      fg_color="#2FB166", bg_color="#2FB166", width=50, height=20,
                      font=("Lalezar", 15), corner_radius=0,
                      hover_color="#2FB166").place(x=1050, y=y)

def _ventana_cambiar_dato(titulo, label_texto, mostrar=""):
    """Ventana genérica para cambiar un dato del perfil. Retorna el valor ingresado."""
    resultado = {"valor": None}
    ventana = ctk.CTkToplevel(ventana_principal)
    ventana.geometry("250x100")
    ventana.title(titulo)
    ventana.resizable(False, False)
    ventana.transient(ventana_principal)
    ventana.lift()
    ventana.focus_set()
    ventana.grab_set()

    ctk.CTkLabel(ventana, text=label_texto).place(x=30, y=5)
    entrada = ctk.CTkEntry(ventana, height=20, width=120, show=mostrar,
                           corner_radius=0, font=("Lalezar", 12))
    entrada.place(x=65, y=40)

    def guardar():
        resultado["valor"] = entrada.get()
        ventana.destroy()

    ctk.CTkButton(ventana, text="Guardar", command=guardar, height=20, width=50,
                  text_color="white", fg_color="#2FB166", bg_color="#2FB166",
                  corner_radius=0, font=("Lalezar", 12)).place(x=100, y=70)
    ventana.wait_window()
    return resultado["valor"]

def _actualizar_campo_usuario(campo, nuevo_valor):
    """Actualiza un campo del usuario en el JSON buscando por mail actual."""
    try:
        with open("src/JSON/Usuarios.json", "r") as archivo:
            datos = json.load(archivo)
        for usuario in datos:
            if usuario["Mail"] == mail_usuario:
                usuario[campo] = nuevo_valor
                break
        with open("src/JSON/Usuarios.json", "w") as archivo:
            json.dump(datos, archivo, indent=4)
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo de usuarios no se encontró.")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "El archivo de usuarios está corrupto.")

def cambiar_nombre():
    global nombre_usuario
    nuevo = _ventana_cambiar_dato("Cambiar Nombre", "Ingresar Nuevo Nombre")
    if nuevo:
        _actualizar_campo_usuario("Usuario", nuevo)
        nombre_usuario = nuevo
        messagebox.showinfo("Éxito", "Nombre modificado correctamente.")
        perfil()

def cambiar_gmail():
    global mail_usuario
    nuevo = _ventana_cambiar_dato("Cambiar Mail", "Ingrese Nuevo Mail")
    if nuevo:
        _actualizar_campo_usuario("Mail", nuevo)
        mail_usuario = nuevo
        messagebox.showinfo("Éxito", "Mail modificado correctamente.")
        perfil()

def cambiar_contrasena():
    nueva = _ventana_cambiar_dato("Cambiar Contraseña", "Nueva Contraseña", mostrar="*")
    if nueva:
        _actualizar_campo_usuario("Clave", hashear_contrasena(nueva))
        messagebox.showinfo("Éxito", "Contraseña modificada correctamente.")

def mostrar_imagen_perfil():
    if imagen_perfil:
        try:
            image = Image.open(imagen_perfil).resize((185, 185), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            label = ctk.CTkLabel(ventana_principal, image=photo, text="")
            label.image = photo
            label.place(x=220, y=125)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

def cargar_imagen_perfil():
    global imagen_perfil
    ruta = filedialog.askopenfilename(title="Seleccioná una imagen",
                                      filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    if ruta:
        try:
            image = Image.open(ruta).resize((185, 185), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            label = ctk.CTkLabel(ventana_principal, image=photo, text="")
            label.image = photo
            label.place(x=220, y=125)
            imagen_perfil = ruta
            _actualizar_campo_usuario("Imagen", ruta)
            messagebox.showinfo("Éxito", "Imagen de perfil actualizada.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

def cerrar_sesion():
    global nombre_usuario, mail_usuario, puntos_club, imagen_perfil
    if messagebox.askyesno("Cerrar Sesión", "¿Seguro querés cerrar sesión?"):
        nombre_usuario = ""
        mail_usuario = ""
        puntos_club = 0
        imagen_perfil = ""
        inicio()

# ---------- GESTIÓN DE RESERVAS ----------
def pantalla_ver_reservas():
    global ventana_reservas
    ventana_reservas = Toplevel(ventana_principal)
    ventana_reservas.title("Reservas")
    ventana_reservas.geometry("950x650")
    ventana_reservas.resizable(False, False)
    ventana_reservas.configure(background="black")

def leer_reservas_json(archivo_json):
    try:
        with open(archivo_json, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)
        return pd.DataFrame(data)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        messagebox.showerror("ERROR", f"Error al leer el archivo: {e}")
        return pd.DataFrame()

def tabla_reservas(nombre_archivo_reservas):
    global frame_busqueda, frame_tabla, buscar_deporte, buscar_cancha, buscar_dia, buscar_numero

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview.Heading", background="#2FB166", foreground="black")
    style.configure("Custom.Treeview", background="black", foreground="white",
                    fieldbackground="black", highlightthickness=0, bd=1, relief="solid")
    style.map("Custom.Treeview", background=[("selected", "#2FB166")])

    frame_tabla = ctk.CTkFrame(ventana_reservas, fg_color="black")
    frame_tabla.pack(fill="both", expand=True)

    frame_busqueda = ctk.CTkFrame(ventana_reservas, fg_color="black")
    frame_busqueda.pack(pady=10)

    campos = [("Número de Reserva", "buscar_numero"), ("Deporte", "buscar_deporte"),
              ("Dia", "buscar_dia"), ("Cancha", "buscar_cancha")]

    entries = {}
    for placeholder, key in campos:
        e = ctk.CTkEntry(frame_busqueda, width=175, height=30, placeholder_text=placeholder,
                         placeholder_text_color="white", text_color="white",
                         border_width=2, border_color="#2FB166", fg_color="#2FB166")
        e.pack(side="left", padx=10)
        entries[key] = e

    buscar_numero = entries["buscar_numero"]
    buscar_deporte = entries["buscar_deporte"]
    buscar_dia = entries["buscar_dia"]
    buscar_cancha = entries["buscar_cancha"]

    if nombre_archivo_reservas == "src/JSON/ReservasRestaurante.json":
        buscar_cancha.pack_forget()
        buscar_deporte.pack_forget()

    ctk.CTkButton(frame_busqueda, text="Buscar", width=175, height=30,
                  command=buscar_reserva, fg_color="#2FB166", text_color="white",
                  bg_color="black").pack(side="left", padx=10)

def mostrar_datos(df):
    for widget in frame_tabla.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(frame_tabla, style="Custom.Treeview")
    tree.pack(fill="both", expand=True, side="left")

    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    ancho_columnas = {"Numero Reserva": 30, "Deporte": 20, "Cancha": 50,
                      "Nombre": 20, "Gmail": 600, "Dia": 20, "Horario": 20,
                      "Precio": 20, "Estado": 30}

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=ancho_columnas.get(col, 100), anchor="center")

    tree.tag_configure("data_row", background="black", foreground="white")
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row), tags=("data_row",))

def buscar_reserva():
    hojas = leer_reservas_json(nombre_archivo_reservas)
    resultado = hojas[hojas['Mail'] == mail_usuario]

    filtros = [
        (buscar_numero.get(), 'Numero Reserva', True),
        (buscar_cancha.get(), 'Cancha', False),
        (buscar_dia.get(), 'Dia', False),
        (buscar_deporte.get(), 'Deporte', False),
    ]
    for valor, columna, exacto in filtros:
        if valor and columna in resultado.columns:
            if exacto:
                resultado = resultado[resultado[columna].astype(str) == valor]
            else:
                resultado = resultado[resultado[columna].str.contains(valor, case=False)]

    mostrar_datos(resultado)

def ver_reservas(tipo_reserva_seleccionado):
    global nombre_archivo_reservas
    if not tipo_reserva_seleccionado:
        messagebox.showerror("ERROR", "Debe seleccionar un tipo de reserva.")
        return
    ventana_seleccion.destroy()
    nombre_archivo_reservas = ("src/JSON/Reservas.json" if tipo_reserva_seleccionado == "Canchas"
                               else "src/JSON/ReservasRestaurante.json")
    pantalla_ver_reservas()
    tabla_reservas(nombre_archivo_reservas)
    hojas = leer_reservas_json(nombre_archivo_reservas)
    if not hojas.empty:
        mostrar_datos(hojas[hojas['Mail'] == mail_usuario])
    else:
        messagebox.showerror("ERROR", "No hay datos disponibles.")

def seleccion_tipo_reserva(destino_reserva):
    global ventana_seleccion
    ventana_seleccion = Toplevel(ventana_principal)
    ventana_seleccion.title("Tipo de Reserva")
    ventana_seleccion.geometry("200x300")
    ventana_seleccion.resizable(False, False)
    ventana_seleccion.transient(ventana_principal)
    ventana_seleccion.lift()
    ventana_seleccion.focus_set()
    ventana_seleccion.grab_set()
    ventana_seleccion.configure(background="black")

    funcion = {"Cancelar": cancelar_reserva, "Ver": ver_reservas}.get(destino_reserva)
    if not funcion:
        messagebox.showerror("ERROR", "Acción no válida.")
        return

    ctk.CTkLabel(ventana_seleccion, text="Seleccione el Tipo de Reserva",
                 text_color="white", width=100, height=20, font=("Lalezar", 15),
                 anchor="center", justify='center').pack(pady=20)

    for texto, tipo in [("Canchas", "Canchas"), ("Restaurante", "Restaurante")]:
        ctk.CTkButton(ventana_seleccion, text=texto, width=150, height=50,
                      command=lambda t=tipo: funcion(t),
                      fg_color="#2FB166", text_color="white").pack(pady=20)

# ---------- CANCELAR RESERVAS ----------
def _ventana_texto(placeholder, mostrar=""):
    """Ventana genérica de input. Retorna el texto ingresado."""
    resultado = {"valor": None}
    ventana = Toplevel(ventana_principal)
    ventana.geometry("400x150")
    ventana.title("Datos")
    ventana.resizable(False, False)
    ventana.configure(background="black")

    entrada = ctk.CTkEntry(ventana, width=300, show=mostrar, height=50,
                           font=("Lalezar", 20), placeholder_text=placeholder,
                           fg_color="white", corner_radius=10,
                           border_color="white", text_color="Black")
    entrada.place(x=50, y=25)

    def confirmar():
        resultado["valor"] = entrada.get()
        ventana.destroy()

    ctk.CTkButton(ventana, command=confirmar, text="Confirmar", width=100, height=25,
                  fg_color="#2FB166", font=("Lalezar", 15), corner_radius=10,
                  hover_color="#2FB166").place(x=150, y=100)
    ventana.wait_window()
    return resultado["valor"]

def cancelar_reserva(tipo_reserva_seleccionado):
    global nombre_archivo_reservas
    if not tipo_reserva_seleccionado:
        messagebox.showerror("ERROR", "Debe seleccionar un tipo de reserva.")
        return
    ventana_seleccion.destroy()
    nombre_archivo_reservas = ("src/JSON/Reservas.json" if tipo_reserva_seleccionado == "Canchas"
                               else "src/JSON/ReservasRestaurante.json")

    numero_ingresado = _ventana_texto("Número de Reserva")
    if not numero_ingresado:
        messagebox.showerror("ERROR", "No se ingresó número de reserva.")
        return

    # Verificar que la reserva pertenece al usuario logueado
    if not _verificar_mail_reserva(numero_ingresado):
        messagebox.showerror("ERROR", "La reserva no pertenece a tu cuenta.")
        return

    clave_ingresada = _ventana_texto("Contraseña", mostrar="*")
    if not _verificar_clave_usuario(clave_ingresada):
        messagebox.showerror("ERROR", "Contraseña incorrecta.")
        return

    restablecer_datos_reserva(numero_ingresado)
    messagebox.showinfo("Éxito", "Reserva cancelada exitosamente.")
    enviar_mail(mail_usuario,
                f"Se canceló tu reserva número {numero_ingresado}.",
                "Reserva Cancelada")

def _verificar_mail_reserva(numero_ingresado):
    try:
        with open(nombre_archivo_reservas, 'r') as f:
            reservas = json.load(f)
        for r in reservas:
            if r['Numero Reserva'] == str(numero_ingresado):
                return r['Mail'] == mail_usuario
    except Exception:
        pass
    return False

def _verificar_clave_usuario(clave_ingresada):
    try:
        with open("src/JSON/Usuarios.json", 'r') as f:
            usuarios = json.load(f)
        for u in usuarios:
            if u['Mail'] == mail_usuario:
                return verificar_contrasena(clave_ingresada, u['Clave'])
    except Exception:
        pass
    return False

def restablecer_datos_reserva(numero_ingresado):
    try:
        with open(nombre_archivo_reservas, 'r') as f:
            archivo_reservas = json.load(f)

        if nombre_archivo_reservas == "src/JSON/Reservas.json":
            for reserva in archivo_reservas:
                if reserva['Numero Reserva'] == str(numero_ingresado):
                    deporte = reserva['Deporte']
                    dia = reserva['Dia']
                    horario = reserva['Horario']
                    cancha = reserva['Cancha']
                    archivo_deporte = f"src/JSON/{deporte}.json"
                    with open(archivo_deporte, 'r') as f:
                        datos_deporte = json.load(f)
                    for item in datos_deporte:
                        for nombre_cancha, dias in item.items():
                            if nombre_cancha == cancha and dia in dias and horario in dias[dia]:
                                if dias[dia][horario] == "Reservada":
                                    dias[dia][horario] = "Disponible"
                    with open(archivo_deporte, 'w') as f:
                        json.dump(datos_deporte, f, indent=4)

        elif nombre_archivo_reservas == "src/JSON/ReservasRestaurante.json":
            for reserva in archivo_reservas:
                if reserva['Numero Reserva'] == str(numero_ingresado):
                    dia = reserva['Dia']
                    cantidad = reserva['Numero de comensales']
                    datos_rest = cargar_datos_restaurante()[0]
                    datos_rest[dia]["Lugares Disponibles"] += cantidad
                    datos_rest[dia]["Lugares Ocupados"] -= cantidad
                    guardar_datos_restaurante([datos_rest])

        archivo_reservas = [r for r in archivo_reservas if r['Numero Reserva'] != str(numero_ingresado)]
        with open(nombre_archivo_reservas, 'w') as f:
            json.dump(archivo_reservas, f, indent=4)

    except FileNotFoundError:
        messagebox.showerror("ERROR", "El archivo no se encontró.")
    except json.JSONDecodeError:
        messagebox.showerror("ERROR", "Error al leer el JSON.")
    except Exception as e:
        messagebox.showerror("ERROR", f"Error inesperado: {e}")

# ---------- MENÚ ----------
def cargar_menu():
    archivo = cargar_archivo("src/JSON/Menu.json")
    for menu in archivo:
        for hoja, productos in menu.items():
            destino = {"Entradas": entradas, "Principal": principales,
                       "Bebidas": bebidas, "Postres": postres}.get(hoja)
            if destino is not None:
                destino.update(productos)

def _mostrar_items_en_ventana(ventana, items, x_producto=75, x_precio=270, y_inicio=118):
    """Renderiza pares producto-precio en una ventana. Elimina código duplicado."""
    y = y_inicio
    for producto, precio in items.items():
        ctk.CTkLabel(ventana, text=str(producto), text_color="black",
                     fg_color="#2FB166", bg_color="#2FB166", corner_radius=0,
                     font=("Lalezar", 20), anchor=ctk.W).place(x=x_producto, y=y)
        ctk.CTkLabel(ventana, text=f"${precio}", text_color="black",
                     fg_color="#2FB166", bg_color="#2FB166", corner_radius=0,
                     font=("Lalezar", 20), anchor=ctk.W).place(x=x_precio, y=y)
        y += 50

def mostrar_menu():
    mapa = {
        "src/Imagenes/Fondos/Entradas.png": entradas,
        "src/Imagenes/Fondos/Principal.png": principales,
        "src/Imagenes/Fondos/Bebidas.png": bebidas,
        "src/Imagenes/Fondos/Postres.png": postres,
    }
    items = mapa.get(fondo_menu, {})
    _mostrar_items_en_ventana(ventana_menu, items)

def menu():
    global i_menu, ventana_menu, fondo_menu
    cargar_menu()
    ventana_menu = Toplevel(ventana_principal)
    ventana_menu.geometry("400x600")
    ventana_menu.title("MENU")
    ventana_menu.resizable(False, False)
    ventana_menu.transient(ventana_principal)
    ventana_menu.lift()
    ventana_menu.focus_set()
    ventana_menu.grab_set()

    i_menu = 0
    fondo_menu = "src/Imagenes/Fondos/" + hojas_menu[i_menu] + ".png"
    poner_fondo(fondo_menu, ventana_menu)
    botones_menu("HojasMenu")
    mostrar_menu()

def botones_menu(tipo_hoja):
    if tipo_hoja == "HojasMenu":
        i, ventana, lista = i_menu, ventana_menu, hojas_menu
    else:
        i, ventana, lista = i_precios, ventana_precios, hojas_precios

    img_atras = ctk.CTkImage(Image.open("src/Imagenes/Botones/Atras.png"), size=(40, 20))
    btn_atras = ctk.CTkButton(ventana, text="", image=img_atras,
                               command=lambda: atras(tipo_hoja),
                               width=40, height=20, fg_color="black",
                               border_width=0, bg_color="black",
                               corner_radius=0, hover_color="black")
    if i == 0:
        btn_atras.place_forget()
    else:
        btn_atras.place(x=40, y=565)

    img_siguiente = ctk.CTkImage(Image.open("src/Imagenes/Botones/Siguiente.png"), size=(40, 20))
    btn_siguiente = ctk.CTkButton(ventana, text="", image=img_siguiente,
                                   command=lambda: siguiente(tipo_hoja),
                                   width=40, height=20, fg_color="black",
                                   border_width=0, bg_color="black",
                                   corner_radius=0, hover_color="black")
    if i == len(lista) - 1:
        btn_siguiente.place_forget()
    else:
        btn_siguiente.place(x=320, y=565)

def restaurant():
    poner_fondo("src/Imagenes/Fondos/Restaurante.png", ventana_principal)
    botones_sidebar()

    img_reserva = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonReserva.png"), size=(250, 250))
    ctk.CTkButton(ventana_principal, text="", image=img_reserva,
                  command=lambda: pantalla_reserva_restaurante() if sesion_activa() else None,
                  width=50, height=50, fg_color="#2FB166", border_width=0,
                  bg_color="black", corner_radius=0, hover_color="#2FB166").place(x=235, y=300)

    img_menu = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonMenu.png"), size=(250, 250))
    ctk.CTkButton(ventana_principal, text="", image=img_menu, command=menu,
                  width=50, height=50, fg_color="#2FB166", border_width=0,
                  corner_radius=0, hover_color="#2FB166").place(x=920, y=300)

# ---------- RESTAURANTE ----------
ARCHIVO_RESTAURANTE = 'src/JSON/Restaurante.json'

def cargar_datos_restaurante():
    try:
        with open(ARCHIVO_RESTAURANTE, 'r') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return [{"Lunes": {"Lugares Disponibles": 50, "Lugares Ocupados": 0},
                 "Martes": {"Lugares Disponibles": 50, "Lugares Ocupados": 0},
                 "Miércoles": {"Lugares Disponibles": 50, "Lugares Ocupados": 0},
                 "Jueves": {"Lugares Disponibles": 50, "Lugares Ocupados": 0},
                 "Viernes": {"Lugares Disponibles": 50, "Lugares Ocupados": 0},
                 "Sábado": {"Lugares Disponibles": 50, "Lugares Ocupados": 0},
                 "Domingo": {"Lugares Disponibles": 50, "Lugares Ocupados": 0}}]

def guardar_datos_restaurante(datos):
    with open(ARCHIVO_RESTAURANTE, 'w') as archivo:
        json.dump(datos, archivo, indent=4)

def pantalla_reserva_restaurante():
    ventana_res = Toplevel(ventana_principal)
    ventana_res.geometry("400x600")
    ventana_res.title("Reservas")
    ventana_res.resizable(False, False)
    ventana_res.transient(ventana_principal)
    ventana_res.lift()
    ventana_res.focus_set()
    ventana_res.grab_set()
    poner_fondo("src/Imagenes/Fondos/Reservas 1.png", ventana_res)

    entry_nombre = ctk.CTkEntry(ventana_res, width=200, height=40, font=("Lalezar", 20),
                                placeholder_text="Ingrese Nombre", fg_color="white",
                                corner_radius=0, border_color="white", text_color="Black")
    entry_nombre.place(x=113, y=267)

    entry_telefono = ctk.CTkEntry(ventana_res, width=200, height=40, font=("Lalezar", 20),
                                  placeholder_text="Ingrese su Telefono", fg_color="white",
                                  corner_radius=0, border_color="white", text_color="Black")
    entry_telefono.place(x=113, y=345)

    dias_data = cargar_datos_restaurante()[0]
    dias_semana = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

    slider_dias = ctk.CTkSlider(ventana_res, from_=0, to=6, number_of_steps=6,
                                bg_color="#2FB166", button_color="blue")
    slider_dias.place(x=105, y=450)

    label_dia = ctk.CTkLabel(ventana_res, text="Día: Lunes", fg_color="#2FB166",
                             bg_color="#2FB166", text_color="white")
    label_dia.place(x=160, y=470)

    slider_cantidad = ctk.CTkSlider(ventana_res, from_=1, to=20, number_of_steps=20,
                                    bg_color="#2FB166", button_color="green")
    slider_cantidad.place(x=105, y=400)

    label_cantidad = ctk.CTkLabel(ventana_res, text="Cantidad de comensales: 1",
                                  fg_color="#2FB166", bg_color="#2FB166", text_color="white")
    label_cantidad.place(x=115, y=415)

    def actualizar_labels(*_):
        label_dia.configure(text=f"Día: {dias_semana[int(slider_dias.get())]}")
        label_cantidad.configure(text=f"Cantidad de comensales: {int(slider_cantidad.get())}")

    slider_dias.configure(command=actualizar_labels)
    slider_cantidad.configure(command=actualizar_labels)

    def reservar():
        nombre = entry_nombre.get()
        telefono = entry_telefono.get()
        dia = dias_semana[int(slider_dias.get())]
        cantidad = int(slider_cantidad.get())

        if not nombre or not telefono:
            messagebox.showerror("Error", "Nombre y teléfono son obligatorios.")
            return
        if dias_data[dia]["Lugares Disponibles"] < cantidad:
            messagebox.showerror("Error", "No hay suficientes lugares disponibles.")
            return

        dias_data[dia]["Lugares Disponibles"] -= cantidad
        dias_data[dia]["Lugares Ocupados"] += cantidad
        guardar_datos_restaurante([dias_data])

        numero = generar_numero_reserva()
        datos_reserva = {"Numero Reserva": numero, "Nombre": nombre, "Telefono": telefono,
                         "Mail": mail_usuario, "Dia": dia, "Numero de comensales": cantidad}

        try:
            with open("src/JSON/ReservasRestaurante.json", "r") as f:
                reservas = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            reservas = []

        reservas.append(datos_reserva)
        with open("src/JSON/ReservasRestaurante.json", "w") as f:
            json.dump(reservas, f, indent=4)

        messagebox.showinfo("Éxito", "Reserva confirmada.")
        cuerpo = "\n".join(f"{k}: {v}" for k, v in datos_reserva.items())
        enviar_mail(mail_usuario, cuerpo, "Reserva Confirmada")
        ventana_res.destroy()

    ctk.CTkButton(ventana_res, text="Reservar", command=reservar, width=100, height=50,
                  fg_color="#2FB166", border_width=0, corner_radius=0,
                  hover_color="#2FB166", font=("Lalezar", 25)).place(x=145, y=530)

# ---------- PRECIOS ----------
def pantalla_precios():
    global ventana_precios
    ventana_precios = Toplevel(ventana_principal)
    ventana_precios.geometry("400x600")
    ventana_precios.title("Precios")
    ventana_precios.resizable(False, False)
    ventana_precios.transient(ventana_principal)
    ventana_precios.lift()
    ventana_precios.focus_set()
    ventana_precios.grab_set()

def precios():
    global i_precios, fondo_precios
    cargar_precios()
    pantalla_precios()
    i_precios = 0
    fondo_precios = "src/Imagenes/Fondos/" + hojas_precios[i_precios] + ".png"
    poner_fondo(fondo_precios, ventana_precios)
    botones_menu("HojasPrecios")

def cargar_precios():
    archivo = cargar_archivo("src/JSON/Precios.json")
    mapa = {"Futbol 5": futbol5, "Futbol 8": futbol8, "Tenis": tenis, "Padel": padel}
    for item in archivo:
        for hoja, info in item.items():
            if hoja in mapa:
                mapa[hoja].update(info)

def mostrar_precios():
    mapa = {
        "src/Imagenes/Fondos/HojaFutbol5.png": futbol5,
        "src/Imagenes/Fondos/HojaFutbol8.png": futbol8,
        "src/Imagenes/Fondos/HojaTenis.png": tenis,
        "src/Imagenes/Fondos/HojaPadel.png": padel,
    }
    items = mapa.get(fondo_precios, {})
    _mostrar_items_en_ventana(ventana_precios, items)

# ---------- BENEFICIOS ----------
def mostrar_botones_beneficios():
    beneficios_config = [
        (240, 665, 125, "Hamburguesa"),
        (550, 665, 150, "Padel 1 hora"),
        (860, 665, 150, "Tenis 1 hora"),
        (1170, 665, 150, "Futbol 1 hora"),
        (240, 357, 30, "Papas"),
        (550, 357, 75, "Gorra Personalizada"),
        (860, 357, 100, "Short Personalizado"),
        (1170, 357, 125, "Camiseta Personalizada"),
    ]
    for x, y, precio, nombre in beneficios_config:
        ctk.CTkButton(ventana_principal, text=str(precio), width=25, height=25,
                      fg_color="#2FB166", bg_color="#2FB166", hover_color="#2FB163",
                      text_color="Black", command=lambda p=precio, n=nombre: agregar_al_carrito(p, n),
                      font=("Lalezar", 20), corner_radius=0).place(x=x, y=y)

    ctk.CTkLabel(ventana_principal, text=str(puntos_club), text_color="BLACK",
                 width=20, height=20, fg_color="#2FB166",
                 font=("Lalezar", 20), anchor=ctk.W).place(x=1200, y=37)

    ctk.CTkButton(ventana_principal, text="Carrito🛒", command=mostrar_recibo,
                  font=("Lalezar", 20), width=20, height=20, fg_color="#2FB166",
                  text_color="black", corner_radius=0, hover_color="#2FB166",
                  bg_color="#2FB166").place(x=1175, y=95)

def agregar_al_carrito(precio, nombre):
    compras.append((nombre, precio))
    messagebox.showinfo("Carrito", f"Agregaste {nombre} al carrito.")

def beneficios():
    poner_fondo("src/Imagenes/Fondos/Beneficios.png", ventana_principal)
    botones_sidebar()
    mostrar_botones_beneficios()

def pagar():
    global puntos_club
    total = sum(precio for _, precio in compras)
    if puntos_club < total:
        messagebox.showerror("Error", "Fondos insuficientes.")
        compras.clear()
    else:
        puntos_club -= total
        _actualizar_campo_usuario("Puntos", puntos_club)
        compras.clear()
        messagebox.showinfo("Éxito", "Pago realizado con éxito.")

def mostrar_recibo():
    ventana_recibo = Toplevel(ventana_principal)
    ventana_recibo.title("Recibo de Compras")
    ventana_recibo.geometry("220x300")
    ventana_recibo.resizable(False, False)

    texto = "\n".join(f"{n}: ${p}" for n, p in compras) or "El carrito está vacío."
    tk.Label(ventana_recibo, text=texto, width=40, justify="left",
             font=("Lalezar", 12)).pack(pady=10)

    ctk.CTkButton(ventana_recibo, text="Seguir Comprando",
                  command=ventana_recibo.destroy).pack(pady=5)
    ctk.CTkButton(ventana_recibo, text="Pagar",
                  command=lambda: [pagar(), ventana_recibo.destroy()]).pack(pady=5)

# ---------- RESERVA DE CANCHAS ----------
def generar_numero_reserva():
    """Genera un ID único de reserva usando UUID."""
    return str(uuid.uuid4())[:8].upper()

def cargar_canchas(deporte_elegido):
    global nombre_archivo, lista_canchas
    poner_fondo(f"src/Imagenes/Fondos/{deporte_elegido}.png", ventana_principal)
    botones_sidebar()
    mostrar_boton_reservas(deporte_elegido)
    dia_elegido = dia.get()
    horario_elegido = horario.get()
    if dia_elegido != "Seleccione un Dia" and horario_elegido != "Seleccione un Horario":
        nombre_archivo = f"src/JSON/{deporte_elegido}.json"
        lista_canchas = cargar_archivo(nombre_archivo)
        if lista_canchas:
            disponibles = mostrar_canchas_disponibles(lista_canchas, dia_elegido, horario_elegido)
            cancha.configure(values=disponibles)

def pantalla_futbol():
    global deporte_elegido
    deporte_elegido = "Futbol"
    cargar_canchas(deporte_elegido)

def pantalla_tenis():
    global deporte_elegido
    deporte_elegido = "Tenis"
    cargar_canchas(deporte_elegido)

def pantalla_padel():
    global deporte_elegido
    deporte_elegido = "Padel"
    cargar_canchas(deporte_elegido)

def mostrar_boton_reservas(deporte_elegido):
    global dia, horario, cancha

    opciones_dia = ["Seleccione un Dia", "Lunes", "Martes", "Miercoles",
                    "Jueves", "Viernes", "Sabado", "Domingo"]
    opciones_horario = ["Seleccione un Horario", "08:00", "09:00", "10:00", "11:00",
                        "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
                        "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]

    estilo_menu = dict(fg_color="#2FB166", text_color="white", height=45, width=230,
                       bg_color="#2FB166", button_color="#2FB166", font=("Lalezar", 15),
                       corner_radius=0, button_hover_color="#2FB166", dropdown_hover_color="#2FB166")

    dia = ctk.CTkOptionMenu(ventana_principal, values=opciones_dia,
                            command=lambda *_: actualizar_canchas(deporte_elegido), **estilo_menu)
    dia.place(x=170, y=365)

    horario = ctk.CTkOptionMenu(ventana_principal, values=opciones_horario,
                                command=lambda *_: actualizar_canchas(deporte_elegido), **estilo_menu)
    horario.place(x=570, y=365)

    cancha = ctk.CTkOptionMenu(ventana_principal, values=["Seleccione una Cancha"], **estilo_menu)
    cancha.place(x=1045, y=365)

    ctk.CTkButton(ventana_principal, text="SIGUIENTE", text_color="white", width=220, height=60,
                  fg_color="#2FB166", corner_radius=0, hover_color="#065F2B",
                  command=reserva, font=("Lalezar", 20)).place(x=580, y=660)

def actualizar_canchas(deporte_elegido):
    global lista_canchas, nombre_archivo, cancha_elegida, dia_elegido, horario_elegido
    dia_elegido = dia.get()
    horario_elegido = horario.get()
    if dia_elegido != "Seleccione un Dia" and horario_elegido != "Seleccione un Horario":
        nombre_archivo = f"src/JSON/{deporte_elegido}.json"
        lista_canchas = cargar_archivo(nombre_archivo)
        if lista_canchas:
            disponibles = mostrar_canchas_disponibles(lista_canchas, dia_elegido, horario_elegido)
            cancha.configure(values=disponibles)
    cancha_elegida = cancha.get()

def mostrar_canchas_disponibles(lista, dia_el, horario_el):
    disponibles = []
    for item in lista:
        for nombre_cancha, datos in item.items():
            try:
                if datos[dia_el][horario_el] == "Disponible":
                    disponibles.append(nombre_cancha)
            except KeyError:
                pass
    if not disponibles:
        messagebox.showerror("Ocupado", f"No hay canchas disponibles el {dia_el} a las {horario_el}.")
    return disponibles

def cargar_datos_reserva():
    try:
        with open("src/JSON/Reservas.json", "r") as f:
            datos = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        datos = []
    datos.append({
        "Numero Reserva": numero,
        "Deporte": deporte_elegido,
        "Cancha": cancha_elegida,
        "Nombre": nombre_usuario,
        "Mail": mail_usuario,
        "Dia": dia_elegido,
        "Horario": horario_elegido,
        "Precio": precio,
        "Estado": "Pendiente"
    })
    with open("src/JSON/Reservas.json", "w") as f:
        json.dump(datos, f, indent=4)

def establecer_precio():
    global precio
    archivo = cargar_archivo("src/JSON/Precios.json")
    precios_dict = {}
    for item in archivo:
        precios_dict.update(item)

    canchas_f5 = ("Cancha 1 (F5)", "Cancha 2 (F5)", "Cancha 3 (F5)", "Cancha 4 (F5)")
    canchas_f8 = ("Cancha 5 (F8)", "Cancha 6 (F8)")
    horarios_dia = ("08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00")

    turno = "Dia" if horario_elegido in horarios_dia else "Noche"

    if deporte_elegido == "Futbol":
        tipo = "Futbol 5" if cancha_elegida in canchas_f5 else "Futbol 8"
    elif deporte_elegido == "Padel":
        tipo = "Padel"
    else:
        tipo = "Tenis"

    precio = precios_dict.get(tipo, {}).get(turno, 0)
    return precio

def ventana_pago(precio_total):
    global pago_realizado, precio_restante, estado_reserva
    precio_restante = precio_total
    cargar_datos_reserva()

    def actualizar_estado_reserva(estado, num_reserva):
        try:
            with open("src/JSON/Reservas.json", "r") as f:
                reservas = json.load(f)
            for r in reservas:
                if str(r["Numero Reserva"]) == str(num_reserva):
                    r["Estado"] = estado
                    break
            with open("src/JSON/Reservas.json", "w") as f:
                json.dump(reservas, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar estado: {e}")

    def procesar_sena():
        global pago_realizado, estado_reserva, precio_restante
        estado_reserva = "Señada"
        precio_restante = precio_total - round(precio_total / 3)
        pago_realizado = True
        actualizar_estado_reserva(estado_reserva, numero)
        mostrar_qr()
        v_pago.destroy()

    def procesar_pago_total():
        global pago_realizado, estado_reserva
        estado_reserva = "Pagada"
        pago_realizado = True
        actualizar_estado_reserva(estado_reserva, numero)
        mostrar_qr()
        v_pago.destroy()

    v_pago = ctk.CTkToplevel(ventana_principal)
    v_pago.title("Confirmar Pago")
    v_pago.geometry("400x300")
    v_pago.resizable(False, False)
    v_pago.transient(ventana_principal)
    v_pago.lift()
    v_pago.focus_set()
    v_pago.grab_set()

    ctk.CTkLabel(v_pago, text=f"Total a pagar: ${precio_total}",
                 font=("Lalezar", 20)).pack(pady=20)
    ctk.CTkButton(v_pago, text="Señar", command=procesar_sena,
                  width=220, height=60, fg_color="#2FB166",
                  font=("Lalezar", 20), corner_radius=0).pack(pady=10)
    ctk.CTkButton(v_pago, text="Pagar Total", command=procesar_pago_total,
                  width=220, height=60, fg_color="#2FB166",
                  font=("Lalezar", 20), corner_radius=0).pack(pady=10)
    v_pago.mainloop()

def mostrar_qr():
    global ventana_qr
    ventana_qr = Toplevel(ventana_principal)
    ventana_qr.title("QR")
    ventana_qr.geometry("400x400")
    ventana_qr.resizable(False, False)
    ventana_qr.transient(ventana_principal)
    ventana_qr.configure(background="black")
    ventana_qr.lift()
    ventana_qr.focus_set()
    ventana_qr.grab_set()

    monto = precio_restante if estado_reserva == "Señada" else precio
    data_qr = f"Transferir ${monto} a la cuenta: 123-456-789"
    qr = qrcode.make(data_qr)
    qr.save("qr_pago.png")

    imagen_pil = Image.open("qr_pago.png")
    imagen_qr = ctk.CTkImage(light_image=imagen_pil, dark_image=imagen_pil, size=(200, 200))
    ctk.CTkLabel(ventana_qr, image=imagen_qr).place(x=100, y=50)

    ctk.CTkButton(ventana_qr, text="Confirmar Pago", command=confirmar_pago,
                  width=100, height=60, fg_color="#2FB166",
                  font=("Lalezar", 20), corner_radius=20).place(x=150, y=300)

def confirmar_pago():
    global pago_realizado, estado_reserva, numero
    ventana_qr.destroy()
    if not pago_realizado:
        messagebox.showerror("Error", "Debe realizar el pago antes de confirmar.")
        return
    msg = ("Reserva señada. El resto del pago se abona al llegar."
           if estado_reserva == "Señada" else "Reserva pagada y confirmada.")
    messagebox.showinfo("Reserva", msg)
    ctk.CTkButton(ventana_principal, text="Confirmar Reserva", command=confirmar_reserva,
                  width=220, height=60, fg_color="#2FB166",
                  font=("Lalezar", 20), corner_radius=0).place(x=570, y=660)

def confirmar_reserva():
    global puntos_club
    puntos_club += 10
    _actualizar_campo_usuario("Puntos", puntos_club)

    for item in lista_canchas:
        if cancha_elegida in item:
            item[cancha_elegida][dia_elegido][horario_elegido] = "Reservada"
            break
    with open(nombre_archivo, "w") as f:
        json.dump(lista_canchas, f, indent=4)

    messagebox.showinfo("Reserva Confirmada", "Te enviaremos un mail con los datos.")
    enviar_mail(mail_usuario, datos_reserva_texto, "Reserva Confirmada")
    poner_fondo("src/Imagenes/Fondos/PantallaPrincipal.png", ventana_principal)
    botones_sidebar()

def reserva():
    global cancha_elegida, dia_elegido, horario_elegido, lista_canchas
    global nombre_archivo, datos_reserva_texto, numero, estado_reserva, precio, pago_realizado

    cancha_elegida = cancha.get()
    dia_elegido = dia.get()
    horario_elegido = horario.get()
    estado_reserva = "Pendiente"
    pago_realizado = False

    if (cancha_elegida == "Seleccione una Cancha" or
            dia_elegido == "Seleccione un Dia" or
            horario_elegido == "Seleccione un Horario"):
        messagebox.showerror("Error", "Seleccione todos los datos.")
        return

    try:
        poner_fondo("src/Imagenes/Fondos/Reserva.png", ventana_principal)
        botones_sidebar()
        numero = generar_numero_reserva()
        precio = establecer_precio()
        datos_reserva_texto = (
            f"Numero Reserva: {numero}\n"
            f"Nombre: {nombre_usuario}\n"
            f"Mail: {mail_usuario}\n"
            f"Deporte: {deporte_elegido}\n"
            f"Día: {dia_elegido}\n"
            f"Horario: {horario_elegido}\n"
            f"Cancha: {cancha_elegida}\n"
            f"Precio: ${precio}\n"
            f"Estado: Pendiente\n"
        )
        ctk.CTkLabel(ventana_principal, text=datos_reserva_texto, text_color="white",
                     width=350, height=350, fg_color="#2FB166",
                     font=("Lalezar", 20), anchor=ctk.W, justify='left').place(x=510, y=225)

        ctk.CTkButton(ventana_principal, text="Realizar Pago",
                      command=lambda: ventana_pago(precio),
                      width=220, height=60, fg_color="#2FB166",
                      font=("Lalezar", 20), corner_radius=0,
                      hover_color="#2FB166").place(x=570, y=660)
    except Exception as e:
        messagebox.showerror("ERROR", f"Error en la reserva: {e}")

# ---------- MAIL ----------
def enviar_mail(destinatario, cuerpo_mensaje, asunto):
    if not destinatario:
        messagebox.showerror("ERROR", "No hay mail registrado.")
        return
    if not EMAIL_REMITENTE or not EMAIL_CONTRASENA:
        messagebox.showwarning("Mail", "Credenciales de correo no configuradas.")
        return
    try:
        mensaje = MIMEMultipart()
        mensaje["From"] = EMAIL_REMITENTE
        mensaje["To"] = destinatario
        mensaje["Subject"] = asunto
        mensaje.attach(MIMEText(cuerpo_mensaje, "plain"))

        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL_REMITENTE, EMAIL_CONTRASENA)
        servidor.sendmail(EMAIL_REMITENTE, destinatario, mensaje.as_string())
        servidor.quit()
        messagebox.showinfo("Éxito", "Correo enviado con éxito.")
    except Exception as e:
        messagebox.showerror("ERROR", f"Error al enviar el correo: {e}")

# ---------- INICIO ----------
def inicio():
    global nombre_usuario, mail_usuario, puntos_club, imagen_perfil
    nombre_usuario = ""
    mail_usuario = ""
    puntos_club = 0
    imagen_perfil = ""

    poner_fondo("src/Imagenes/Fondos/Inicio.png", ventana_principal)

    for texto, comando, x in [
        ("Iniciar Sesion", fondo_iniciar_sesion, 215),
        ("Crear Cuenta", mostrar_formulario_crear_cuenta, 933),
    ]:
        ctk.CTkButton(ventana_principal, text=texto, text_color="white", width=220, height=60,
                      fg_color="#2FB166", corner_radius=0, hover_color="#2FB166",
                      command=comando, font=("Lalezar", 20)).place(x=x, y=355)

    img_cerrar = ctk.CTkImage(Image.open("src/Imagenes/Botones/BotonCerrar.png"), size=(40, 50))
    ctk.CTkButton(ventana_principal, text="", image=img_cerrar, command=cerrar,
                  width=50, height=20, fg_color="#2FB166", bg_color="black",
                  border_width=0, corner_radius=90, hover_color="#2FB166").place(x=10, y=10)

# ---------- MAIN ----------
inicio()
ventana_principal.mainloop()