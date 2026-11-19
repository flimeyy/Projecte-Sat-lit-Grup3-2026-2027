// Comunicación entre placas arduino
#include <SoftwareSerial.h>
int i;
SoftwareSerial mySerial(10, 11); // RX, TX 
//////////////////////////////
// Led de la tierra
const int led1 = 13;
const int led_error = 12;
int esperandoTimeout = 0;
int nextTimeout = 0;
int temp = 0;
int flag = 0;

void setup() {
   pinMode(led1, OUTPUT);
   pinMode(led_error, OUTPUT);
   Serial.begin(9600);
   mySerial.begin(9600);
}
void loop() {
   int i = millis();
   // Comunicación entre placas arduino
   // Recepción:
   if (mySerial.available()) {
      digitalWrite(led1, HIGH);
      String data = mySerial.readString();
      int codigo = data.substring(0).toInt();
      if (codigo == 3){
         digitalWrite(led_error, HIGH);
         Serial.print(data);
      } else if (codigo != 0) {
         Serial.print(data); // No usamos la función .println() debido a que la información recibida de la otra placa Arduino ya viene con un \n (Se envia con un .println())
         digitalWrite(led_error,LOW);
      }
      digitalWrite(led1, LOW);
      nextTimeout = millis() + 5000;
      flag = 0;
   } 
   temp = millis();
   if (nextTimeout <= temp && flag == 0 && nextTimeout/temp>0){ // Hemos añadido la división para evitar que haya un error por culpa de la conversión del millis()
      digitalWrite(led_error,HIGH);
      Serial.println("3:0");
      nextTimeout = millis() + 5000;
      flag = 1;
   }

   if(Serial.available()){
      String mensaje = Serial.readString();
      if (mensaje == "3")
         digitalWrite(led_error, HIGH);
      else {
         mySerial.println(mensaje);
         digitalWrite(led_error, LOW);
      }
   }
}