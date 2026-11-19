// Definiciones necesarias sensor de temperatura
#include <DHT.h>
#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
int esperandoTimeout;
int nextTimeoutHT;

// Declaraciones comunicacion entre Arduinos
#include <SoftwareSerial.h>
SoftwareSerial mySerial(10, 11); // RX, TX

// Led y control de tiempo
const int led = 12;  // LED en el pin 13 
const int interval = 3000; // 3 segundos para el LED 13
long inicio_temp;
long heartbeat;

int temperatura = 0;

int mediasat= 0;//Se activa cuando queramos calcular la media en el satélite
float temperaturas[10]={0}; //Aqui almacenaremos las 10 ultimas temperaturas

int i=0;

float suma=0;
float media;
int cont_temp=0; //Contador de temperaturas
int cont_medias=0; //Contador de medias superiores al limite

int limite;

#include <Servo.h>
#include <string.h>
Servo servoMotor;

int rotar = true;
int grado = 0;
int ejecutar = 1;
// Pines del sensor ultrasonidos
const int trigPin1 = 9;
const int echoPin1 = 8;
const int trigPin2 = 7;
const int echoPin2 = 6;

// Variables del sensor ultrasonidos
float time1,time2,distance1,distance2;
long time;

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
  dht.begin();
  pinMode(led, OUTPUT);
  digitalWrite(led, LOW);
  inicio_temp = millis();
  heartbeat = millis();

  time = millis();
  pinMode(trigPin1, OUTPUT);
  digitalWrite(trigPin1,LOW);
  pinMode(echoPin1, INPUT);

  pinMode(trigPin2, OUTPUT);
  digitalWrite(trigPin2,LOW);
  pinMode(echoPin2, INPUT);
  servoMotor.attach(3);
}

void loop() {
  if (mySerial.available()) {
      String comando = mySerial.readString();
      int fin=comando.indexOf(':',0);
      int codigo = comando.substring(0, fin).toInt();
      Serial.println(comando);
      if (codigo == 1){
        //Serial.println(codigo);
        codigo = comando.substring(fin+1, fin+2).toInt();
        if (codigo == 0){
          temperatura = 0;
        }
        if (codigo == 1){
          //Serial.println("f");
          temperatura = 1;
        }
      }
      else if(codigo == 2){
        codigo = comando.substring(fin+1, fin+2).toInt();
        if (codigo == 0){
          mediasat = 0;
        }
        if (codigo == 1){
          mediasat = 1;
          limite = comando.substring(4,7).toInt();
          Serial.println(limite);
        }
      }
      else if (codigo == 4){
        int fin2 = comando.indexOf(':',2);
        int mensaje = comando.substring(fin+1,fin2).toInt();
        if (mensaje != -1){
          grado = mensaje;
          rotar = false;
        } else {
          rotar = true;
        }
      }
      else if (codigo == 5){
        int fin2 = comando.indexOf(':',2);
        int mensaje = comando.substring(fin+1,fin2).toInt();
        interval = mensaje*1000;
      }
  }

  if ((millis() - inicio_temp >= interval) && (temperatura == 1)) {
    //Serial.println("F");
    digitalWrite(led, HIGH);
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    if ((isnan(h)) || (isnan(t))){
      if (esperandoTimeout == false){
        esperandoTimeout = true;
        nextTimeoutHT = millis(); // 5 segundos
      }
    }
    else {
      esperandoTimeout = false;
      if (mediasat==1){
        temperaturas[i]=t;
        cont_temp++;
        suma += t;

        if (cont_temp == 10){
          suma -= temperaturas[0];
          media=suma/10;
        } else if (cont_temp > 10){
          suma -= temperaturas[i+1];
          media = suma/10;
        }
        else
          media=suma/cont_temp;
        //Serial.println(suma, media);
        
        if (media>limite)
          cont_medias++;
        else 
          cont_medias=0;
        
        if (cont_medias==3) { //las tres últimas medias de temperatura han superado el límite
          mySerial.println("3:2");
        } else {
          mySerial.print("1:");
          mySerial.print(h);
          mySerial.print(":");
          mySerial.print(t);
          mySerial.print(":");
          mySerial.println(media);
        }
        i++; //Para las temperaturas
        if (i>=10)
          i=0;
        //Serial.println(i);
      }
      else{
        //Serial.println("Funciona");
        mySerial.print("1:");
        mySerial.print(h);
        mySerial.print(":");
        mySerial.println(t);
      }
    }
    digitalWrite(led,LOW);
    // Siguiente instante en el que habrá que cambiar
    inicio_temp = millis();
  }
  if (esperandoTimeout && (millis() - nextTimeoutHT >= 5000)){
    mySerial.println ("3:1");
    esperandoTimeout = false;
    nextTimeoutHT = millis();
  }

  if (millis() - heartbeat >= 1000){
    mySerial.println(0);
    heartbeat = millis();
  }

  //Radar
  if (ejecutar){    
    // SENSOR ULTRASONIDOS
    digitalWrite(trigPin1,HIGH);
    delay(10);  //Mandamos una pulsación al trigger del sensor ultrasonido de 10 milisegundos.
    digitalWrite(trigPin1,LOW);
    time1 = pulseIn(echoPin1,HIGH); // El pulseIn nos permite medir el ancho de pulso (el tiempo que tarda en volver el sonido enviado con el trigger)

    digitalWrite(trigPin2,HIGH); // Repetimos el priceso explicado  para el segundo sensor ultrasonidos
    delay(10);
    digitalWrite(trigPin2,LOW);
    time2 = pulseIn(echoPin2,HIGH);

    if (millis()-time >= 1000 || grado == 180){
      distance1 = time1/59; // "https://naylampmechatronics.com/blog/10_tutorial-de-arduino-y-sensor-ultrasonico-hc-sr04.html" hace una demostración matemática de como dividir los milisegundos del sensor por 59 nos permite obtener la distancia en cm.
      distance2 = time2/59;
      Serial.print("4:");
      Serial.print(distance1);
      Serial.print(":");
      Serial.print(distance2);
      Serial.print(":");
      Serial.println(grado); // Mandamos toda la información en el formato establecido por Ramón: id:distancia1:distancia2:pos_servomotor
      time = millis();
      // OJO: Este código supone que el clima es perfecto (25ºC). Para la versión 4, planeamos tener en cuenta el clima que hará para calcular la velocidad del sonido en ese ambiente.
      ///////////////////////////////////////////////////////////
    }
  if (rotar & grado < 180){ // Generamos un bucle donde el servomotor girará (casi) constantemente sin interrupciones (es decir, cada ejecución del código, el servomotor aumentará 1º su rotación)
      grado=grado+1;
    } else if (rotar) {
      grado=0; // En el caso de que el grado sea igual (o, en caso de error, mayor a 180º), el
    }
    servoMotor.write(grado);
  }
}