from tkinter import *
from tkinter import ttk
from tkinter import messagebox as MessageBox
from PIL import Image, ImageTk
import sv_ttk

def ventana_jugar():
    jugar_ventana = Toplevel()
    sv_ttk.set_theme("dark")
    jugar_ventana.title("Jugar - Kakuro - 2023152240")
    jugar_ventana.geometry("800x800")
    jugar_ventana.minsize(800, 800)
    jugar_ventana.maxsize(800, 800)
    
    logo_jugar = ImageTk.PhotoImage(Image.open("assets/title_logo.png").resize((119, 32), Image.LANCZOS))
    logo_jugar_label = Label(jugar_ventana, image=logo_jugar)
    logo_jugar_label.image = logo_jugar
    logo_jugar_label.place(x=10, y= 10, anchor=NW)
    
    player_name = Label(jugar_ventana, fg="white", text="Jugador: Tony Barrantes")
    player_name.place(relx = 0.3, y= 10, relwidth=0.4,  anchor=NW)
    
    current_number = [0]
    def select_number(button):
        def select():
            for e_button in numeros_botones:
                e_button.configure(bg="#1C1C1C", fg="white")
            if current_number[-1] == button:
                current_number.append(0)
            else:
                current_number.append(button)
                numeros_botones[button - 1].configure(bg="white", fg="#1C1C1C")
            print(curr_num())
        return select
    def curr_num():
        return current_number[-1]
    def place_number(i, j):
        def place():
            if curr_num() == 0:
                MessageBox.showerror("Selecciona un número", "Para ingresar un número al Kakuro, se debe haber seleccionado uno previamente")
            else:
                matriz[i][j].configure(text=f"{curr_num()}")
                current_number.append(0)
                for e_button in numeros_botones:
                    e_button.configure(bg="#1C1C1C", fg="white")
        return place
        
    matriz = []
    for i in range(10):
        sublista = []
        for j in range(10):
            entry = Button(jugar_ventana, height = 2, width=5, font=("Arial", 10))  
            # entry.insert(END, f"   \  22 \n    \ \n 2  \ ")  
            entry.place(x= 30 + i*50,y= 60 + j*50, anchor=NW)
            sublista = sublista + [entry]
            sublista[-1].config(command=place_number(i, j))
        matriz = matriz + [sublista]
    
    numeros_botones = []
    for n in range(1, 10):
        boton = Button(jugar_ventana, height = 3, width=7, text=f"{n}", font=("Arial", 10))
        numeros_botones = numeros_botones + [boton]
        numeros_botones[-1].config(command=select_number(n))
        boton.place(x= 650, y= 60 + n*50, anchor=NW)
    
    boton_iniciar = Button(jugar_ventana, height = 2, width=14, text="Iniciar \n Juego", font=("Arial", 10), bg="#FF0066")
    boton_undo = Button(jugar_ventana, height = 2, width=14, text="Deshacer \n Jugada", font=("Arial", 10), bg="#0FD1DB")
    boton_borrar_casilla = Button(jugar_ventana, height = 2, width=14, text="Borrar \n Casilla", font=("Arial", 10), bg="#FFD700")
    boton_top10 = Button(jugar_ventana, height = 2, width=14, text="Top 10", font=("Arial", 10), bg="#00B050")
    
    boton_iniciar.place(x= 40, y= 580, anchor=NW)
    boton_undo.place(x= 220, y= 580, anchor=NW)
    boton_borrar_casilla.place(x= 400, y= 580, anchor=NW)
    boton_top10.place(x= 580, y= 580, anchor=NW)
    
    boton_redo = Button(jugar_ventana, height = 2, width=14, text="Rehacer \n Jugada", font=("Arial", 10), bg="#FF0066")
    boton_borrar_juego = Button(jugar_ventana, height = 2, width=14, text="Borrar \n Juego", font=("Arial", 10), bg="#0FD1DB")
    boton_guardar = Button(jugar_ventana, height = 2, width=14, text="Guardar \n Juego", font=("Arial", 10), bg="#FFD700")
    
    boton_redo.place(x= 220, y= 660, anchor=NW)
    boton_borrar_juego.place(x= 400, y= 660, anchor=NW)
    boton_guardar.place(x= 580, y= 660, anchor=NW)
    
    boton_terminar = Button(jugar_ventana, height = 2, width=14, text="Terminar \n Juego", font=("Arial", 10), bg="#FF0066")
    boton_cargar = Button(jugar_ventana, height = 2, width=14, text="Cargar \n Juego", font=("Arial", 10), bg="#0FD1DB")
    
    boton_terminar.place(x= 400, y= 740, anchor=NW)
    boton_cargar.place(x= 580, y= 740, anchor=NW)
        
    
    
    return