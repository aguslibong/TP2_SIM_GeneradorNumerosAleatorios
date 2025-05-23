import tkinter as tk
import random
import math
import matplotlib.pyplot as plt
from scipy.stats import chi2, norm, expon

def crear_grupos_intervalos(minimo, maximo, intervalos):
    grupos_intervalos = []
    amplitud_intervalo = (maximo - minimo) / intervalos
    for i in range(intervalos):
        inicio = minimo + i * amplitud_intervalo
        fin = inicio + amplitud_intervalo
        grupos_intervalos.append((inicio, fin))
    return grupos_intervalos

def contar_numeros_en_cada_intervalo(lista, grupos_intervalos, intervalos):
    contador = [0] * intervalos
    for numero in lista:
        for i, (inicio, fin) in enumerate(grupos_intervalos):
            if inicio <= numero <= fin:
                contador[i] += 1
                break
    return contador

def frecuencia_esperada_normal(grupos_intervalos, total_datos, media, desviacion):
    frecuencias = []
    for inicio, fin in grupos_intervalos:
        prob_inicio = norm.cdf(inicio, loc=media, scale=desviacion)
        prob_fin = norm.cdf(fin, loc=media, scale=desviacion)
        frecuencia = total_datos * (prob_fin - prob_inicio)
        frecuencias.append(frecuencia)
    return frecuencias

def frecuencia_esperada_exponencial(grupos_intervalos, total_datos, lambd):
    frecuencias = []
    for inicio, fin in grupos_intervalos:
        prob_inicio = expon.cdf(inicio, scale=1/lambd)
        prob_fin = expon.cdf(fin, scale=1/lambd)
        frecuencia = total_datos * (prob_fin - prob_inicio)
        frecuencias.append(frecuencia)
    return frecuencias

def obtener_chi_calculado(frecuencia_observada, frecuencia_esperada):
    chi_calculada = 0
    for fo, fe in zip(frecuencia_observada, frecuencia_esperada):
        if fe > 0:
            chi_calculada += ((fo - fe) ** 2) / fe
    return chi_calculada

def generaruniforme(limInf, limSup, cantidad):
    intervalos = int(selected_interval.get())
    lista = [round(random.random() * (limSup - limInf) + limInf, 4) for _ in range(cantidad)]
    lista.sort()
    maximo = lista[-1]
    minimo = lista[0]

    grupos_intervalos = crear_grupos_intervalos(minimo, maximo, intervalos)
    frecuencias_observadas = contar_numeros_en_cada_intervalo(lista, grupos_intervalos, intervalos)
    
    print("Intervalos:")
    for i, (inicio, fin) in enumerate(grupos_intervalos):
        print(f"Intervalo {i+1}: {inicio:.4f} - {fin:.4f}, Frecuencia observada: {frecuencias_observadas[i]}")

    frecuencia_esperada = cantidad / intervalos
    chi_calculado = obtener_chi_calculado(frecuencias_observadas, [frecuencia_esperada] * intervalos)
    
    alfa = 0.05
    grados_de_libertad = intervalos - 1
    chi_critico = chi2.ppf(1 - alfa, grados_de_libertad)

    resultado = "Se acepta la hipótesis nula es uniforme" if chi_calculado < chi_critico else "Se rechaza la hipótesis nula no es uniforme"
    graficar(lista, chi_calculado, chi_critico, resultado)
    return lista

def generar_normal(media, desviacion, cantidad):
    lista = []
    intervalos = int(selected_interval.get())
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

    lista.sort()
    maximo = lista[-1]
    minimo = lista[0]

    alfa = 0.05
    grados_libertad = intervalos - 3
    grupos_intervalos = crear_grupos_intervalos(minimo, maximo, intervalos)
    frecuencias_observadas = contar_numeros_en_cada_intervalo(lista, grupos_intervalos, intervalos)

    print("Intervalos:")
    for i, (inicio, fin) in enumerate(grupos_intervalos):
        print(f"Intervalo {i+1}: {inicio:.4f} - {fin:.4f}, Frecuencia observada: {frecuencias_observadas[i]}")

    frecuencias_esperada = frecuencia_esperada_normal(grupos_intervalos, cantidad, media, desviacion)
    chi_calculado = obtener_chi_calculado(frecuencias_observadas, frecuencias_esperada)
    chi_critico = chi2.ppf(1 - alfa, grados_libertad)

    resultado = "Se acepta la hipótesis nula" if chi_calculado < chi_critico else "Se rechaza la hipótesis nula"
    graficar(lista, chi_calculado, chi_critico, resultado)
    return lista

def generarexponencial(media, cantidad):
    lambd = 1 / media
    lista = [round(-media * math.log(1 - random.random()), 4) for _ in range(cantidad)]
    lista.sort()
    intervalos = int(selected_interval.get())

    alfa = 0.05
    grados_libertad = intervalos - 2
    maximo = lista[-1]
    minimo = lista[0]

    grupos_intervalos = crear_grupos_intervalos(minimo, maximo, intervalos)
    frecuencias_observadas = contar_numeros_en_cada_intervalo(lista, grupos_intervalos, intervalos)

    print("Intervalos:")
    for i, (inicio, fin) in enumerate(grupos_intervalos):
        print(f"Intervalo {i+1}: {inicio:.4f} - {fin:.4f}, Frecuencia observada: {frecuencias_observadas[i]}")

    frecuencias_esperada = frecuencia_esperada_exponencial(grupos_intervalos, cantidad, lambd)
    chi_calculado = obtener_chi_calculado(frecuencias_observadas, frecuencias_esperada)
    chi_critico = chi2.ppf(1 - alfa, grados_libertad)

    resultado = "Se acepta la hipótesis nula es exponencial" if chi_calculado < chi_critico else "Se rechaza la hipótesis nula es exponencial"
    graficar(lista, chi_calculado, chi_critico, resultado)
    return lista

def graficar(datos, chi_calculado, chi_critico, resultado):
    intervalos = int(selected_interval.get())
    plt.figure(figsize=(10, 5))
    plt.hist(datos, bins=intervalos, edgecolor='black')
    plt.title('Histograma de Números Generados')
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.grid(True)
    texto_chi = f"Chi calculado = {chi_calculado:.3f}\nChi crítico = {chi_critico:.3f}\n{resultado}"
    plt.figtext(0.75, 0.7, texto_chi, bbox={"facecolor": "white", "alpha": 0.5, "pad": 10})
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
        generar_normal(media, desv, numero)
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

# Interfaz gráfica
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
