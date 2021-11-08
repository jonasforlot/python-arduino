#include <Wire.h>
#include <Adafruit_MMA8451.h>
#include <Adafruit_Sensor.h>

Adafruit_MMA8451 mma = Adafruit_MMA8451();
 long temps;

void setup(void) {
   Serial.begin(9600);
   temps = millis();
 //  Serial.println("Adafruit MMA8451 test!");
 mma.begin();
 mma.setRange(MMA8451_RANGE_2_G);
 }

 void loop() {
   // Read the 'raw' data in 14-bit counts
   temps = millis();
   mma.read();
   Serial.print("t : ");
   Serial.print("\t");
   Serial.print(temps); 
   Serial.print("\t");
   Serial.print("ax : "); 
   Serial.print("\t");
   Serial.print(mma.x); 
   Serial.print("\t");
   Serial.print("ay : "); 
   Serial.print("\t");
   Serial.print(mma.y); 
   Serial.print("\t");
   Serial.print("ay : "); 
   Serial.print("\t"); 
   Serial.print(mma.z); 
   Serial.println("\t");
 Serial.println();
   delay(10);
 }
