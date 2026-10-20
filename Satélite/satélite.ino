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
long inicio;

int temperatura = 0;


void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
  dht.begin();
  pinMode(led, OUTPUT);
  inicio = millis();
}

void loop() {
  if (mySerial.available()) {
      String estado_temp = mySerial.readString();
      if (estado_temp == "satoff"){
        temperatura = 0;
      }
      if (estado_temp == "saton"){
        temperatura = 1;
      }
  }

  if ((millis() - inicio >= interval) && (temperatura == 1)) {
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
      Serial.println("Funciona");
      esperandoTimeout = false;
      mySerial.print("H:");
      mySerial.print(h);
      mySerial.print(":T:");
      mySerial.println(t);
    }
    digitalWrite(led,LOW);
    // Siguiente instante en el que habrá que cambiar
    inicio = millis();
  }
  if (esperandoTimeout && (millis() - nextTimeoutHT >= 5000)){
    mySerial.print ("Fallo");
    esperandoTimeout = false;
    nextTimeoutHT = millis();
  }
}