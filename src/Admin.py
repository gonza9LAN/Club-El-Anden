import json
import os
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, simpledialog
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()
EMAIL_REMITENTE = os.getenv("EMAIL_REMITENTE")
EMAIL_CONTRASENA = os.getenv("EMAIL_CONTRASENA")


# ---------- UTILIDADES ----------
def cargar_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, "r") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        messagebox.showerror("Error", f"Error al leer el archivo: {e}")
        return []

def enviar_mail(destinatario, cuerpo_mensaje, asunto):
    if not destinatario:
        messagebox.showerror("ERROR", "No hay mail registrado.")
        return
    if not EMAIL_REMITENTE or not EMAIL_CONTRASENA:
        messagebox.showwarning("Mail", "Credenciales de correo no configuradas (.env).")
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

def _estilo_tabla():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview.Heading", background="#2FB166", foreground="black")
    style.configure("Custom.Treeview", background="black", foreground="white",
                    fieldbackground="black", highlightthickness=0, bd=1, relief="solid")
    style.map("Custom.Treeview", background=[("selected", "#2FB166")])

def _crear_treeview(frame, columnas, anchos):
    """Crea un Treeview con scrollbar dentro del frame dado."""
    _estilo_tabla()
    tree = ttk.Treeview(frame, style="Custom.Treeview")
    tree.pack(fill="both", expand=True, side="left")
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)
    tree["columns"] = columnas
    tree["show"] = "headings"
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=anchos.get(col, 100), anchor="center")
    tree.tag_configure("data_row", background="black", foreground="white")
    return tree

# ---------- PANTALLA PRINCIPAL ----------
def pantalla_administrador():
    global ventana_administrador
    ventana_administrador = ctk.CTk()
    ventana_administrador.geometry("500x600")
    ventana_administrador.title("El ANDEN - Administracion")
    ventana_administrador.resizable(False, False)
    ventana_administrador.configure(fg_color="black")

def botones_administrador():
    ctk.CTkLabel(ventana_administrador, text="Administrador", text_color="white",
                 width=150, height=100, font=("Lalezar", 50),
                 anchor=ctk.W, justify='left').place(x=100, y=5)

    botones = [
        ("Lugares Restaurante", ver_disponibilidad, 100),
        ("Ver Canchas", seleccion_deporte, 150),
        ("Precios Canchas", gestionar_precios_canchas, 200),
        ("Ver Reservas", lambda: seleccion_tipo_reserva("Ver"), 250),
        ("Eliminar Reserva", lambda: seleccion_tipo_reserva("Cancelar"), 300),
        ("Gestionar Menu", gestionar_menu, 350),
    ]
    for texto, comando, y in botones:
        ctk.CTkButton(ventana_administrador, text=texto, command=comando,
                      border_width=2, border_color="#2FB166", font=("Lalezar", 20),
                      width=200, height=20, fg_color="black",
                      corner_radius=50, hover_color="black").place(x=150, y=y)

def administrador():
    pantalla_administrador()
    botones_administrador()

# ---------- RESERVAS ----------
def seleccion_tipo_reserva(destino_reserva):
    global ventana_seleccion
    ventana_seleccion = Toplevel(ventana_administrador)
    ventana_seleccion.title("Tipo de Reserva")
    ventana_seleccion.geometry("200x300")
    ventana_seleccion.resizable(False, False)
    ventana_seleccion.configure(background="black")

    funcion = {"Cancelar": eliminar_reserva, "Ver": ver_reservas}.get(destino_reserva)
    if not funcion:
        messagebox.showerror("ERROR", "Acción no válida.")
        return

    ctk.CTkLabel(ventana_seleccion, text="Tipo de Reserva", text_color="white",
                 font=("Lalezar", 15)).pack(pady=20)

    for texto in ["Canchas", "Restaurante"]:
        ctk.CTkButton(ventana_seleccion, text=texto, width=150, height=50,
                      command=lambda t=texto: funcion(t),
                      fg_color="#2FB166", text_color="white").pack(pady=20)

def pantalla_reservas():
    global ventana_reservas
    ventana_reservas = Toplevel(ventana_administrador)
    ventana_reservas.title("Reservas")
    ventana_reservas.geometry("950x650")
    ventana_reservas.resizable(False, False)
    ventana_reservas.configure(background="black")

