olumna 1, fila 0
    logo = ImageTk.PhotoImage(Image.open("assets/title_logo.png").resize((180, 48), Image.LANCZOS))
    logo_label = Label(ventana, image=logo)
    logo_label.image = logo 
    logo_label.place(x= 160, y= 50)
    
    # Pide el nombre del jugador
    nombre_label = Label(ventana, text="Nombre del jugador:", font=("Arial", 8))
    nombre_label.place(relx= 0.5, y= 120, anchor=N)
    nombre_entry = Entry(ventana, font=("Arial", 8))
    nombre_entry.place(relx= 0.5, y= 135, anchor=N)
    
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
    
# Inicia la ventana principal
root = Tk()
main(root)
sv_ttk.set_theme("dark")
root.mainloop()