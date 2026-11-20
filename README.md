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
+ __Iniciación, temperaturas y humedades (1):__ Los mensajes que comiencen por el carácter '1' seran los que indiquen la inicialización del sistema o los que lleven la información captada por el sensor DHT del satélite.<br/>
  Si el mensaje es enviado desde Python, este tendrá esta forma: __*"1:[indicador de iniciación(1)/pausa(0)]"*__, donde "1:1" indica que se ha de empezar la recepción y "1:0" que se ha de pausar.<br/>
  En cambio, si el Python es el que recibe el mensaje, lo recibirá con la siguiente estructura: __*"1:[dato de temperatura(ºC)]:[dato de humedad(%)]"*__. Python se encargará de separar el mensaje y asignar cada dato a us respectiva variable.

+ __Medias de temperarura (2):__ Los mensajes introducidos por el carácter '2' indican donde se ha de realizar el cálculo de las medias y el resultado de estas.<br/>
Si el mensaje es enviado desde Python, significará que indica dónde se ha de calcular la media de temperatura, el cual se puede realizar en Python(0), o en el satélite(1). De esta manera, estos mensajes seguirán: __*"2:[indicador de cálculo en Python(0)/satélite(1)]"*__.<br/>
Si el mensaje es recibido en Python, será la media calculada desde el satélite. El mensaje se estructurará se esta manera: __"*2:[media de temperatura(ºC)]*"__.

+ __Alertas (3):__ Los mensajes que empiecen con un '3' seran aquellos que le indiquen a Pyhton que estan habiendo problemas, ya sean o de comunicación o de temperatura. Estos mensajes los recibirá Python con la siguiente estructura: __"*3:[indicador de tipo de alerta (0/1/2)]"*__.<br/>
En caso de haber un problema de comunicación con el satélite, este enviará el mensaje: *"3:0"*.<br/>
Si hay algun problema con el sensor DHT de temperatura y humedad, el mensaje será: *"3:1"*.<br/>
Por último, si se detecta que la media ha superado el límite de temperatura préviamente introducido por el usuario, la alerta se enviará de esta forma: *"3:2"*.<br/>

+ __Sensor de distancia (4):__ Los mensajes que tengan como primer carácter '4' indicaran información en relación al sensor de distancia.<br/>
Si el mensaje es enviado por Python, significará que este lleva consigo el grado de rotación nuevo introducido por el usuario. Por tanto, el mensaje se veria tal que así: __*"4:[grado de rotación(º)]"*__.<br/>
No obstante, si el mensaje lo recibe Python, será un mensaje del satélite que informa de las datos captados por los senores ultrasónicos. De esta manera, el mensaje se estructurará de esta forma: __*"4:[distancia captada (sensor1)]:[distancia captada (sensor2)]:[rotación actual]"*__.

 + __Periodio de transmisión (5):__ El mensaje que tenga como primer carácter el '5' será el que modifique el periodo de transmisión. El mensaje se enviará desde Python al satélite con la siguiente estuctura __*"5:[valor de periodo de transmmisión introducido por el usuario]"*__.


#### 2. Cálculo de medias de temperatura y límite:
Con esta nueva incorporación, seremos capaces de ver la media de los últimos 10 valores de temperatura captados por el sensor DHT. Ahora, la gráfica no solo dibuja la variación de humedad y temperatura, sinó que también la media de esta última. Además, también hemos implementado un sistema que activa una alerta si detecta que los tres últimos datos de la media superan un cierto límite introducido por el usuario a través de un nuevo 'slider' en la interfaz.<br/>
No obstante, el cálculo y la comunicación de la media requiere su propio proceso, el cual puede alterar el funcionamiento del sistema entero dependiendo de donde se realice el cálculo de la media. Debido a esto, le damos la libertad al usuario de poder elegir dónde se realizará este proceso en función de sus intereses a través de dos nuevos botones en la interfaz gráfica.<br/>
Por una parte, calcularlo en el satélite otorga mayor agilidad para activar la alerta en caso de que la temperatura media sobrepase el límite. Por otra parte, si el usuario decide calcularla en Python ahorra un gasto de energía en el satélite que es mas permisible en tierra.

#### 3. Sensor de distancia:
Usando sensores ultrasónicos HC-SR04, hemos incorporado un sistema que detecte objetos cercanos al satélite.<br/>
No obstate, el sensor ultrasónico tiene un rango fijo de 180º, el cual no nos permite detectar objetos que no esten en dicho rango. Para solucionar esto, hemos implementado otro sensor ultrasónico en sentido contrario, ademas de asir ambos a un servo motor. Con estas implementaciones, el satélite es capaz de detectar objetos próximos en un mayor rango.
Seremos capaces de ver estos objetos a través de una nueva gráfica que nos indica la distancia y la posicion a la que se encuentran respecto al sensor.<br/>
Además, el usuario tiene la libertad de introducir el grado de rotación al que quiera que gire el sensor. También tiene la opción de reiniciar la rotación del satélite is asi lo desea.

#### 4. Modificación de periodos de transmisión:
Por último, en esta versión del proyecto también hemos añadido una función que permite al usaurio modificar el periodo de transmisión de datos, modificando el intervalo en el que préviamente trabajaba el código del satélite y sustituyendolo por el nuevo valor introducido por el usuario.



