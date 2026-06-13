# 🏟️ El Andén — Sistema de Gestión Deportiva y Gastronómica

Sistema de escritorio desarrollado en Python para la gestión integral de un complejo deportivo: reservas de canchas de fútbol, tenis y pádel, restaurante con menú digital, sistema de beneficios con puntos y panel de administración.

---

## 📋 Descripción

El Andén es una aplicación de escritorio construida con `customtkinter` que permite a los usuarios registrarse, iniciar sesión y gestionar reservas de canchas y mesas del restaurante, mientras que los administradores pueden supervisar disponibilidad, precios y reservas en tiempo real.

> **Nota:** Este proyecto fue desarrollado originalmente en equipo en un repositorio privado. Este repositorio es una copia personal donde apliqué mejoras de seguridad y refactorización al código original.

---

## ✨ Funcionalidades

### 👤 Usuario
- Registro e inicio de sesión con persistencia en JSON
- Perfil personalizable: foto, nombre, mail y contraseña
- Reserva de canchas de **Fútbol 5**, **Fútbol 8**, **Tenis** y **Pádel**
- Selección de día, horario y cancha con disponibilidad en tiempo real
- Pago con opción de **seña (1/3)** o **pago total**
- Generación de **código QR** para el pago
- Reserva de mesas en el restaurante con selección de día y cantidad de comensales
- Consulta y **cancelación de reservas** propias
- Sistema de **puntos** acumulables por reservas, canjeables por beneficios
- Visualización del **menú** del restaurante con precios
- Confirmación de reserva por **correo electrónico automático**

### 🛠️ Administrador (`Admin.py`)
- Panel de administración independiente
- Visualización y filtrado de todas las reservas (canchas y restaurante)
- Eliminación de reservas con notificación automática al usuario por mail
- Consulta de disponibilidad de canchas por deporte, día y horario
- Gestión de precios de canchas (modificación en tabla con doble clic)
- Gestión del menú del restaurante: modificar precios y agregar productos
- Control de lugares disponibles en el restaurante por día

---

## 🗂️ Estructura del Proyecto
---
El-Anden/

├── src/

│   ├── main.py               # Aplicación principal (usuario)

│   ├── Admin.py              # Panel de administración

│   ├── JSON/

│   │   ├── Usuarios.json

│   │   ├── Reservas.json

│   │   ├── ReservasRestaurante.json

│   │   ├── Futbol.json

│   │   ├── Tenis.json

│   │   ├── Padel.json

│   │   ├── Menu.json

│   │   ├── Precios.json

│   │   └── Restaurante.json

│   └── Imagenes/

│       ├── Fondos/

│       ├── Botones/

│       ├── FotosPerfil/

│       └── Productos/

├── .env.example

├── .gitignore

├── requirements.txt

└── README.md

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
|---|---|
| Python 3 | Lenguaje principal |
| customtkinter | Interfaz gráfica moderna |
| tkinter / ttk | Componentes adicionales de UI |
| Pillow (PIL) | Manejo de imágenes |
| pandas | Procesamiento de datos en tablas |
| qrcode | Generación de QR para pagos |
| smtplib | Envío de correos automáticos |
| JSON | Persistencia de datos |

---

## ⚙️ Instalación

**Requisitos:** Python 3.10 o superior

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/El-Anden.git
cd El-Anden

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Instalar la fuente Lalezar (incluida en el repositorio)
# Hacer doble clic en el archivo .ttf e instalar

# Ejecutar la aplicación
python src/main.py

# Ejecutar el panel de administración
python src/Admin.py
```

---

## 👥 Equipo

Desarrollado por estudiantes del Instituto Técnico Industrial Huergo como proyecto integrador de 4to año.

---

## 📄 Licencia

Este proyecto fue desarrollado con fines educativos.