def leer_reservas_json(archivo_json):
    try:
        with open(archivo_json, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)
        return pd.DataFrame(data)
    except FileNotFoundError:
        messagebox.showerror("ERROR", f"Archivo {archivo_json} no encontrado.")
        return pd.DataFrame()
    except json.JSONDecodeError:
        messagebox.showerror("ERROR", "El archivo no es un JSON válido.")
        return pd.DataFrame()

def mostrar_datos_reservas(df):
    for widget in frame_tabla_reservas.winfo_children():
        widget.destroy()
    anchos = {"Numero Reserva": 30, "Deporte": 20, "Cancha": 50, "Nombre": 20,
              "Gmail": 600, "Dia": 20, "Horario": 20, "Precio": 20, "Estado": 30}
    tree = _crear_treeview(frame_tabla_reservas, list(df.columns), anchos)
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row), tags=("data_row",))

def buscar_reserva():
    resultado = hojas_reservas.copy()
    filtros = [
        (buscar_numero.get(), 'Numero Reserva', True),
        (buscar_cancha.get(), 'Cancha', False),
        (buscar_dia.get(), 'Dia', False),
        (buscar_deporte.get(), 'Deporte', False),
        (buscar_mail.get(), 'Mail', False),
        (buscar_estado.get(), 'Estado', False),
    ]
    for valor, col, exacto in filtros:
        if valor and col in resultado.columns:
            resultado = (resultado[resultado[col].astype(str) == valor] if exacto
                         else resultado[resultado[col].str.contains(valor, case=False)])
    mostrar_datos_reservas(resultado)

def ver_reservas(tipo_reserva_seleccionado):
    global hojas_reservas, frame_busqueda_reservas, frame_tabla_reservas
    global buscar_numero, buscar_deporte, buscar_dia, buscar_cancha, buscar_mail, buscar_estado

    ventana_seleccion.destroy()
    archivo = ("src/JSON/Reservas.json" if tipo_reserva_seleccionado == "Canchas"
               else "src/JSON/ReservasRestaurante.json")

    pantalla_reservas()

    frame_tabla_reservas = ctk.CTkFrame(ventana_reservas, fg_color="black")
    frame_tabla_reservas.pack(fill="both", expand=True)
    frame_busqueda_reservas = ctk.CTkFrame(ventana_reservas, fg_color="black", bg_color="black")
    frame_busqueda_reservas.pack(pady=10, fill="x", side="bottom")

    hojas_reservas = leer_reservas_json(archivo)
    if not hojas_reservas.empty:
        mostrar_datos_reservas(hojas_reservas)
    else:
        messagebox.showerror("ERROR", "No hay datos disponibles.")

    campos = [("Número de Reserva", "buscar_numero"), ("Deporte", "buscar_deporte"),
              ("Dia", "buscar_dia"), ("Cancha", "buscar_cancha"),
              ("Mail", "buscar_mail"), ("Estado", "buscar_estado")]

    entries = {}
    for placeholder, key in campos:
        e = ctk.CTkEntry(frame_busqueda_reservas, width=125, height=30,
                         placeholder_text=placeholder, placeholder_text_color="white",
                         text_color="white", border_width=2,
                         border_color="#2FB166", fg_color="#2FB166")
        e.pack(side="left", padx=10)
        entries[key] = e

    buscar_numero = entries["buscar_numero"]
    buscar_deporte = entries["buscar_deporte"]
    buscar_dia = entries["buscar_dia"]
    buscar_cancha = entries["buscar_cancha"]
    buscar_mail = entries["buscar_mail"]
    buscar_estado = entries["buscar_estado"]

    if archivo == "src/JSON/ReservasRestaurante.json":
        entries["buscar_cancha"].pack_forget()
        entries["buscar_deporte"].pack_forget()
        entries["buscar_estado"].pack_forget()

    ctk.CTkButton(frame_busqueda_reservas, text="Buscar", width=175, height=30,
                  command=buscar_reserva, fg_color="#2FB166",
                  text_color="white").pack(side="left", padx=10)
    ventana_reservas.mainloop()

