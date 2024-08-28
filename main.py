import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import clips

# Función para capturar la salida de CLIPS
def capturar_salida(texto, *args):
    global resultado
    resultado += texto

# Función para ejecutar el motor de inferencia y obtener la recomendación
def obtener_recomendacion():
    global resultado
    resultado = ""

    # Crear un entorno CLIPS
    env = clips.Environment()

    # Redirigir la salida de CLIPS a la función capturar_salida
    env.define_function(capturar_salida)

    # Definir el hecho 'cliente' con sus atributos
    env.build("""
    (deftemplate cliente
        (slot preferencia)
        (slot presupuesto))
    """)

    # Definir el hecho 'destino' con sus atributos
    env.build("""
    (deftemplate destino
        (slot nombre (type SYMBOL))
        (slot tipo (type SYMBOL))
        (slot clima (type SYMBOL))
        (slot costo (type SYMBOL)))
    """)

    # Obtener las entradas del usuario desde los comboboxes
    preferencia = entrada_preferencia.get()
    presupuesto = entrada_presupuesto.get()

    # Definir hechos en CLIPS basados en la entrada del usuario
    env.assert_string(f"(cliente (preferencia {preferencia}) (presupuesto {presupuesto}))")

    # Definir destinos
    destinos = [
        "(destino (nombre Paris) (tipo cultural) (clima templado) (costo alto))",
        "(destino (nombre Bangkok) (tipo aventura) (clima tropical) (costo medio))",
        "(destino (nombre Reykjavik) (tipo relajacion) (clima frio) (costo alto))",
        "(destino (nombre NuevaYork) (tipo cultural) (clima templado) (costo alto))",
        "(destino (nombre MachuPicchu) (tipo aventura) (clima templado) (costo medio))",
        "(destino (nombre Maldivas) (tipo relajacion) (clima tropical) (costo alto))",
        "(destino (nombre Tailandia) (tipo aventura) (clima tropical) (costo bajo))",
        "(destino (nombre Tokio) (tipo cultural) (clima templado) (costo alto))",
        "(destino (nombre Sydney) (tipo aventura) (clima templado) (costo alto))",
        "(destino (nombre Cairo) (tipo cultural) (clima calido) (costo bajo))",
        "(destino (nombre Hawaii) (tipo relajacion) (clima tropical) (costo medio))",
        "(destino (nombre Amsterdam) (tipo cultural) (clima templado) (costo medio))",
        "(destino (nombre CapeTown) (tipo aventura) (clima templado) (costo medio))",
        "(destino (nombre Dubai) (tipo lujo) (clima calido) (costo alto))",
        "(destino (nombre BuenosAires) (tipo cultural) (clima templado) (costo bajo))",
        "(destino (nombre Bali) (tipo relajacion) (clima tropical) (costo bajo))",
        "(destino (nombre AlpesSuizos) (tipo aventura) (clima frio) (costo alto))",
        "(destino (nombre Miami) (tipo relajacion) (clima calido) (costo medio))",
        "(destino (nombre SanFrancisco) (tipo cultural) (clima templado) (costo alto))",
        "(destino (nombre Barcelona) (tipo cultural) (clima templado) (costo medio))",
        "(destino (nombre Lisboa) (tipo cultural) (clima templado) (costo bajo))",
        "(destino (nombre Nairobi) (tipo aventura) (clima templado) (costo bajo))",
        "(destino (nombre Santorini) (tipo relajacion) (clima templado) (costo alto))",
        "(destino (nombre Atenas) (tipo cultural) (clima templado) (costo medio))",
        "(destino (nombre Vancouver) (tipo aventura) (clima templado) (costo alto))",
        "(destino (nombre Praga) (tipo cultural) (clima templado) (costo bajo))",
        "(destino (nombre Fiyi) (tipo relajacion) (clima tropical) (costo medio))",
        "(destino (nombre Londres) (tipo cultural) (clima templado) (costo alto))"
    ]

    for destino in destinos:
        env.assert_string(destino)

    # Definir reglas para recomendación
    env.build("""
    (defrule recomendar-destino
       (cliente (preferencia ?tipo) (presupuesto ?costo))
       (destino (nombre ?nombre) (tipo ?tipo) (costo ?costo))
       =>
       (capturar_salida (str-cat "Recomendamos el destino: " ?nombre "\n")))
    """)

    # Regla de fallback
    env.build("""
    (defrule recomendar-default
       (cliente (preferencia ?tipo) (presupuesto ?costo))
       =>
       (capturar_salida "No se encontró un destino exacto, pero recomendamos explorar otras opciones interesantes.\n"))
    """)

    # Ejecutar el motor de inferencia
    env.run()

    # Mostrar la recomendación
    if resultado:
        messagebox.showinfo("Recomendación", resultado)
    else:
        messagebox.showinfo("Recomendación", "No se encontró ningún destino adecuado.")

# Crear la ventana principal
root = tk.Tk()
root.title("Destinos Perfectos - Sistema Experto")

# Etiquetas y campos de entrada con Combobox
tk.Label(root, text="Preferencia:").grid(row=0)
entrada_preferencia = ttk.Combobox(root, values=["cultural", "aventura", "relajacion", "lujo"])
entrada_preferencia.grid(row=0, column=1)

tk.Label(root, text="Presupuesto:").grid(row=1)
entrada_presupuesto = ttk.Combobox(root, values=["alto", "medio", "bajo"])
entrada_presupuesto.grid(row=1, column=1)

# Botón para obtener la recomendación
tk.Button(root, text="Obtener Recomendación", command=obtener_recomendacion).grid(row=2, columnspan=2)

# Ejecutar la aplicación
root.mainloop()
