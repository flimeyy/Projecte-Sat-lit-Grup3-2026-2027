# Proyecto Ingeniería de Satélites: Grupo 3 (EETAC)
### Descripción breve del circuito y código:
En este proyecto se usan dos placas arduino para simular la comunicación de antena a satélite. El satélite envia datos sobre la humedad y temperatura hacia la tierra, donde se procesarán e insertarán en una gráfica dentro de una interfaz gráfica de Python.
El programa de Python, además de mostrar los datos recibidos, permite mandar comandos hacia el satélite para empezar, pausar y reanudar la recepción de datos.

En el caso de que el satélite no pueda recibir datos de temperatura y humedad a través del sensor DHT, la placa Tierra recibirá un mensaje del satélite donde se explica que no se reciben los datos del sensor.
Por otra parte, si la tierra dejara de recibir datos del satélite al pasar 5 segundos, también se recibiría un mensaje de alerta diferente. En ambos casos, se encendería el LED rojo, que indica que hay un error.

Otros elementos del circuito incluyen el LED verde del satélite (que indica que se están transmitiendo datos) y el LED azul de la tierra (que indica que se están recibiendo datos del satélite).

---
### Video explicativo
[<img width="915" height="515" alt="image" src="https://github.com/user-attachments/assets/c6c2b8e7-7d95-4c13-8fca-78c5ca840153" />](https://drive.google.com/file/d/1ykUhEqpNUyoC-kpXGAwzGxvVKVvOCLyA/view?usp=sharing)
---
*Uso de la inteligencia artificial: Nuestro grupo se ha dispuesto a evitar el uso de la IA en lo máximo posible, limitándonos a busquedas excepcionales de ayuda que no se puedan resolver en la documentación oficial del lenguaje de programación. Hasta la fecha (06-11-2026), no se ha hecho ninguna consulta a dichas herramientas.*

---

### Versión 2:
La 2ª versión de nuestro proyecto ha requerido cambios significativos. Desde la incorporación de un sensor de distancia y rotación hasta una nueva estructuración de envio de datos para planificar la posterior incorporación del sistema LoRa (telecomunicaciones). Todos los cambios aplicados se resumen en la siguiente lista:

#### 1. Protocolo de aplicación:
Debido a que las nuevas adiciones al satélite requieren nuevos tipos de mensajes, los cuales la aplicación de Python tendrá que saber diferenciar. Para poder diferenciar cada mensaje, hemos añadido un caracter identificativo a cada mensaje que varia en función del objetivo de dicho mensaje. En nuestro caso, hemos seguido el siguiente protocolo.
- __Iniciación, temperaturas y humedades (1):__ Los mensajes que comiencen por el carácter '1' seran los que indiquen la inicialización del sistema o los que lleven la información captada por el sensor DHT del satélite.<br/>
  Si el mensaje es enviado desde Python, este tendrá esta forma: *"1:[indicador de iniciación(1)/pausa(0)]"*, donde "1:1" indica que se ha de empezar la recepción y "1:0" que se ha de pausar.<br/>
  En cambio, si el Python es el que recibe el mensaje, lo recibirá con la siguiente estructura: *"1:[dato de temperatura(ºC)]:[dato de humedad(%)]"*. Python se encargará de separar el mensaje y asignar cada dato a us respectiva variable.

-__Medias de temperarura (2):__ Los mensajes introducidos por el carácter '2' indican donde se ha de realizar el cálculo de las medias y el resultado de estas.<br/>
Si el mensaje es enviado desde Python, significará que indica dónde se ha de calcular la media de temperatura, el cual se puede realizar en Python(0), o en el satélite(1). De esta manera, estos mensajes seguirán: *"2:[indicador de cálculo en Python(0)/satélite(1)]"*.<br/>
Si el mensaje es recibido en Python, será un mensaje, que, además de enviar la media de temperatura, también enviará junto a ella los datos de temperatura y humedad. Al ser la media de la misma naturaleza de la temperatura, no es necesario un nuevo tipo de mensaje exclusivo para la media. Por lo tanto, el mensaje completo tendrá esta forma: *"2:["*







