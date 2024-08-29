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
        (slot presupuesto)
        (slot clima))
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
    clima = entrada_clima.get()

    # Definir hechos en CLIPS basados en la entrada del usuario
    env.assert_string(f"(cliente (preferencia {preferencia}) (presupuesto {presupuesto}) (clima {clima}))")

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
       (cliente (preferencia ?tipo) (presupuesto ?costo) (clima ?clima))
       (destino (nombre ?nombre) (tipo ?tipo) (costo ?costo) (clima ?clima))
       =>
       (capturar_salida (str-cat "Recomendamos el destino: " ?nombre "\n")))
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
root.geometry("400x200")
root.configure(bg="#f0f0f0")

# Configuración de estilo
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")
style.configure("TButton", font=("Arial", 12), background="#d3d3d3")
style.configure("TCombobox", font=("Arial", 12))

# Etiquetas y campos de entrada con Combobox
tk.Label(root, text="Preferencia:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entrada_preferencia = ttk.Combobox(root, values=["cultural", "aventura", "relajacion", "lujo"])
entrada_preferencia.grid(row=0, column=1, padx=10, pady=10, sticky="w")

tk.Label(root, text="Presupuesto:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entrada_presupuesto = ttk.Combobox(root, values=["alto", "medio", "bajo"])
entrada_presupuesto.grid(row=1, column=1, padx=10, pady=10, sticky="w")

tk.Label(root, text="Clima preferido:", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10, sticky="e")
entrada_clima = ttk.Combobox(root, values=["templado", "tropical", "frio", "calido"])
entrada_clima.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Botón para obtener la recomendación
obtener_button = ttk.Button(root, text="Obtener Recomendación", command=obtener_recomendacion)
obtener_button.grid(row=3, columnspan=2, pady=20)

# Ejecutar la aplicación
root.mainloop()
