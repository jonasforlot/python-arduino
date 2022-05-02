#include <phyphoxBle.h> 
#include <Arduino.h>
#include "LSM6DS3.h"
#include "Wire.h"

float accx, accy, accz, acc;
float gyrx, gyry, gyrz, gyr;


void setup() {
  PhyphoxBLE::start();                //Start the BLE server

   Wire.begin();
   Serial.begin(115200);
  
  accelerometer.begin();
  if(accelerometer.isActive()){
    Serial.println("Accelerometer already active");
  }else{
    if(accelerometer.powerOn()){
      Serial.println("Accelerometer Power ON");
    }else{
      Serial.println("Accelerometer Not Powered On");
    }
  accelerometer.changeFullScale(XL_FS_16G);


  }

}


void loop() {
  if (accelerometer.isActive()) {

      accx = accelerometer.getConvertedXAxis(), 2;   
    }


      Serial.println(accx);

      PhyphoxBLE::write(accx);

      PhyphoxBLE::poll();                  //IMPORTANT: In contrast to other devices, poll() needs to be called periodically on the 33 IoT
 
   
}