def _ventana_texto_input(placeholder):
    resultado = {"valor": None}
    ventana = Toplevel(ventana_administrador)
    ventana.geometry("400x150")
    ventana.title("Texto")
    ventana.resizable(False, False)
    ventana.configure(background="black")

    entrada = ctk.CTkEntry(ventana, width=300, height=50, font=("Lalezar", 20),
                           placeholder_text=placeholder, fg_color="white",
                           corner_radius=10, border_color="white", text_color="Black")
    entrada.place(x=50, y=25)

    def confirmar():
        resultado["valor"] = entrada.get()
        ventana.destroy()

    ctk.CTkButton(ventana, command=confirmar, text="Confirmar", width=100, height=25,
                  fg_color="#2FB166", font=("Lalezar", 15), corner_radius=10,
                  hover_color="#2FB166").place(x=150, y=100)
    ventana.wait_window()
    return resultado["valor"]

def obtener_mail_usuario(numero_ingresado, archivo):
    try:
        with open(archivo, 'r') as f:
            reservas = json.load(f)
        for r in reservas:
            if r.get("Numero Reserva") == numero_ingresado:
                return r.get("Mail", "")
    except Exception:
        pass
    return ""

def eliminar_reserva(tipo_reserva_seleccionado):
    global nombre_archivo_reservas
    ventana_seleccion.destroy()
    nombre_archivo_reservas = ("src/JSON/Reservas.json" if tipo_reserva_seleccionado == "Canchas"
                               else "src/JSON/ReservasRestaurante.json")

    numero_ingresado = _ventana_texto_input("Ingrese el Numero de Reserva")
    if not numero_ingresado:
        messagebox.showerror("ERROR", "No se ingresó número de reserva.")
        return

    mail_usuario = obtener_mail_usuario(numero_ingresado, nombre_archivo_reservas)
    restablecer_datos_reserva(numero_ingresado)
    enviar_mail(mail_usuario,
                f"Tu reserva número {numero_ingresado} fue eliminada por el administrador.",
                "Reserva Eliminada")
    messagebox.showinfo("Éxito", "Reserva eliminada exitosamente.")

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
                        datos = json.load(f)
                    for item in datos:
                        for nombre_cancha, dias in item.items():
                            if nombre_cancha == cancha and dia in dias and horario in dias[dia]:
                                if dias[dia][horario] == "Reservada":
                                    dias[dia][horario] = "Disponible"
                    with open(archivo_deporte, 'w') as f:
                        json.dump(datos, f, indent=4)

        elif nombre_archivo_reservas == "src/JSON/ReservasRestaurante.json":
            for reserva in archivo_reservas:
                if reserva['Numero Reserva'] == str(numero_ingresado):
                    dia = reserva['Dia']
                    cantidad = reserva['Numero de comensales']
                    datos_rest = cargar_datos_restaurante()[0]
                    datos_rest[dia]["Lugares Disponibles"] += cantidad
                    datos_rest[dia]["Lugares Ocupados"] -= cantidad
                    guardar_datos_restaurante([datos_rest])

        archivo_reservas = [r for r in archivo_reservas
                            if r['Numero Reserva'] != str(numero_ingresado)]
        with open(nombre_archivo_reservas, 'w') as f:
            json.dump(archivo_reservas, f, indent=4)

    except FileNotFoundError:
        messagebox.showerror("ERROR", "Archivo no encontrado.")
    except json.JSONDecodeError:
        messagebox.showerror("ERROR", "Error al leer el JSON.")
    except Exception as e:
        messagebox.showerror("ERROR", f"Error inesperado: {e}")

# ---------- CANCHAS ----------
def seleccion_deporte():
    global ventana_seleccion
    ventana_seleccion = Toplevel(ventana_administrador)
    ventana_seleccion.title("Seleccionar Deporte")
    ventana_seleccion.geometry("400x300")
    ventana_seleccion.resizable(False, False)
    ventana_seleccion.configure(background="black")

    for deporte in ["Futbol", "Tenis", "Padel"]:
        ctk.CTkButton(ventana_seleccion, text=deporte, width=150, height=50,
                      command=lambda d=deporte: ver_canchas(d),
                      fg_color="#2FB166", text_color="white").pack(pady=20)
    ventana_seleccion.mainloop()

