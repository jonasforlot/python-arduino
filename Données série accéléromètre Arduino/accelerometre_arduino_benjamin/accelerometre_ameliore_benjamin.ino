    #include "Wire.h"  // Arduino Wire library
    #include "I2Cdev.h"  //bibliothèque I2Cdev à installer
    #include "MPU6050.h" //bibliothèque MPU6050 à installer
    // AD0 low = 0x68 (default for InvenSense evaluation board)
    // AD0 high = 0x69
    MPU6050 accelgyro;
    long temps;
    int16_t ax, ay, az;  //mesures brutes
    int16_t gx, gy, gz;
     
    void setup() {
      Wire.begin();  // bus I2C
      Serial.begin(9600); // liaison série
      while (!Serial) {
        ; // wait for serial port to connect. Needed for native USB (LEONARDO)
      }
      accelgyro.initialize();  // initialize device
      temps = millis();
      
     
      
    }
     
    void loop() {
      temps = millis();
      accelgyro.getAcceleration(&ax, &ay, &az);
      Serial.print(temps); 
      Serial.print("\t");
      Serial.println(ax);  
      
    }
