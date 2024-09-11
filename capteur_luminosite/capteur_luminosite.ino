/*!
 * @file getLightIntensity.ino
 * @brief Set sensor mode and read light values
 * @n Experimental phenomenon: the light value is read once a second after the sensor device starts successfully
 * @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence     The MIT License (MIT)
 * @author [Fary](fary_young@outlook.com)
 * @version  V1.0
 * @date  2020-12-03
 * @https://github.com/DFRobot/DFRobot_B_LUX_V30B 
 */
#include <DFRobot_B_LUX_V30B.h>
DFRobot_B_LUX_V30B    myLux(13);//The sensor chip is set to 13 pins, SCL and SDA adopt default configuration
long temps;
/* 
   * MANUAL
   *   eAutomatic：The default automatic configuration, after using this mode does not have to configure the following mode, IC automatic configuration. 
   *   eManual ：Manual configuration. This pattern is configured and used in combination with subsequent patterns
   * CDR
   *   eCDR_0：Don't divide the CDR
   *   eCDR_1: Eight divided the CDR
   * TIM
   *   eTime800ms:The collection time is 800ms
   *   eTime400ms:The collection time is 400ms
   *   eTime200ms:The collection time is 200ms
   *   eTime100mse:The collection time is 100ms
   *   Time50ms:The collection time is 50ms
   *   eTime25ms:The collection time is 25ms
   *   eTime12_5ms:The collection time is 12.5ms
   *   eTime6_25ms:The collection time is 6.25ms
   * Manual mode combination
   *   (The collected value cannot exceed the maximum range of each mode. If the read data exceeds the range, the data is not correct)
   *   eManual+eCDR_0+eTime800ms    mode=64    The maximum value collected is: 2938 (Lux)
   *   eManual+eCDR_0+eTime400ms    mode=65    The maximum value collected is: 5875（lux）
   *   eManual+eCDR_0+eTime200ms    mode=66    The maximum value collected is: 11750（lux）
   *   eManual+eCDR_0+eTime100ms    mode=67    The maximum value collected is: 23501（lux）
   *   eManual+eCDR_0+eTime50ms     mode=68    The maximum value collected is: 47002（lux）
   *   eManual+eCDR_0+eTime25ms     mode=69    The maximum value collected is: 94003（lux）
   *   eManual+eCDR_0+eTime12.50ms  mode=70    The maximum value collected is: 200000（lux）
   *   eManual+eCDR_0+eTime6.25ms   mode=71    The maximum value collected is: 200000（lux）
   *   
   *   eManual+eCDR_1+eTime800ms    mode=72    The maximum value collected is: 23501（lux）
   *   eManual+eCDR_1+eTime400ms    mode=73    The maximum value collected is: 47002（lux）
   *   eManual+eCDR_1+eTime200ms    mode=74    The maximum value collected is: 94003（lux）
   *   eManual+eCDR_1+eTime100ms    mode=75    The maximum value collected is: 200000（lux）
   *   eManual+eCDR_1+eTime50ms     mode=76    The maximum value collected is: 200000（lux）
   *   eManual+eCDR_1+eTime25ms     mode=77    The maximum value collected is: 200000（lux）
   *   eManual+eCDR_1+eTime12.50ms  mode=78    The maximum value collected is: 200000（lux）
   *   eManual+eCDR_1+eTime6.25ms   mode=79    The maximum value collected is: 200000（lux）
   */
void setup() {
  Serial.begin(9600);
  myLux.begin();
  /* 
   * The setMode and readMode functions can be omitted. When not configured, the default configuration is the one used last time.
   * When using the setMode function, its return value should be judged. If the return value is 1, the setting is successful.
   * while(!myLux.setMode(myLux.eManual,myLux.eCDR_0,myLux.eTime800ms));
   * Serial.print("mode: ");
   * Serial.println(myLux.readMode());
  */
  temps = millis();
}

void loop() {
  Serial.print("t : ");
  Serial.print("\t");
  Serial.print(temps); 
  Serial.print("\t");
  Serial.print("value: ");
  Serial.print("\t");
  Serial.print(myLux.lightStrengthLux());
  Serial.print("\t");
  Serial.println(" (lux).");
  delay(1000);
 
}
