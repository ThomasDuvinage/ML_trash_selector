#include <Servo.h>

#define POUBELLEJ_PIN 9
#define POUBELLEV_PIN 10
#define POUBELLEB_PIN 11

Servo PoubelleJ;
Servo PoubelleV;
Servo PoubelleB;

void setup() {
  Serial.begin(9600);
  
  PoubelleJ.attach(POUBELLEJ_PIN);  
  PoubelleV.attach(POUBELLEV_PIN);
  PoubelleB.attach(POUBELLEB_PIN);

  PoubelleJ.write(3);
  PoubelleV.write(11);
  PoubelleB.write(4);

  pinMode(LED_BUILTIN,OUTPUT);
  digitalWrite(LED_BUILTIN,LOW);
 }

void loop() {
  while(Serial.available()){
     int poubelle = Serial.read();

    if(poubelle == '0'){ //verre
      PoubelleV.write(100);
      delay(2000);
      }
    else if(poubelle == '1'){//plastique et metal
      PoubelleJ.write(100);
      delay(2000);
    }
    else if(poubelle == '2'){//carton
      PoubelleB.write(100);
      delay(2000);
    }
    else{
      PoubelleJ.write(3);
      PoubelleV.write(11);
      PoubelleB.write(4);
    }
  }
}
