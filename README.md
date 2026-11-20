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
Debido a que las nuevas adiciones al satélite requeriran nuevos tipos de mensajes, los cuales la aplicación de Python tendrá que saber diferenciar. Para poder diferenciar cada mensaje, hemos añadido un caracter identificativo a cada mensaje que varia en función del objetivo de dicho mensaje. En nuestro caso, hemos seguido el siguiente protocolo.
  - Temperaturas y humedades (1): Los mensajes que comiencen por el carácter '1' tendran la siguiente estructura:
      "1:[dato de temperatura]:[dato de humedad]"
  -Medias de temperatura (2): Los mensajes que comiencen por el carácter '2' tendran la siguiente estructura:
      "2:[indicador de dónde se ha de caluclar la media (tierra=0)(satélite=1)]"
  -Alertas y alarmas (3): Los mensajes que comiencen por el carácter '3' tendran la siguiente estructura:
      "3:[tipo de alarma]"
          - (3:0): No se reciben datos del satélite.
          - (3:1): El sensor DHT no esta funcionando correctamente.
          - (3:2): Se ha superado el límite de temperatura.




