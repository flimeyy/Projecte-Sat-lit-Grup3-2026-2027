import tkinter as tk
from tkinter import messagebox
import serial, threading
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib.lines import Line2D

device = "COM3"
mySerial = serial.Serial(device, 19200)
media_tierra=1
trozos=[]
linea=-1

def lectura():
    threadRecepcion = threading.Thread (target = leer_linea)
    threadRecepcion.start() 

def leer_linea():
    while True:
        if mySerial.in_waiting > 0:
            linea = mySerial.readline().decode('utf-8').rstrip()
            print(linea)
            global trozos
            trozos = linea.split(":")

def recepcion():
    temperaturas = []
    ultimas_temps = []
    humedades=[]
    medias=[]
    cont_medias=0 #cuenta las medias que superen el limite
    limite=limite_slider.get()
    eje_x=[]
    i=0

    fig = Figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    ax.set_ylim(0, 100)
    linea_temp, = ax.plot([], [], label="Temperatura")
    linea_hum, = ax.plot([], [], label="Humedad")
    linea_media,= ax.plot([], [], label="Media de temperatura")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=grafica_frame)
    
    grafica_canvas = canvas.get_tk_widget()
    grafica_canvas.config(width=350, height=350)
    grafica_canvas.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

    while True:
        if  mySerial.in_waiting > 0:  
            if trozos[0] == "1":
                eje_x.append(i)
                temperatura=float(trozos[2])
                humedad = float(trozos[1])
                if media_tierra == 1:
                    ultimas_temps.append(temperatura)
                    if len(temperaturas) > 10:
                        del ultimas_temps[0]
                    media=(sum(ultimas_temps))/len(ultimas_temps)
                    if media>float(limite):
                        cont_medias+=1
                    else:
                        cont_medias=0        
                    if cont_medias==3:
                        mensaje="3"
                        mySerial.write(mensaje.encode('utf-8'))
                else:
                    media = trozos[3]
                    print(media)
                temperaturas.append(temperatura)
                humedades.append(humedad)
                medias.append(media)
                if len(temperaturas) >= 100: #PARA DEPURAR CAMBIAR
                    del(temperaturas[0])
                    del(humedades[0])
                    del(medias[0])
                    del(eje_x[len(eje_x)-1])

                linea_temp.set_data(eje_x, temperaturas)
                linea_hum.set_data(eje_x, humedades)
                linea_media.set_data(eje_x, medias)
                ax.set_title("Iteracion nº{}".format(i))
                ax.relim()
                ax.autoscale_view()
                canvas.draw_idle()

                i+=1

            elif trozos[0]== "3":
                if trozos[1] == "1":
                    messagebox.showerror(title="Alerta", message="¡El sensor del satélite no funciona!")
                elif trozos[1] == "0":
                    messagebox.showwarning(title="Alerta", message="¡No se recibe información del satélite!")
                elif trozos[1] == "2":
                    messagebox.showwarning(title="Alerta", message="Se ha superado el límite de temperatura introducido")

def iniciar():
    mensaje = "1:1"
    mySerial.write(mensaje.encode('utf-8'))
    print("Funciona")
    threadRecepcion = threading.Thread (target = recepcion)
    threadRecepcion.start()

def pausar():
    mensaje = "1:0"
    mySerial.write(mensaje.encode('utf-8'))
    print("Funciona")

def reanudar():
    mensaje = "1:1"
    mySerial.write(mensaje.encode('utf-8'))
    print("Funciona")

def modificar_periodo():
    mensaje = "5:"
    mySerial.write((mensaje + periodo_entry.get()).encode('utf-8'))
    print("Funciona")

def mediasat(): #*
    limite=str(limite_slider.get())
    mensaje = "2:1:"

    mySerial.write(str((mensaje + limite)).encode('utf-8'))
    print(mensaje + limite)
    media_tierra = 0

def mediatierra(): #*
    mensaje = "2:0"
    mySerial.write(mensaje.encode('utf-8'))
    media_tierra=1
    limite=str(limite_slider.get())

def mandar_angulo():
    mensaje = insertar_grado.get()
    try:
        if (int(mensaje) <= 180 and int(mensaje) >= 0):
            mySerial.write(("4:{}:0".format(mensaje)).encode("utf-8"))
            print("4:{}".format(mensaje))
        else:
            raise ValueError
    except ValueError:
        messagebox.showerror(title="Alerta", message="¡El valor introducido no es un entero entre 0 y 180!")

def reiniciar_rotacion():
    mySerial.write("4:-1:0".encode("utf-8"))

def iniciar_hilo_grafico():
    hilo = threading.Thread(target=plot_angulos, daemon=True)
    hilo.start()