def ver_canchas(deporte):
    global hojas_canchas, frame_tabla_canchas, frame_busqueda_canchas
    global buscar_cancha, buscar_dia, buscar_estado, buscar_horario

    ventana_seleccion.destroy()

    ventana_canchas = Toplevel(ventana_administrador)
    ventana_canchas.title(f"Canchas {deporte}")
    ventana_canchas.geometry("950x650")
    ventana_canchas.resizable(False, False)
    ventana_canchas.configure(background="black")

    frame_tabla_canchas = ctk.CTkFrame(ventana_canchas, fg_color="black")
    frame_tabla_canchas.pack(fill="both", expand=True)
    frame_busqueda_canchas = ctk.CTkFrame(ventana_canchas, fg_color="black", bg_color="black")
    frame_busqueda_canchas.pack(pady=10, fill="x", side="bottom")

    archivo = f"src/JSON/{deporte}.json"
    data = cargar_archivo(archivo)
    if data:
        hojas_canchas = procesar_canchas(data)
        mostrar_datos_canchas(hojas_canchas)
    else:
        messagebox.showerror("ERROR", "No hay datos disponibles.")

    campos = [("Dia", "buscar_dia"), ("Cancha", "buscar_cancha"),
              ("Horario", "buscar_horario"), ("Estado", "buscar_estado")]
    entries = {}
    for placeholder, key in campos:
        e = ctk.CTkEntry(frame_busqueda_canchas, width=125, height=30,
                         placeholder_text=placeholder, placeholder_text_color="white",
                         text_color="white", border_width=2,
                         border_color="#2FB166", fg_color="#2FB166")
        e.pack(side="left", padx=10)
        entries[key] = e

    buscar_dia = entries["buscar_dia"]
    buscar_cancha = entries["buscar_cancha"]
    buscar_horario = entries["buscar_horario"]
    buscar_estado = entries["buscar_estado"]

    ctk.CTkButton(frame_busqueda_canchas, text="Buscar", width=175, height=30,
                  command=filtrar_canchas, fg_color="#2FB166",
                  text_color="white").pack(side="left", padx=10)
    ventana_canchas.mainloop()

def procesar_canchas(data):
    filas = []
    for info in data:
        for cancha, dias in info.items():
            for dia, horarios in dias.items():
                for hora, estado in horarios.items():
                    filas.append({"Cancha": cancha, "Dia": dia, "Horario": hora, "Estado": estado})
    return pd.DataFrame(filas)

def mostrar_datos_canchas(df):
    for widget in frame_tabla_canchas.winfo_children():
        widget.destroy()
    anchos = {"Cancha": 30, "Dia": 20, "Horario": 50, "Estado": 20}
    tree = _crear_treeview(frame_tabla_canchas, ["Cancha", "Dia", "Horario", "Estado"], anchos)
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row), tags=("data_row",))

def filtrar_canchas():
    resultado = hojas_canchas.copy()
    for valor, col in [(buscar_cancha.get(), 'Cancha'), (buscar_dia.get(), 'Dia'),
                       (buscar_estado.get(), 'Estado'), (buscar_horario.get(), 'Horario')]:
        if valor:
            resultado = resultado[resultado[col].str.contains(valor, case=False)]
    mostrar_datos_canchas(resultado)

# ---------- PRECIOS ----------
def gestionar_precios_canchas():
    global frame_tabla_precios
    ventana_precios = Toplevel(ventana_administrador)
    ventana_precios.title("Precios")
    ventana_precios.geometry("500x500")
    ventana_precios.resizable(False, False)
    ventana_precios.configure(background="black")

    frame_tabla_precios = ctk.CTkFrame(ventana_precios, fg_color="black")
    frame_tabla_precios.pack(fill="both", expand=True)

    frame_texto = ctk.CTkFrame(ventana_precios, fg_color="black", bg_color="black")
    frame_texto.pack(fill="x", side="bottom", pady=10)

    try:
        with open("src/JSON/Precios.json", "r", encoding="utf-8") as f:
            data = json.load(f)[0]
    except Exception:
        messagebox.showerror("ERROR", "No se pudieron cargar los precios.")
        return

    mostrar_tabla_precios(data)

    ctk.CTkLabel(frame_texto, text="Doble clic para modificar el precio",
                 text_color="white", font=("Lalezar", 20), anchor="center").pack()
    ventana_precios.mainloop()

