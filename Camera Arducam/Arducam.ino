#include <Wire.h>
#include <SPI.h>
#include <ArduCAM.h>
#include "memorysaver.h"

#define CS 7
#define THRESHOLD 500

ArduCAM myCAM(OV5642, CS);

bool capture_in_progress = false;

uint8_t read_fifo_burst(ArduCAM myCAM);

void setup()
{
  Wire.begin();
  Serial.begin(921600);

  pinMode(CS, OUTPUT);
  digitalWrite(CS, HIGH);
  SPI.begin();

  // Reset caméra
  myCAM.write_reg(0x07, 0x80);
  delay(100);
  myCAM.write_reg(0x07, 0x00);
  delay(100);

  // Vérification SPI
  myCAM.write_reg(ARDUCHIP_TEST1, 0x55);
  if (myCAM.read_reg(ARDUCHIP_TEST1) != 0x55)
  {
    Serial.println("SPI ERROR");
    while (1);
  }

  // Vérification OV5642
  uint8_t vid, pid;
  myCAM.wrSensorReg16_8(0xff, 0x01);
  myCAM.rdSensorReg16_8(OV5642_CHIPID_HIGH, &vid);
  myCAM.rdSensorReg16_8(OV5642_CHIPID_LOW, &pid);

  if (vid != 0x56 || pid != 0x42)
  {
    Serial.println("OV5642 NOT FOUND");
    while (1);
  }

  // Init caméra
  myCAM.set_format(JPEG);
  myCAM.InitCAM();
  myCAM.OV5642_set_JPEG_size(OV5642_640x480);
  myCAM.write_reg(ARDUCHIP_TIM, VSYNC_LEVEL_MASK);

  Serial.println("CAMERA READY");
}

void loop()
{
  int sensor = analogRead(A0);

  // Déclenchement
  if (sensor > THRESHOLD && !capture_in_progress)
  {
    capture_in_progress = true;

    myCAM.flush_fifo();
    myCAM.clear_fifo_flag();
    myCAM.start_capture();

    Serial.println("ACK CMD CAM start single shoot. END");
    delay(500);
  }

  // Capture terminée
  if (capture_in_progress && myCAM.get_bit(ARDUCHIP_TRIG, CAP_DONE_MASK))
  {
    Serial.println("ACK CMD CAM Capture Done. END");
    delay(50);
    read_fifo_burst(myCAM);
    myCAM.clear_fifo_flag();
    capture_in_progress = false;
  }

  delay(500);
}

uint8_t read_fifo_burst(ArduCAM myCAM)
{
  uint8_t temp = 0, temp_last = 0;
  uint32_t length = myCAM.read_fifo_length();
  bool is_header = false;

  if (length == 0 || length >= MAX_FIFO_SIZE)
    return 0;

  myCAM.CS_LOW();
  myCAM.set_fifo_burst();

  while (length--)
  {
    temp_last = temp;
    temp = SPI.transfer(0x00);

    if (is_header)
    {
      Serial.write(temp);
    }
    else if (temp == 0xD8 && temp_last == 0xFF)
    {
      is_header = true;
      Serial.println("ACK IMG END");
      Serial.write(temp_last);
      Serial.write(temp);
    }

    if (temp == 0xD9 && temp_last == 0xFF)
      break;

    delayMicroseconds(15);
  }

  myCAM.CS_HIGH();
  return 1;
}
