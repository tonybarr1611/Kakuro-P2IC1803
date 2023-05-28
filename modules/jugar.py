from tkinter import *
from tkinter import ttk
from tkinter import messagebox as MessageBox
from PIL import Image, ImageTk
import sv_ttk
import json
import random
import time
import datetime

def ventana_jugar(player_name):
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
    player_name_label = Label(jugar_ventana, fg="white", text=f"Jugador: {player_name}")
    player_name_label.place(relx = 0.3, y= 10, relwidth=0.4,  anchor=NW)
    # Se inicia la lista de current number, esta se usa para definir cual número se encuentra seleccionado actualmente
    current_number = [0]
    # Variable que indica el estado del juego
    game_state = False
    # Se inician las pilas
    undo_pila = []
    redo_pila = []
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
    def verificar_tablero():
        for i in range(9):
            for j in range(9):
                if matriz[i][j]["state"] == "normal" and matriz[i][j]["text"] == "":
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
            elif curr_num() != 10 and validar_numero(curr_num(), i, j) == True:
                undo_pila.append((i, j, matriz[i-1][j-1]["text"]))
                matriz[i-1][j-1].configure(text=f"{curr_num()}")
                current_number.append(0)
                for e_button in numeros_botones:
                    e_button.configure(bg="#1C1C1C", fg="white")
                boton_borrar_casilla.configure(bg="#FFD700", fg="white")      
            elif curr_num() == 10:
                if matriz[i-1][j-1]["text"] == "":
                    MessageBox.showerror("Error", "ESTA CASILLA NO SE PUEDE BORRAR")
                else:
                    undo_pila.append((i, j, matriz[i-1][j-1]["text"]))
                    matriz[i-1][j-1].configure(text="")
                    current_number.append(0)
                for e_button in numeros_botones:
                    e_button.configure(bg="#1C1C1C", fg="white")
                boton_borrar_casilla.configure(bg="#FFD700", fg="white")
            if verificar_tablero() == True:
                jugar_ventana.after_cancel(reloj_loop_id)
                MessageBox.showinfo("FELICIDADES", f" ¡EXCELENTE {player_name}! TERMINÓ EL JUEGO CON ÉXITO")
                if configuracion["RELOJ"] == 2:
                    player_time = "99:99:99"
                else:
                    player_time = reloj_actual.get()
                    if configuracion["RELOJ"] == 3:
                        print(type(player_time))
                        player_time = (datetime.datetime.strptime(f"{horas_temp}:{minutos_temp}:{segundos_temp}", "%H:%M:%S") - datetime.datetime.strptime(player_time, "%H:%M:%S"))
                        player_time = str(player_time)

                with open("configs/kakuro2023top10.dat", "r") as file:
                    top10 = file.read()
                top10 = json.loads(top10)
                top_nivel = top10[niveles[configuracion["NIVEL"]-1]]
                for n in top_nivel:
                    if top_nivel[n] == "()":
                        top_nivel[n] = (player_name, player_time)
                        break
                    else:
                        if datetime.datetime.strptime(player_time, "%H:%M:%S") < datetime.datetime.strptime(top_nivel[n][1], "%H:%M:%S"):
                            for k in range(10, int(n), -1):
                                top_nivel[str(k)] = top_nivel[str(k-1)]
                            top_nivel[n] = (player_name, player_time)
                            break
                top10[niveles[configuracion["NIVEL"]-1]] = top_nivel
                with open("configs/kakuro2023top10.dat", "w") as file:
                    file.write(json.dumps(top10))
                
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
        boton = Button(jugar_ventana, height = 3, width=7, text=f"{n}", font=("Arial", 10), state=DISABLED)
        numeros_botones = numeros_botones + [boton]
        numeros_botones[-1].config(command=select_number(n))
        boton.place(x= 650, y= 60 + n*50, anchor=NW)
    # Función undo o deshacer
    def undo():
        if len(undo_pila) == 0:
            MessageBox.showerror("Error", "No hay jugadas para deshacer")
            return
        print(undo_pila[-1])
        redo_pila.append(undo_pila[-1][:2] + (matriz[undo_pila[-1][0]-1][undo_pila[-1][1]-1]['text'],))
        matriz[undo_pila[-1][0]-1][undo_pila[-1][1]-1].configure(text=undo_pila[-1][2])
        undo_pila.pop()
    # Función redo o rehacer
    def redo():
        if len(redo_pila) == 0:
            MessageBox.showerror("Error", "No hay jugadas para rehacer")
            return
        undo_pila.append(redo_pila[-1][:2] + (matriz[redo_pila[-1][0]-1][redo_pila[-1][1]-1]['text'],))
        print(redo_pila[-1][2])
        matriz[redo_pila[-1][0]-1][redo_pila[-1][1]-1].configure(text=redo_pila[-1][2])
        redo_pila.pop()
    # Función borrar casilla
    def borrar_casilla():
        for e_button in numeros_botones:
            e_button.configure(bg="#1C1C1C", fg="white")
        if current_number[-1] == 10:
            current_number.append(0)
            boton_borrar_casilla.configure(bg="#FFD700", fg="white")
        else:
            current_number.append(10)
            boton_borrar_casilla.configure(bg="white", fg="#1C1C1C")
    # Función guardar juego
    def guardar_juego():
        print("guardar")
        juego_actual = {}
        for j in matriz:
            juego_actual[matriz.index(j)] = {}
            for i in j:
                juego_actual[matriz.index(j)][j.index(i)] = i.cget("text")
        partida_guardar = {"juego_actual": juego_actual, "undo_pila": undo_pila, "redo_pila": redo_pila}
        partida_guardar = json.dumps(partida_guardar)
        with open("configs/kakuro2023juegoactual.dat", "w") as file:
            file.write(partida_guardar)
        if MessageBox.askquestion("Guardar", "¿VA A CONTINUAR JUGANDO?") == "yes":
            pass
        else:
            jugar_ventana.destroy()
    # Función cargar juego
    def cargar_juego():
        with open("configs/kakuro2023juegoactual.dat", "r") as file:
            partida_cargar = file.read()
        partida_cargar = json.loads(partida_cargar)
        print(partida_cargar["juego_actual"])
        for j in matriz:
            print(partida_cargar["juego_actual"][str(matriz.index(j))])
            for i in j:
                print(partida_cargar["juego_actual"][str(matriz.index(j))][str(j.index(i))])
                i.configure(text=partida_cargar["juego_actual"][str(matriz.index(j))][str(j.index(i))])
        undo_pila = partida_cargar["undo_pila"]
        redo_pila = partida_cargar["redo_pila"]
    # Función iniciar juego       
    def iniciar_juego():
        global horas_temp, minutos_temp, segundos_temp
        if configuracion["RELOJ"] == 3:
            horas_temp = reloj_horas_valor.get()
            minutos_temp = reloj_minutos_valor.get()
            segundos_temp = reloj_segundos_valor.get()
            print(f"horas: {horas_temp}, minutos: {minutos_temp}, segundos: {segundos_temp}")
            if horas_temp == "" and minutos_temp == "" and segundos_temp == "":
                MessageBox.showerror("Error", "Por favor ingrese un tiempo valido")
                return
            if horas_temp.isnumeric() and minutos_temp.isnumeric() and segundos_temp.isnumeric():
                if int(horas_temp) > 2 or int(minutos_temp) > 59 or int(minutos_temp) < 0 or int(segundos_temp) > 59 or int(segundos_temp) < 0:
                    MessageBox.showerror("Error", "Por favor ingrese un tiempo valido")
                    return
                if int(horas_temp) == 0 and int(minutos_temp) == 0 and int(segundos_temp) == 0:
                    MessageBox.showerror("Error", "Por favor ingrese un tiempo valido")
                    return
            else:
                MessageBox.showerror("Error", "Por favor ingrese un tiempo valido")
                return
        if configuracion["RELOJ"] == 1 or configuracion["RELOJ"] == 3:
            reloj_horas.destroy()
            reloj_minutos.destroy()
            reloj_segundos.destroy()
            horas_temp = reloj_horas_valor.get()
            minutos_temp = reloj_minutos_valor.get()
            segundos_temp = reloj_segundos_valor.get()
            reloj_horas_valor.destroy()
            reloj_minutos_valor.destroy()
            reloj_segundos_valor.destroy()
            def cronometro():
                reloj_actual.set((datetime.datetime.strptime(reloj_actual.get(), "%H:%M:%S") + datetime.timedelta(seconds=1)).strftime("%H:%M:%S"))
                global reloj_loop_id
                reloj_loop_id = jugar_ventana.after(1000, cronometro)
            def timer():
                reloj_actual.set((datetime.datetime.strptime(reloj_actual.get(), "%H:%M:%S") - datetime.timedelta(seconds=1)).strftime("%H:%M:%S"))
                if reloj_actual.get() == "00:00:00":
                    if MessageBox.askquestion("Tiempo expirado", "¿DESEA CONTINUAR EL MISMO JUEGO?") == 'yes':
                        reloj_actual.set(f"{horas_temp}:{minutos_temp}:{segundos_temp}")
                        configuracion["RELOJ"] = 1
                        cronometro()
                    else:
                        jugar_ventana.destroy()
                    return
                global reloj_loop_id
                reloj_loop_id = jugar_ventana.after(1000, timer)
            global reloj_actual
            reloj_actual = StringVar()
            reloj_label = Label(jugar_ventana, textvariable=reloj_actual, font=("Arial", 20), bg="#1C1C1C", fg="white")
            reloj_label.place(x= 20, y= 700, anchor=NW)
            if configuracion["RELOJ"] == 1:
                reloj_actual.set("00:00:00")
                cronometro()
            else:
                reloj_actual.set(f"{horas_temp}:{minutos_temp}:{segundos_temp}")
                timer()
                
        for e_button in numeros_botones:
            e_button.configure(state=NORMAL)
        boton_borrar_casilla.configure(state=NORMAL)
        boton_iniciar.configure(state=DISABLED)
        boton_top10.configure(state=DISABLED)
        boton_cargar.configure(state=DISABLED)
        boton_guardar.configure(state=NORMAL)
        boton_undo.configure(state=NORMAL)
        boton_redo.configure(state=NORMAL)   
        game_state = True
        boton_borrar_juego.config(command=lambda: reiniciar_tablero(partida_actual, matriz, game_state))
        boton_terminar.config(command=lambda: terminar_juego(matriz, game_state, partidas))
    # Primera fila de botones
    boton_iniciar = Button(jugar_ventana, height = 2, width=14, text="Iniciar \n Juego", command=iniciar_juego, font=("Arial", 10), bg="#FF0066")
    boton_undo = Button(jugar_ventana, height = 2, width=14, text="Deshacer \n Jugada", command=undo, font=("Arial", 10), bg="#0FD1DB")
    boton_borrar_casilla = Button(jugar_ventana, height = 2, width=14, text="Borrar \n Casilla", command=borrar_casilla, font=("Arial", 10), bg="#FFD700", state=DISABLED)
    boton_top10 = Button(jugar_ventana, height = 2, width=14, text="Top 10", font=("Arial", 10), bg="#00B050")
    
    boton_iniciar.place(x= 40, y= 580, anchor=NW)
    boton_undo.place(x= 220, y= 580, anchor=NW)
    boton_borrar_casilla.place(x= 400, y= 580, anchor=NW)
    boton_top10.place(x= 580, y= 580, anchor=NW)
    # Segunda fila de botones
    boton_redo = Button(jugar_ventana, height = 2, width=14, text="Rehacer \n Jugada", command=redo, font=("Arial", 10), bg="#FF0066")
    boton_borrar_juego = Button(jugar_ventana, height = 2, width=14, text="Borrar \n Juego", font=("Arial", 10), bg="#0FD1DB")
    boton_guardar = Button(jugar_ventana, height = 2, width=14, text="Guardar \n Juego", command=guardar_juego, font=("Arial", 10), bg="#FFD700")
    
    boton_redo.place(x= 220, y= 660, anchor=NW)
    boton_borrar_juego.place(x= 400, y= 660, anchor=NW)
    boton_guardar.place(x= 580, y= 660, anchor=NW)
    # Tercera fila de botones
    boton_terminar = Button(jugar_ventana, height = 2, width=14, text="Terminar \n Juego", font=("Arial", 10), bg="#FF0066")
    boton_cargar = Button(jugar_ventana, height = 2, width=14, text="Cargar \n Juego", command=cargar_juego, font=("Arial", 10), bg="#0FD1DB")
    
    boton_terminar.place(x= 400, y= 740, anchor=NW)
    boton_cargar.place(x= 580, y= 740, anchor=NW)
    # Obtiene las configuraciones del archivo de configuración
    with open("configs\kakuro2023configuración.dat", "r") as file:
        configuracion = file.read()
    configuracion = json.loads(configuracion)
    
    if configuracion["RELOJ"] == 1 or configuracion["RELOJ"] == 3:
        reloj_horas = Label(jugar_ventana, text="Horas", font=("Arial", 10), borderwidth=1)
        reloj_horas.place(x= 20, y= 680, anchor=NW)
        reloj_minutos = Label(jugar_ventana, text="Minutos", font=("Arial", 10), borderwidth=1)
        reloj_minutos.place(x= 70, y= 680, anchor=NW)
        reloj_segundos = Label(jugar_ventana, text="Segundos", font=("Arial", 10), borderwidth=1)
        reloj_segundos.place(x= 130, y= 680, anchor=NW)
        
        reloj_horas_valor = Entry(jugar_ventana, width=7, font=("Arial", 10), borderwidth=1, justify=CENTER)
        reloj_horas_valor.place(x= 20, y= 700, anchor=NW)
        reloj_minutos_valor = Entry(jugar_ventana, width=8, font=("Arial", 10), borderwidth=1, justify=CENTER)
        reloj_minutos_valor.place(x= 70, y= 700, anchor=NW)
        reloj_segundos_valor = Entry(jugar_ventana, width=8, font=("Arial", 10), borderwidth=1, justify=CENTER)
        reloj_segundos_valor.place(x= 130, y= 700, anchor=NW)
        if configuracion["RELOJ"] == 1:
            reloj_horas_valor.configure(state=DISABLED)
            reloj_minutos_valor.configure(state=DISABLED)
            reloj_segundos_valor.configure(state=DISABLED)
    
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
    niveles = ["FACIL", "MEDIO", "DIFICIL", "EXPERTO"]
    nivel_label = Label(jugar_ventana, text="Nivel: " + niveles[configuracion["NIVEL"]-1], font=("Arial", 10), borderwidth=1, fg="white", bg="#1C1C1C")
    nivel_label.place(x= 20, y= 740, anchor=NW)
    partidas = partidas[niveles[configuracion["NIVEL"]-1]]
    def seleccionar_partida(partidas):
        if len(partidas) == 0:
            MessageBox.showinfo("Error", "NO HAY PARTIDAS PARA ESTE NIVEL")
            jugar_ventana.destroy()
            return [], partidas
        partida_actual = random.choice(partidas)
        partidas = list(partidas)
        partidas.remove(partida_actual)
        partidas = tuple(partidas)
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
        boton_terminar.config(command=lambda: terminar_juego(matriz, game_state, partidas))
        return partida_actual, partidas
    partida_actual, partidas = seleccionar_partida(partidas)
    boton_borrar_juego.config(command=lambda: reiniciar_tablero(partida_actual, matriz, game_state))
    boton_terminar.config(command=lambda: terminar_juego(matriz, game_state, partidas))
    # Función para rellenar el tablero actual
    def reiniciar_tablero(partida_actual, matriz, game_state):
        if game_state:
            if MessageBox.askquestion("Reiniciar", "¿Está seguro que desea reiniciar el tablero?", icon='warning') == "yes":
                game_state = False
                rellenar_tablero(partida_actual, matriz)
            else:
                return
        else:
            MessageBox.showerror("Error", "NO SE HA INICIADO EL JUEGO")
    # Función para terminar el juego actual
    def terminar_juego(matriz, game_state, partidas):
        if game_state:
            if MessageBox.askquestion("Terminar", "¿Está seguro que desea terminar el juego?", icon='warning') == "yes":
                game_state = False
                global partida_actual
                partida_actual, partidas = seleccionar_partida(partidas)
                rellenar_tablero(partida_actual, matriz)
            else:
                return
        else:
            MessageBox.showerror("Error", "NO SE HA INICIADO EL JUEGO")
    # Rellenar el tablero con los valores de la partida
    def rellenar_tablero(partida_actual, matriz):
        for i in matriz:
            for k in i:
                matriz[matriz.index(i)][i.index(k)].configure(text="")
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
        
    rellenar_tablero(partida_actual, matriz)
    

        
    return