def mostrar_tabla_precios(data):
    for widget in frame_tabla_precios.winfo_children():
        widget.destroy()

    anchos = {"Deporte": 100, "Dia": 100, "Noche": 100}
    tree = _crear_treeview(frame_tabla_precios, ["Deporte", "Dia", "Noche"], anchos)

    for deporte, precios in data.items():
        tree.insert("", "end", values=(deporte, precios["Dia"], precios["Noche"]))

    tree.bind("<Double-1>", lambda e: editar_precio(e, tree, data))

def editar_precio(event, tree, data):
    item = tree.selection()
    if not item:
        return
    item = item[0]
    col = int(tree.identify_column(event.x).split("#")[-1]) - 1
    if col > 0:
        deporte = tree.item(item, "values")[0]
        actual = tree.item(item, "values")[col]
        nuevo = simpledialog.askstring("Editar Precio",
                                       f"Nuevo precio para {deporte} ({'Día' if col == 1 else 'Noche'}):",
                                       initialvalue=actual)
        if nuevo:
            vals = list(tree.item(item, "values"))
            vals[col] = nuevo
            tree.item(item, values=vals)
            campo = "Dia" if col == 1 else "Noche"
            data[deporte][campo] = int(nuevo)
            with open("src/JSON/Precios.json", "w", encoding="utf-8") as f:
                json.dump([data], f, ensure_ascii=False, indent=4)

# ---------- MENÚ ----------
def gestionar_menu():
    global frame_tabla_menu

    ventana_menu = Toplevel(ventana_administrador)
    ventana_menu.title("Menú de Precios")
    ventana_menu.geometry("800x600")
    ventana_menu.resizable(False, False)
    ventana_menu.configure(background="black")

    frame_tabla_menu = ctk.CTkFrame(ventana_menu, fg_color="black")
    frame_tabla_menu.pack(fill="both", expand=True)

    frame_busqueda = ctk.CTkFrame(ventana_menu, fg_color="black", bg_color="black")
    frame_busqueda.pack(pady=10, fill="x", side="bottom")

    try:
        with open("src/JSON/Menu.json", "r", encoding="utf-8") as f:
            menu_data = json.load(f)[0]
    except Exception:
        messagebox.showerror("ERROR", "No se pudo cargar el menú.")
        return

    mostrar_tabla_menu(menu_data)

    for tipo in ["Todos", "Entradas", "Principal", "Bebidas", "Postres"]:
        ctk.CTkButton(ventana_menu, text=tipo, fg_color="#2FB166", hover_color="#2FB166",
                      command=lambda t=tipo: mostrar_tabla_menu(menu_data, t),
                      width=100, height=30, corner_radius=20).pack(side="left", padx=10)

    ctk.CTkButton(ventana_menu, text="Agregar Producto", fg_color="#2FB166", hover_color="#2FB166",
                  command=lambda: agregar_producto(menu_data),
                  width=125, height=30, corner_radius=20).pack(side="right", padx=10)

    ctk.CTkLabel(frame_busqueda, text="Doble clic para modificar el precio",
                 text_color="white", font=("Lalezar", 20), anchor="center").pack()
    ventana_menu.mainloop()

def mostrar_tabla_menu(data, tipo="Todos"):
    for widget in frame_tabla_menu.winfo_children():
        widget.destroy()

    anchos = {"Tipo": 100, "Producto": 200, "Precio": 100}
    tree = _crear_treeview(frame_tabla_menu, ["Tipo", "Producto", "Precio"], anchos)

    items = []
    if tipo == "Todos":
        for categoria, productos in data.items():
            for producto, precio in productos.items():
                items.append((categoria, producto, precio))
    else:
        for producto, precio in data.get(tipo, {}).items():
            items.append((tipo, producto, precio))

    for row in items:
        tree.insert("", "end", values=row)

    tree.bind("<Double-1>", lambda e: editar_precio_menu(e, tree, data))

def editar_precio_menu(event, tree, data):
    item = tree.selection()
    if not item:
        return
    item = item[0]
    col = int(tree.identify_column(event.x).split("#")[-1]) - 1
    if col == 2:
        tipo, producto, actual = tree.item(item, "values")
        nuevo = simpledialog.askstring("Editar Precio",
                                       f"Nuevo precio para {producto} ({tipo}):",
                                       initialvalue=actual)
        if nuevo:
            tree.item(item, values=(tipo, producto, nuevo))
            if tipo in data and producto in data[tipo]:
                data[tipo][producto] = int(nuevo)
            with open("src/JSON/Menu.json", "w", encoding="utf-8") as f:
                json.dump([data], f, ensure_ascii=False, indent=4)

