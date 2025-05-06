import tkinter as tk
import random
import math
import matplotlib.pyplot as plt


def generaruniforme(limInf, limSup, cantidad):
    lista = [round(random.random() * (limSup - limInf) + limInf, 4) for _ in range(cantidad)]
    graficar(lista)
    return lista

def generar_normal(media, desviacion, cantidad):
    lista = []
    i = 0
    while i < cantidad:
        U1 = random.random()
        U2 = random.random()
        Z0 = math.sqrt(-2 * math.log(U1)) * math.cos(2 * math.pi * U2)
        Z1 = math.sqrt(-2 * math.log(U1)) * math.sin(2 * math.pi * U2)
        lista.append(round(Z0 * desviacion + media, 4))
        i += 1
        if i < cantidad:
            lista.append(round(Z1 * desviacion + media, 4))
            i += 1
    graficar(lista)
    return lista

def generarexponencial(media, cantidad):
    lista = [round(-media * math.log(1 - random.random()), 4) for _ in range(cantidad)]
    graficar(lista)
    return lista

def graficar(datos):
    intervalos = int(selected_interval.get())
    plt.figure(figsize=(10, 5))
    plt.hist(datos, bins=intervalos, edgecolor='black')
    plt.title('Histograma de Números Generados')
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.grid(True)
    plt.show()

def generar_numeros():
    numero = int(entryCantidad.get())

    opcion = selected_option.get()
    if opcion == "Uniforme":
        desde = float(entryDesde.get())
        hasta = float(entryHasta.get())
        generaruniforme(desde, hasta, numero)
    elif opcion == "Exponencial":
        media = float(entryMediaExponencial.get())
        generarexponencial(media, numero)
    elif opcion == "Normal":
        media = float(entryMedia.get())
        desv = float(entryDesv.get())
        generar_normal(media, desv, numero )
    else:
        print("Opción no válida")

def actualizar_campos(*args):
    for widget in frame_dinamico.winfo_children():
        widget.destroy()

    opcion = selected_option.get()
    if opcion == "Uniforme":
        tk.Label(frame_dinamico, text="Intervalo desde:").pack()
        global entryDesde
        entryDesde = tk.Entry(frame_dinamico)
        entryDesde.pack()

        tk.Label(frame_dinamico, text="Intervalo hasta:").pack()
        global entryHasta
        entryHasta = tk.Entry(frame_dinamico)
        entryHasta.pack()
    elif opcion == "Exponencial":
        tk.Label(frame_dinamico, text="Media:").pack()
        global entryMediaExponencial
        entryMediaExponencial = tk.Entry(frame_dinamico)
        entryMediaExponencial.pack()
    elif opcion == "Normal":
        tk.Label(frame_dinamico, text="Media:").pack()
        global entryMedia
        entryMedia = tk.Entry(frame_dinamico)
        entryMedia.pack()
        tk.Label(frame_dinamico, text="Desv:").pack()
        global entryDesv
        entryDesv = tk.Entry(frame_dinamico)
        entryDesv.pack()

    tk.Label(frame_dinamico, text="Cantidad de números a generar:").pack()
    global entryCantidad
    entryCantidad = tk.Entry(frame_dinamico)
    entryCantidad.pack()

    tk.Label(frame_dinamico, text="Cantidad de intervalos (bins):").pack()
    global selected_interval
    selected_interval = tk.StringVar(value="10")
    interval_options = ["10", "15", "20", "25"]
    interval_dropdown = tk.OptionMenu(frame_dinamico, selected_interval, *interval_options)
    interval_dropdown.pack()

    tk.Button(frame_dinamico, text="Generar", command=generar_numeros).pack()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Generador de Números")

tk.Label(root, text="Selecciona una distribución:").pack()
options = ["Uniforme", "Exponencial", "Normal"]
selected_option = tk.StringVar(value=options[0])
dropdown = tk.OptionMenu(root, selected_option, *options)
dropdown.pack()

frame_dinamico = tk.Frame(root)
frame_dinamico.pack()

selected_option.trace("w", actualizar_campos)
actualizar_campos()

root.mainloop()
