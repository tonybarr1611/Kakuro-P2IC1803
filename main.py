from tkinter import *
from tkinter import ttk
from tkinter import messagebox as MessageBox
from PIL import Image, ImageTk
import sv_ttk
from modules.jugar import ventana_jugar
from modules.configurar import ventana_configurar
def acerca_de():
    MessageBox.showinfo("Acerca de", "V1.0 Kakuro\n \nDesarrollado por:\n Anthony Barrantes Jiménez  - 2023152240 \n Creado: \n mes de mayo de 2023")
def main(ventana):
    ventana.title("Kakuro - 2023152240")
    ventana.geometry("500x500")
    ventana.minsize(500,500)
    ventana.maxsize(500,500)
    
    # Icono de la ventana
    ventana.iconbitmap("assets/logo.ico")
    # Despliega una imagen en la columna 1, fila 0
    logo = ImageTk.PhotoImage(Image.open("assets/title_logo.png").resize((180, 48), Image.LANCZOS))
    logo_label = Label(ventana, image=logo)
    logo_label.image = logo 
    logo_label.place(x= 160, y= 50)
    
    # Pide el nombre del jugador
    nombre_label = Label(ventana, text="Nombre del jugador:", font=("Arial", 8))
    nombre_label.place(relx= 0.5, y= 120, anchor=N)
    nombre_entry = Entry(ventana, font=("Arial", 8))
    nombre_entry.place(relx= 0.5, y= 135, anchor=N)
    nombre_entry.insert(0, "a")
    # Verifica que se haya añadido un nombre de jugador
    def ejecutar_juego():
        nombre_jugador = nombre_entry.get()
        if nombre_jugador == "":
            MessageBox.showerror("Error", "Debe ingresar un nombre de jugador")
            return
        else:
            ventana_jugar(nombre_jugador)
    # Botones
    boton_jugar = Button(ventana, text="Jugar", command=lambda: ejecutar_juego(), bg="#FF0066", height=2, width=30)
    boton_jugar.place(relx= 0.5, y= 200, anchor=N)
    
    boton_configurar = Button(ventana, text="Configurar", command=lambda: ventana_configurar(), bg="#0FD1DB", height=2, width=30)
    boton_configurar.place(relx= 0.5, y = 250, anchor=N)
    
    boton_ayuda = Button(ventana, text="Ayuda", command=lambda: print("Ayuda"), bg="#FFD700", height=2, width=30)
    boton_ayuda.place(relx= 0.5, y = 300, anchor=N)
    
    boton_acerca_de = Button(ventana, text="Acerca de", command=lambda: acerca_de(), bg="#00B050", height=2, width=30)
    boton_acerca_de.place(relx= 0.5, y = 350, anchor=N)
    
    boton_salir = Button(ventana, text="Salir", command=lambda: exit(), bg="#ED7D31", height=2, width=30)
    boton_salir.place(relx= 0.5, y = 400, anchor=N)
    

root = Tk()
main(root)
sv_ttk.set_theme("dark")
root.mainloop()