def plot_angulos():
    angle1 = []
    value1 = []
    value2 = []
    
    while True:
        if mySerial.in_waiting > 0: # Hay que cambiarlo URGENTEMENTE
            if trozos[0] == "4":
                ang = int(trozos[3]) * np.pi / 180
                angle1.append(ang)
                value1.append(float(trozos[1]))
                value2.append(float(trozos[2]))
                
                # Aumentamos el historial a 8 para que el barrido de área se aprecie mejor
                if len(angle1) > 8:
                    del(angle1[0])
                    del(value1[0])
                    del(value2[0])
                
                ax.clear()
                
                max_val = max(max(value1, default=1), max(value2, default=1)) * 1.2
                
                # --- LÓGICA DE BARRIDO DE ÁREA (RELLENO ENTRE PASOS) ---
                for i in range(len(angle1)):
                    a1 = angle1[i]
                    v1 = value1[i]
                    v2 = value2[i]
                    
                    # Calcular extremos de la línea actual
                    x1_curr = v1 * np.cos(a1)
                    y1_curr = v1 * np.sin(a1)
                    x2_curr = v2 * np.cos(a1 + np.pi)
                    y2_curr = v2 * np.sin(a1 + np.pi)
                    
                    # Opacidad progresiva (desvanecimiento del rastro)
                    alpha_val = (i + 1) / len(angle1)
                    
                    # Si hay un punto anterior en el historial, rellenamos el área (barrido)
                    if i > 0:
                        a1_prev = angle1[i-1]
                        v1_prev = value1[i-1]
                        v2_prev = value2[i-1]
                        
                        # Calcular extremos de la línea anterior
                        x1_prev = v1_prev * np.cos(a1_prev)
                        y1_prev = v1_prev * np.sin(a1_prev)
                        x2_prev = v2_prev * np.cos(a1_prev + np.pi)
                        y2_prev = v2_prev * np.sin(a1_prev + np.pi)
                        
                        # Creamos el polígono de barrido uniendo ordenadamente los 4 vértices
                        # Lado Sensor 1: x1_prev -> x1_curr  |  Lado Sensor 2: x2_curr -> x2_prev
                        x_polygon = [x1_prev, x1_curr, x2_curr, x2_prev]
                        y_polygon = [y1_prev, y1_curr, y2_curr, y2_prev]
                        
                        # Rellenamos el sector con un tono verde/azul de radar electrónico
                        ax.fill(x_polygon, y_polygon, color='#17becf', alpha=alpha_val * 0.35)
                    
                    # Dibujamos el borde delantero (la lectura actual brillante)
                    if i == len(angle1) - 1:
                        # La línea más nueva (el haz principal del radar) resalta en color sólido
                        ax.plot([x1_curr, x2_curr], [y1_curr, y2_curr], color='#00ffcc', linewidth=2.5)
                    else:
                        # Líneas intermedias más tenues para estructurar el rastro
                        ax.plot([x1_curr, x2_curr], [y1_curr, y2_curr], color='gray', linewidth=1, alpha=alpha_val * 0.5)
                        
                    # Marcadores en los extremos de cada lectura
                    ax.plot(x1_curr, y1_curr, marker='o', color='blue', markersize=6, alpha=alpha_val)   
                    ax.plot(x2_curr, y2_curr, marker='s', color='orange', markersize=5, alpha=alpha_val) 
                
                # --- ESTÉTICA DE RADAR ---
                ax.set_xlim(-max_val, max_val)
                ax.set_ylim(-max_val, max_val)
                ax.set_aspect('equal')
                
                for r in np.linspace(max_val/4, max_val, 4):
                    circle = plt.Circle((0, 0), r, color='gray', fill=False, linestyle='--', alpha=0.25)
                    ax.add_patch(circle)
                
                angulos_guia = [0, 45, 90, 135, 180, 225, 270, 315]
                distancia_etiqueta = max_val * 1.08  
                
                for ang_deg in angulos_guia:
                    ang_rad = ang_deg * np.pi / 180
                    ax.plot([0, max_val * np.cos(ang_rad)], [0, max_val * np.sin(ang_rad)], 
                            color='gray', linestyle=':', alpha=0.25)
                    ax.text(distancia_etiqueta * np.cos(ang_rad), distancia_etiqueta * np.sin(ang_rad), f"{ang_deg}°", ha='center', va='center', fontsize=9, color='darkgray')
                
                leyenda_elementos = [
                    Line2D([0], [0], marker='o', color='w', label='Sensor 1', markerfacecolor='blue', markersize=6),
                    Line2D([0], [0], marker='s', color='w', label='Sensor 2', markerfacecolor='orange', markersize=5),
                    Line2D([0], [0], color='#17becf', lw=4, alpha=0.5, label='Área barrida')
                ]
                ax.legend(handles=leyenda_elementos, loc='upper right', frameon=True)
                
                ax.axis('off')
                canvas.draw()



