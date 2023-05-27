from tkinter import *
from tkinter import ttk
from tkinter import messagebox as MessageBox
from PIL import Image, ImageTk
import sv_ttk
import json

def ventana_configurar():
    configurar_ventana = Toplevel()
    sv_ttk.set_theme("dark")
    configurar_ventana.title("Configurar - Kakuro - 2023152240")
    configurar_ventana.geometry("400x400")
    configurar_ventana.minsize(400, 400)
    configurar_ventana.maxsize(400, 400)
    configurar_ventana.iconbitmap("assets/logo.ico")
    # Despliegue del logo
    logo_jugar = ImageTk.PhotoImage(Image.open("assets/title_logo.png").resize((119, 32), Image.LANCZOS))
    logo_jugar_label = Label(configurar_ventana, image=logo_jugar)
    logo_jugar_label.image = logo_jugar
    logo_jugar_label.place(x=10, y= 10, anchor=NW)
    # Lectura de las configuraciones actuales
    with open("configs\kakuro2023configuración.dat", "r") as file:
        configuracion = file.read()
    configuracion = json.loads(configuracion)
    
    # Opciones de nivel
    nivel_label = Label(configurar_ventana, text="Nivel", font=("Arial", 22))
    nivel_label.place(x= 10, y= 70, anchor=NW)
    niveles = ["Fácil", "Medio", "Difícil", "Experto"]
    nivel = StringVar()
    nivel.set(niveles[configuracion["NIVEL"] - 1])
    niveles_menu = OptionMenu(configurar_ventana, nivel, *niveles)
    niveles_menu.place(x= 10, y= 120, anchor=NW)
    
    # Opciones de reloj
    reloj_label = Label(configurar_ventana, text="Reloj", font=("Arial", 22))
    reloj_label.place(x= 10, y= 170, anchor=NW)
    relojes = ["Cronómetro", "No usar reloj", "Timer"]
    reloj = StringVar()
    reloj.set(relojes[configuracion["RELOJ"] - 1])
    relojes_menu = OptionMenu(configurar_ventana, reloj, *relojes)
    relojes_menu.place(x= 10, y= 220, anchor=NW)
    
    # Boton guardar
    def guardar_configuraciones(nivel, reloj, configuraciones):
        configuracion = json.dumps({"NIVEL": niveles.index(nivel) + 1, "RELOJ": relojes.index(reloj) + 1})
        with open("configs\kakuro2023configuración.dat", "w") as file:
            file.write(configuracion)
            MessageBox.showinfo("Configuración", "Configuración guardada con éxito")
            Toplevel.destroy(configurar_ventana)

    boton_guardar = Button(configurar_ventana, text="Guardar configuración", command=lambda: guardar_configuraciones(nivel.get(), reloj.get(), configuracion), bg="#0FD1DB", height=2, width=30)
    boton_guardar.place(x= 10, y= 270, anchor=NW)