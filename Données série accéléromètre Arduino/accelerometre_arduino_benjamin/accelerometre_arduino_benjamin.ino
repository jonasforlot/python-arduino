    #include "Wire.h"  // Arduino Wire library
    #include "I2Cdev.h"  //bibliothèque I2Cdev à installer
    #include "MPU6050.h" //bibliothèque MPU6050 à installer
    // AD0 low = 0x68 (default for InvenSense evaluation board)
    // AD0 high = 0x69
    MPU6050 accelgyro;
    long temps;
    int16_t ax, ay, az;  //mesures brutes
    int16_t gx, gy, gz;
    int valeur_tension;
    float tension;
     
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
//      accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
      temps = millis();
      valeur_tension = analogRead(A0);
      tension = valeur_tension*5.0/1023;
      // On peut aussi utiliser ces méthodes
      accelgyro.getAcceleration(&ax, &ay, &az);
      //accelgyro.getRotation(&gx, &gy, &gz);
     
      // Affichage accel/gyro x/y/z
//      Serial.print("a/g:\t");
//      Serial.print(ax); 
//      Serial.print("\t");
      Serial.print("t : ");
      Serial.print("\t");
      Serial.print(temps); 
      Serial.print("\t");
      Serial.print("ax : "); 
      Serial.print("\t");
      Serial.print(ax);//    
      Serial.print("\t");
      Serial.print("ay : "); 
      Serial.print("\t");
      Serial.print(ay);//    
      Serial.print("\t");
      Serial.print("az : "); 
      Serial.print("\t");  
      Serial.print(az); 
      Serial.print("\t");
      Serial.print("Tension : "); 
      Serial.print("\t");
      Serial.print(tension);//     
      Serial.println("\t");

//      Serial.print(gx); 
//      Serial.print("\t");
//      Serial.print(gy); 
//      Serial.print("\t");
//      Serial.print(gz); 
//      Serial.println("\t");
      delay(50);  
    }
