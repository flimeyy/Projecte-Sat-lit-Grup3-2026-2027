# Proyecto Ingeniería de Satélites: Grupo 3 (EETAC)
### Descripción breve del circuito y código:
En este proyecto se usan dos placas arduino para simular la comuncicación de antena a satélite. El satélite envia datos sobre la humedad y temperatura hacia la tierra, donde se procesarán e insertarán en una gráfica dentro de una interfaz gráfica de Python.
El programa de Python, además de mostrar los datos recibidos, permite mandar comandos hacia el satélite para empezar, pausar y reanudar la recepción de datos.

En el caso de que el satélite no pueda recibir datos de temperatura y humedad a través del sensor DHT, la placa Tierra recibirá un mensaje del satélite donde se explica que no se reciben los datos del sensor.
Por otra parte, si la tierra dejara de recibir datos del satélite al pasar 5 segundos, también se recibiría un mensaje de alerta diferente. En ambos casos, se encendería el LED rojo, que indica que hay un error.

Otros elementos del circuito incluyen el LED verde del satélite (que indica que se están transmitiendo datos) y el LED azul de la tierra (que indica que se están recibiendo datos del satélite).

---
### Video explicativo
-# (adjuntar video)
