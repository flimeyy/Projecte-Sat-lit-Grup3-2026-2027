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
const int led = 13;  // LED en el pin 13 
const int interval = 3000; // 3 segundos para el LED 13
long inicio_temp;
long heartbeat;

int temperatura = 0;


void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
  dht.begin();
  pinMode(led, OUTPUT);
  inicio_temp = millis();
  heartbeat = millis();
}

void loop() {
  if (mySerial.available()) {
      String comando = mySerial.readString();
      int fin=comando.indexOf(':',0);
      int codigo = comando.substring(0, fin).toInt();
      if (codigo == 1){
        codigo = comando.substring(fin+1, fin+2).toInt();
        if (codigo == 0){
          temperatura = 0;
        }
        if (codigo == 1){
          temperatura = 1;
        }
      }
  }

  if ((millis() - inicio_temp >= interval) && (temperatura == 1)) {
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
      //Serial.println("Funciona");
      esperandoTimeout = false;
      mySerial.print("1:");
      mySerial.print(h);
      mySerial.print(":");
      mySerial.println(t);
    }
    digitalWrite(led,LOW);
    // Siguiente instante en el que habrá que cambiar
    inicio_temp = millis();
  }
  if (esperandoTimeout && (millis() - nextTimeoutHT >= 5000)){
    mySerial.println (3);
    esperandoTimeout = false;
    nextTimeoutHT = millis();
  }

  if (millis() - heartbeat >= 1000){
    mySerial.println(0);
    heartbeat = millis();
  }
}