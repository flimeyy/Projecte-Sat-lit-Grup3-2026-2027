import tkinter as tk
from tkinter import messagebox
import serial,threading
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

device = "COM3"
mySerial = serial.Serial(device, 9600)

def recepcion():
    temperaturas = []
    humedades=[]
    eje_x=[]
    i=0
    fig = Figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    linea_temp, = ax.plot([], [], label="Temperatura")
    linea_hum, = ax.plot([], [], label="Humedad")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=grafica_frame)
    
    grafica_canvas = canvas.get_tk_widget()
    grafica_canvas.config(width=400, height=400)
    grafica_canvas.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

    while True:
        if mySerial.in_waiting > 0:
            linea = mySerial.readline().decode('utf-8').rstrip()
            print(linea)
            trozos = linea.split(":")
            if trozos[0] == "H":
                eje_x.append(i)
                temperatura=float(trozos[3])
                humedad = float(trozos[1])
                
                temperaturas.append(temperatura)
                humedades.append(humedad)

                linea_temp.set_data(eje_x, temperaturas)
                linea_hum.set_data(eje_x, humedades)
                ax.set_title("Iteracion nº{}".format(i))
                ax.relim()
                ax.autoscale_view()
                canvas.draw_idle()

                i+=1
            else:
                if linea == "Fallo":
                    messagebox.showerror(title="Alerta", message="¡El sensor del satélite no funciona!")
                elif linea == "nullerror":
                    messagebox.showwarning(title="Alerta", message="¡No se recibe información del satélite!")

def iniciar():
    mensaje = "saton"
    mySerial.write(mensaje.encode('utf-8'))
    #print("Funciona")
    threadRecepcion = threading.Thread (target = recepcion)
    threadRecepcion.start()

def pausar():
    mensaje = "satoff"
    mySerial.write(mensaje.encode('utf-8'))
    #print("Funciona")

def reanudar():
    mensaje = "saton"
    mySerial.write(mensaje.encode('utf-8'))
    #print("Funciona")

#Definiciones interfaz gráfica
window = tk.Tk()
window.geometry("800x400")
window.rowconfigure(0, weight=1)

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=9)

#Cuadro de los botones
controles_frame = tk.LabelFrame(window, text='Controles')
controles_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

controles_frame.rowconfigure(index=0, weight=1)
controles_frame.rowconfigure(index=1, weight=1)
controles_frame.rowconfigure(index=2, weight=1)
controles_frame.columnconfigure(index=0, weight=1)


boton_iniciar = tk.Button(controles_frame, text="Iniciar", font=("Comic Sans MS", 20), bg="chartreuse4", command=iniciar)
boton_iniciar.grid(row=0,column=0,padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
 
boton_pausar = tk.Button(controles_frame, text="Pausar", font=("Comic Sans MS", 20), bg="DarkRed", command=pausar)
boton_pausar.grid(row=1,column=0,padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

boton_reanudar = tk.Button(controles_frame, text="Reanudar", font=("Comic Sans MS", 20), bg="DarkOrchid", command=reanudar)
boton_reanudar.grid(row=2,column=0,padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

#Cuadro de la gráfica
grafica_frame = tk.LabelFrame(window, text='Temperatura y humedad')
grafica_frame.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

grafica_frame.rowconfigure(index=0, weight=1)
grafica_frame.columnconfigure(index=0, weight=1)

grafica_canvas = tk.Canvas(grafica_frame, width=400, height=400, bg="white")


window.mainloop()