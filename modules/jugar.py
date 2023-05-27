from tkinter import *
from tkinter import ttk
from tkinter import messagebox as MessageBox
from PIL import Image, ImageTk
import sv_ttk
import json
import random

def ventana_jugar():
    # Inicialización de la ventana
    jugar_ventana = Toplevel()
    sv_ttk.set_theme("dark")
    jugar_ventana.title("Jugar - Kakuro - 2023152240")
    jugar_ventana.geometry("800x800")
    jugar_ventana.minsize(800, 800)
    jugar_ventana.maxsize(800, 800)
    jugar_ventana.iconbitmap("assets/logo.ico")
    # Despliegue del logo
    logo_jugar = ImageTk.PhotoImage(Image.open("assets/title_logo.png").resize((119, 32), Image.LANCZOS))
    logo_jugar_label = Label(jugar_ventana, image=logo_jugar)
    logo_jugar_label.image = logo_jugar
    logo_jugar_label.place(x=10, y= 10, anchor=NW)
    # Despliegue del nombre del jugador
    player_name = Label(jugar_ventana, fg="white", text="Jugador: Tony Barrantes")
    player_name.place(relx = 0.3, y= 10, relwidth=0.4,  anchor=NW)
    # Se inicia la lista de current number, esta se usa para definir cual número se encuentra seleccionado actualmente
    current_number = [0]
    # Función que se encarga de seleccionar un número en los botones y lo envia a la lista de current_number
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
    # Función que valida ingresar el número en la casilla seleccionada
    def validar_numero(num, i, j):
        # Valida columna
        it_j = j
        datos_columna =[(0, 0), 0, 0]
        while True:
            if matriz[i-1][it_j-1]["state"] == "disabled":
                for n in partida_actual:
                    if n == (it_j, i):
                        for k in partida_actual[n]:
                            if k[0] == 2:
                                datos_columna = [n, int(k[1]), int(k[2])]
                break
            else:
                it_j = it_j - 1
        sumatoria_columna = 0
        numeros_columna = []
        if datos_columna[1] != 0:
            for k in range(datos_columna[2]):
                num_casilla = matriz[datos_columna[0][1]-1][datos_columna[0][0]+k]['text']
                numeros_columna.append(num_casilla)
                if num_casilla.isnumeric():
                    sumatoria_columna = sumatoria_columna + int(num_casilla)
        sumatoria_columna = sumatoria_columna + num
        if str(num) in numeros_columna:
            MessageBox.showerror("Error", "JUGADA NO ES VÁLIDA PORQUE EL NÚMERO YA ESTÁ EN SU GRUPO DE COLUMNA")
            return False
        if sumatoria_columna > datos_columna[1]:
            MessageBox.showerror("Error", f"JUGADA NO ES VÁLIDA PORQUE LA SUMA DE LA COLUMNA ES {str(sumatoria_columna)} Y LA CLAVE NUMÉRICA ES {str(datos_columna[1])}")
            return False
        # Valida fila
        it_i = i
        datos_fila =[(0, 0), 0, 0]
        print(f"i: {i}, j: {j}")
        while True:
            if matriz[it_i-1][j-1]["state"] == "disabled":
                for n in partida_actual:
                    if n == (j, it_i):
                        for k in partida_actual[n]:
                            if k[0] == 1:
                                datos_fila = [n, int(k[1]), int(k[2])]
                break
            else:
                it_i = it_i - 1
        print(datos_fila)
        sumatoria_fila = 0
        numeros_fila = []
        if datos_fila[1] != 0:
            for k in range(datos_fila[2]):
                num_casilla = matriz[datos_fila[0][1]+k][datos_fila[0][0]-1]['text']
                numeros_fila.append(num_casilla)
                if num_casilla.isnumeric():
                    sumatoria_fila = sumatoria_fila + int(num_casilla)
        sumatoria_fila = sumatoria_fila + num
        if str(num) in numeros_fila:
            MessageBox.showerror("Error", "JUGADA NO ES VÁLIDA PORQUE EL NÚMERO YA ESTÁ EN SU GRUPO DE FILA")
            return False    
        if sumatoria_fila > datos_fila[1]:
            MessageBox.showerror("Error", f"JUGADA NO ES VÁLIDA PORQUE LA SUMA DE LA FILA ES {str(sumatoria_fila)} Y LA CLAVE NUMÉRICA ES {str(datos_fila[1])}")
            return False  
        return True
    
    # Función que retorna el número seleccionado actualmente
    def curr_num():
        return current_number[-1]
    # Función que coloca un número en la casilla seleccionada
    def place_number(i, j):
        def place():
            if curr_num() == 0:
                MessageBox.showerror("Selecciona un número", "Para ingresar un número al Kakuro, se debe haber seleccionado uno previamente")
            elif validar_numero(curr_num(), i, j) == True:
                matriz[i-1][j-1].configure(text=f"{curr_num()}")
                current_number.append(0)
                for e_button in numeros_botones:
                    e_button.configure(bg="#1C1C1C", fg="white")
        return place
    # Creación del tablero de juego
    matriz = []
    for i in range(1, 10):
        sublista = []
        for j in range(1, 10):
            entry = Button(jugar_ventana, height = 2, width=5, font=("Arial", 9), bg="white", fg="#1C1C1C", relief=FLAT) 
            entry.configure(state=DISABLED) 
            # entry.insert(END, f"   \  22 \n    \ \n 2  \ ")  
            entry.place(x= 30 + i*50,y= 60 + j*50, anchor=NW)
            sublista = sublista + [entry]
            sublista[-1].config(command=place_number(i, j))
        matriz = matriz + [sublista]
    # Creación de los botones de números
    numeros_botones = []
    for n in range(1, 10):
        boton = Button(jugar_ventana, height = 3, width=7, text=f"{n}", font=("Arial", 10))
        numeros_botones = numeros_botones + [boton]
        numeros_botones[-1].config(command=select_number(n))
        boton.place(x= 650, y= 60 + n*50, anchor=NW)
    # Primera fila de botones
    boton_iniciar = Button(jugar_ventana, height = 2, width=14, text="Iniciar \n Juego", font=("Arial", 10), bg="#FF0066")
    boton_undo = Button(jugar_ventana, height = 2, width=14, text="Deshacer \n Jugada", font=("Arial", 10), bg="#0FD1DB")
    boton_borrar_casilla = Button(jugar_ventana, height = 2, width=14, text="Borrar \n Casilla", font=("Arial", 10), bg="#FFD700")
    boton_top10 = Button(jugar_ventana, height = 2, width=14, text="Top 10", font=("Arial", 10), bg="#00B050")
    
    boton_iniciar.place(x= 40, y= 580, anchor=NW)
    boton_undo.place(x= 220, y= 580, anchor=NW)
    boton_borrar_casilla.place(x= 400, y= 580, anchor=NW)
    boton_top10.place(x= 580, y= 580, anchor=NW)
    # Segunda fila de botones
    boton_redo = Button(jugar_ventana, height = 2, width=14, text="Rehacer \n Jugada", font=("Arial", 10), bg="#FF0066")
    boton_borrar_juego = Button(jugar_ventana, height = 2, width=14, text="Borrar \n Juego", font=("Arial", 10), bg="#0FD1DB")
    boton_guardar = Button(jugar_ventana, height = 2, width=14, text="Guardar \n Juego", font=("Arial", 10), bg="#FFD700")
    
    boton_redo.place(x= 220, y= 660, anchor=NW)
    boton_borrar_juego.place(x= 400, y= 660, anchor=NW)
    boton_guardar.place(x= 580, y= 660, anchor=NW)
    # Tercera fila de botones
    boton_terminar = Button(jugar_ventana, height = 2, width=14, text="Terminar \n Juego", font=("Arial", 10), bg="#FF0066")
    boton_cargar = Button(jugar_ventana, height = 2, width=14, text="Cargar \n Juego", font=("Arial", 10), bg="#0FD1DB")
    
    boton_terminar.place(x= 400, y= 740, anchor=NW)
    boton_cargar.place(x= 580, y= 740, anchor=NW)
        
    # Obtener los tableros
    with open("configs/kakuro2023partidas.dat", "r") as file:
        partidas = file.read()
    # Cambiar los parentesis por corchetes para leerlo como json
    for n in range(partidas.count("(")):
        partidas = partidas.replace("(", "[")
        partidas = partidas.replace(")", "]")
    # Lee el archivo como json
    partidas = json.loads(partidas)
    # Cambia las listas por tuplas
    for n in partidas:
        for i in partidas[n]:
            for j in i:
                partidas[n][partidas[n].index(i)][i.index(j)] = tuple(j)
            partidas[n][partidas[n].index(i)] = tuple(i)
        partidas[n] = tuple(partidas[n])
    
    partidas = partidas["FACIL"]
    partida_actual = random.choice(partidas)
    partidas = list(partidas)
    partidas.remove(partida_actual)
    partidas = tuple(partidas)
    print(partida_actual)
    partida_actual_orden = {}
    for i in partida_actual:
        if partida_actual_orden.get((i[2], i[3])) == None:
            partida_actual_orden[i[2], i[3]] = [(i[0], i[1], i[4])]
        else:
            partida_actual_orden[i[2], i[3]] = partida_actual_orden[i[2], i[3]] + [(i[0], i[1], i[4])]
    partida_actual = partida_actual_orden
    del partida_actual_orden
    for i in partida_actual:
        partida_actual[i].sort(key=lambda x: x[0])
    
    # Rellenar el tablero con los valores de la partida
    for k in partida_actual:
        # Obtiene la suma de la fila y columna, si no existe, se deja un string vacío
        if len(partida_actual[k]) == 2:
            fila_suma = str(partida_actual[k][0][1])
            columna_suma = str(partida_actual[k][1][1])
        elif partida_actual[k][0][0] == 1:
            fila_suma = str(partida_actual[k][0][1])
            columna_suma = " "
        else:
            fila_suma = " "
            columna_suma = str(partida_actual[k][0][1])
        # Obtiene la posición de la casilla y crea el texto que se debe insertar en la misma  
        i = k[0] - 1
        j = k[1] - 1
        texto = f"   \  {fila_suma} \n    \ \n {columna_suma}  \ "
        matriz[j][i].configure(text=texto)
        # Cambia el color y el estado de las casillas consideradas por dicha fila o columna
        if fila_suma.isnumeric() == True:
            print(fila_suma)
            fila_suma = int(fila_suma)
            for n in range(partida_actual[k][0][2]):
                matriz[j+n+1][i].configure(bg="#666666", fg="white", state=NORMAL)
        if columna_suma.isnumeric() == True:
            print(columna_suma)
            columna_suma = int(columna_suma)
            for n in range(partida_actual[k][-1][2]):
                matriz[j][i+n+1].configure(bg="#666666", fg="white", state=NORMAL)
        
    
    
    
        
    return