def agregar_producto(data):
    tipo = simpledialog.askstring("Nuevo Producto",
                                  "Tipo (Entradas, Principal, Bebidas, Postres):")
    if tipo not in data:
        messagebox.showerror("ERROR", "Tipo no válido.")
        return
    producto = simpledialog.askstring("Nuevo Producto", "Nombre del producto:")
    precio_str = simpledialog.askstring("Nuevo Producto", "Precio:")
    try:
        data[tipo][producto] = int(precio_str)
        mostrar_tabla_menu(data)
        with open("src/JSON/Menu.json", "w", encoding="utf-8") as f:
            json.dump([data], f, ensure_ascii=False, indent=4)
    except (ValueError, TypeError):
        messagebox.showerror("ERROR", "Precio no válido.")

# ---------- RESTAURANTE ----------
ARCHIVO_RESTAURANTE = 'src/JSON/Restaurante.json'

def cargar_datos_restaurante():
    try:
        with open(ARCHIVO_RESTAURANTE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return [{"Lunes": {"Lugares Disponibles": 50, "Lugares Ocupados": 0}}]

def guardar_datos_restaurante(datos):
    with open(ARCHIVO_RESTAURANTE, 'w') as f:
        json.dump(datos, f, indent=4)

def ver_disponibilidad():
    global frame_tabla_disponibilidad

    ventana_disp = Toplevel(ventana_administrador)
    ventana_disp.title("Disponibilidad de Mesas")
    ventana_disp.geometry("450x450")
    ventana_disp.resizable(False, False)
    ventana_disp.configure(background="black")

    frame_tabla_disponibilidad = ctk.CTkFrame(ventana_disp, fg_color="black")
    frame_tabla_disponibilidad.pack(fill="both", expand=True)

    frame_texto = ctk.CTkFrame(ventana_disp, fg_color="black", bg_color="black")
    frame_texto.pack(fill="x", side="bottom", pady=10)

    data = cargar_datos_restaurante()[0]
    if data:
        mostrar_datos_disponibilidad(data)
    else:
        messagebox.showerror("Error", "No hay datos disponibles.")

    ctk.CTkLabel(frame_texto, text="Doble clic para modificar lugares disponibles",
                 text_color="white", font=("Lalezar", 20), anchor="center").pack()
    ventana_disp.mainloop()

def mostrar_datos_disponibilidad(data):
    for widget in frame_tabla_disponibilidad.winfo_children():
        widget.destroy()

    anchos = {"Día": 150, "Lugares Disponibles": 100, "Lugares Ocupados": 100}
    tree = _crear_treeview(frame_tabla_disponibilidad,
                           ["Día", "Lugares Disponibles", "Lugares Ocupados"], anchos)

    for dia, info in data.items():
        tree.insert("", "end",
                    values=(dia, info["Lugares Disponibles"], info["Lugares Ocupados"]))

    tree.bind("<Double-1>", lambda e: editar_lugares(e, tree, data))

def editar_lugares(event, tree, data):
    item = tree.selection()
    if not item:
        return
    item = item[0]
    col = int(tree.identify_column(event.x).split("#")[-1]) - 1
    if col == 1:
        dia = tree.item(item, "values")[0]
        actual = tree.item(item, "values")[1]
        nuevo = simpledialog.askstring("Editar Lugares",
                                       f"Nueva cantidad para {dia}:", initialvalue=actual)
        if nuevo:
            try:
                nuevo = int(nuevo)
                tree.set(item, column="Lugares Disponibles", value=nuevo)
                data[dia]["Lugares Disponibles"] = nuevo
                with open(ARCHIVO_RESTAURANTE, "w", encoding="utf-8") as f:
                    json.dump([data], f, ensure_ascii=False, indent=4)
            except ValueError:
                messagebox.showerror("ERROR", "Ingresá un número válido.")

# ---------- MAIN ----------
administrador()
ventana_administrador.mainloop()