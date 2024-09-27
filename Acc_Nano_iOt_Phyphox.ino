/*
  Arduino LSM6DS3 - Simple Accelerometer

  This example reads the acceleration values from the LSM6DS3
  sensor and continuously prints them to the Serial Monitor
  or Serial Plotter.

  The circuit:
  - Arduino Uno WiFi Rev 2 or Arduino Nano 33 IoT

  created 10 Jul 2019
  by Riccardo Rizzo

  This example code is in the public domain.
*/

#include <Arduino_LSM6DS3.h>
#include <phyphoxBle.h> 
#include <Wire.h> // Inclure la bibliothèque Wire pour la communication I2C



void setup() {
  PhyphoxBLE::start();                //Start the BLE server
  Wire.begin(); // Initialiser la communication I2C
  delay(100); // Laisser le temps au capteur de s'initialiser
     
  Serial.begin(9600);


  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");

    while (1);
  }

  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Acceleration in g's");
  Serial.println("X\tY\tZ");
}

void loop() {
  float x, y, z;

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);

    Serial.println(x);
   PhyphoxBLE::write(x);

   PhyphoxBLE::poll();                  //IMPORTANT: In contrast to other devices, poll() needs to be called periodically on the 33 IoT

    
  }
}