#Definiciones interfaz gráfica
window = tk.Tk()
window.geometry("1200x600")
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=4)
window.columnconfigure(3, weight=4)


#Cuadro de los botones
controles_frame = tk.LabelFrame(window, text='Controles')
controles_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

controles_frame.rowconfigure(index=0, weight=1)
controles_frame.rowconfigure(index=1, weight=1)
controles_frame.rowconfigure(index=2, weight=1)
controles_frame.rowconfigure(index=3, weight=1)
controles_frame.rowconfigure(index=4, weight=1)
controles_frame.rowconfigure(index=5, weight=1)
controles_frame.columnconfigure(index=0, weight=1)


boton_iniciar = tk.Button(controles_frame, text="Iniciar", font=("Comic Sans MS", 20), bg="chartreuse4", command=iniciar)
boton_iniciar.grid(row=0,column=0,padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
 
boton_pausar = tk.Button(controles_frame, text="Pausar", font=("Comic Sans MS", 20), bg="DarkRed", command=pausar)
boton_pausar.grid(row=1,column=0,padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

boton_reanudar = tk.Button(controles_frame, text="Reanudar", font=("Comic Sans MS", 20), bg="DarkOrchid", command=reanudar)
boton_reanudar.grid(row=2,column=0,padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

periodo_entry=tk.Entry(controles_frame, font=("Comic Sans MS", 10))
periodo_entry.grid(row=4, column=0, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

boton_periodo = tk.Button(controles_frame, text="Modificar periodo", font=("Comic Sans MS", 20), bg="DarkOrchid", command=modificar_periodo)
boton_periodo.grid(row=5,column=0,padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

#Cuadro de la gráfica
grafica_frame = tk.LabelFrame(window, text='Temperatura y humedad')
grafica_frame.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W) #*

grafica_frame.rowconfigure(index=0, weight=1)
grafica_frame.columnconfigure(index=0, weight=1)

grafica_canvas = tk.Canvas(grafica_frame, width=200, height=200, bg="white")

#Cuadro de la media
media_frame = tk.LabelFrame(window, text='Cálculo de la media de temperatura')
media_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

media_frame.rowconfigure(index=0, weight=1)
media_frame.columnconfigure(index=0, weight=1)
media_frame.columnconfigure(index=1, weight=1)

boton_mediasat = tk.Button(media_frame, text="Calcular desde\nel satélite", font=("Comic Sans MS", 10), bg="LightSkyBlue2", command=mediasat)
boton_mediasat.grid(row=0,column=0,padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
 
boton_mediatierra = tk.Button(media_frame, text="Cálcular desde\ntierra", font=("Comic Sans MS", 10), bg="dark sea green", command=mediatierra)
boton_mediatierra.grid(row=0,column=1,padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

#Cuadro del limite
limite_frame = tk.LabelFrame(window, text='Temperatura limite (en ºC)')
limite_frame.grid(row=1, column=1, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

limite_frame.rowconfigure(index=0, weight=1)
limite_frame.columnconfigure(index=0, weight=1)

limite_slider=tk.Scale(limite_frame, from_=0, to=100, length=450, orient="horizontal", tickinterval=25, font=("Comic Sans MS", 6))
limite_slider.set(50)
limite_slider.grid(row=0, column=0)

#Cuadro de la radio
controles_radio_frame = tk.LabelFrame(window, text="Controles sensor de distancia")
controles_radio_frame.grid(row=1, column=2, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
controles_radio_frame.rowconfigure(index=0, weight=1)
controles_radio_frame.rowconfigure(index=1, weight=1)
controles_radio_frame.columnconfigure(index=0, weight=1)
controles_radio_frame.columnconfigure(index=1, weight=1)

boton_mandar = tk.Button(controles_radio_frame, text="Establecer posicion", command=mandar_angulo)
boton_mandar.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

insertar_grado = tk.Entry(controles_radio_frame)
insertar_grado.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

empezar = tk.Button(controles_radio_frame, text="Graficar", command=iniciar_hilo_grafico)
empezar.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

boton_reiniciar = tk.Button(controles_radio_frame, text="Reiniciar rotación", command=reiniciar_rotacion)
boton_reiniciar.grid(row=1, column=1, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

radio_frame = tk.LabelFrame(window, text="Sensor de distancia")
radio_frame.grid(row=0, column=2, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)


fig = Figure(figsize=(5, 5), dpi=100)
ax = fig.add_subplot(111)
ax.axis('off') 

canvas = FigureCanvasTkAgg(fig, master=radio_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

window.after_idle(lectura)
window.mainloop()

quit()
