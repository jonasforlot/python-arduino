#include <SPI.h>
#include <SD.h>

#include <Wire.h>


const int MPU2 = 0x69, MPU1=0x68;

long accelX, accelY, accelZ,accel;



long temps;



File fichierSD;

    
void setup() {
   Wire.begin();
  Wire.beginTransmission(MPU1);
  Wire.write(0x6B);
  Wire.write(0b00000000);
  Wire.endTransmission();  
  Wire.beginTransmission(MPU1);
  Wire.write(0x1B);
  Wire.write(0x00000000);
  Wire.endTransmission(); 
  Wire.beginTransmission(MPU1);
  Wire.write(0x1C);
  Wire.write(0b00000000);
  Wire.endTransmission(); 
  
  Wire.begin();
  Wire.beginTransmission(MPU2);
  Wire.write(0x6B);
  Wire.write(0b00000000); 
  Wire.endTransmission();  
  Wire.beginTransmission(MPU2); 
  Wire.write(0x1B);
  Wire.write(0x00000000);
  Wire.endTransmission(); 
  Wire.beginTransmission(MPU2);
  Wire.write(0x1C);
  Wire.write(0b00000000);
  Wire.endTransmission(); 
//  Serial.begin(9600); // liaison série
//  while (!Serial) {
//    ; // wait for serial port to connect. Needed for native USB (LEONARDO)
//  }
//      
//  Serial.println(F("Initialisation OK"));

//  Initialisation de la carte SD
    if(!SD.begin(10)) {
//      Serial.println(F("Initialisation SD impossible !"));
    return;
    }
    

 
  
 
  
}
     
void loop() {
  temps = millis();
//  Serial.print(temps);
//  
//  Serial.print("\t");
//  Serial.print("Acc1\t");
//  Serial.print(GetMpuValue(MPU1));
//  Serial.print("\t ||| Acc2\t");
//
//  Serial.print(GetMpuValue(MPU2));
//  Serial.println(""); 

   fichierSD = SD.open("acc3.txt", FILE_WRITE);
 

   
   if(fichierSD) {
//     Serial.println(F("Ecriture en cours"));
   //Ecriture
 fichierSD.print(temps);
  
  fichierSD.print("\t");
//  fichierSD.print("Acc1\t");
  fichierSD.print(GetMpuValue(MPU1));
//  fichierSD.print("\t ||| Acc2\t");
fichierSD.print("\t");
  fichierSD.print(GetMpuValue(MPU2));
  fichierSD.println(""); 

fichierSD.close();
  }
}
  
  
int GetMpuValue(const int MPU){
  
  Wire.beginTransmission(MPU); 
  Wire.write(0x3B);
  Wire.endTransmission();
  Wire.requestFrom(MPU,6);
  while(Wire.available() < 6);
  accelX = Wire.read()<<8|Wire.read(); 
  accelY = Wire.read()<<8|Wire.read(); 
  accelZ = Wire.read()<<8|Wire.read();
  accel = sqrt(accelX*accelX+accelY*accelY+accelZ*accelZ);
 
  
 return(accel);

}
