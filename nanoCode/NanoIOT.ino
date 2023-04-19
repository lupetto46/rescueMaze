#include <ArduinoJson.h>
#include <MadgwickAHRS.h>
#include <Wire.h>
#include "Arduino_BMI270_BMM150.h"
#include "Servo.h"
#include "Adafruit_TCS34725.h"

#define avDx A0
#define avSx A6
#define dtDx A2
#define dtSx A3
#define dxAv A1
#define sxAv A7
// Global Vars

StaticJsonDocument<200> doc;
Madgwick filter;
const float sensorRate = 104;
int degrees;
Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_240MS, TCS34725_GAIN_1X);
Servo cancello;
Servo pistone;
// Funcs

void printSerial(String msg) {
  Serial.flush();
  Serial.println(msg);
}

int getRotation() {
  float xAcc, yAcc, zAcc;
  float xGyro, yGyro, zGyro;
  // values for orientation:
  float heading;
  // check if the IMU is ready to read:
  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
  // read accelerometer & gyrometer:
    IMU.readAcceleration(xAcc, yAcc, zAcc);
    IMU.readGyroscope(xGyro, yGyro, zGyro);
      
    // update the filter, which computes orientation:
    filter.updateIMU(xGyro, yGyro, zGyro, xAcc, yAcc, zAcc);

    // print the heading, pitch and roll
    heading= filter.getYaw();
    return heading;
  }
  return degrees;
}



void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);
  // attempt to start the IMU:
  if (!IMU.begin()) {
  Serial.println("Failed to initialize IMU");
  // stop here if you can't access the IMU:
  while (true);
  }
  // start the filter to run at the sample rate:

  if (!tcs.begin()) {
    Serial.println("No TCS34725 found ... check your connections");
    while (true);
  }

  pistone.attach(10);
  cancello.attach(9);

  pistone.write(10);
  cancello.write(180);

  filter.begin(sensorRate);
}


int getDist(int pin) {
  float in = analogRead(pin);
  float volt = in * (5.0/1023.0);
  int distance = 13*pow(volt, -1);

  return distance;
}



int distAvDx() { //AVANTI GUARDA DESTRA A0
  return getDist(avDx) - 6;
}

int distDxAv() { // DESTRA GUARDA AVANTI A1
  return getDist(dxAv) - 5;
}

int distDtDx() { //DIETRO GUARDA DESTRA A2
  return getDist(dtDx) - 5;
}

int distDtSx() { //DIETRO GUARDA SINISTRA A3
  return getDist(dtSx) - 6;  
}

int distAvSx(){ //AVANTI GUARDA SINISTRA A6
  return getDist(avSx) - 6;
}

int distSxAv() { //SINISTRA GUARDA AVANTI A7
  return getDist(sxAv) - 4;
}

void spara(int quantita) {
  for(int i = 0; i < quantita; i++) {
    cancello.write(90);
    delay(500);
    pistone.write(0);
    delay(500);
    pistone.write(180);
    delay(500);
    cancello.write(180);
    delay(300);
    cancello.write(90);
    delay(300);
    cancello.write(180);
    delay(1000);
  }
  pistone.write(0);
}

String readed;
void loop() {
  if(Serial.available()) {
    readed = Serial.readStringUntil('\n');
    Serial.println(readed);
    delay(1000);
    if(readed == "1"){
      spara(1);
    }else if(readed == "2"){
      spara(2);
    }else if(readed == "3"){
      spara(3);
      }
    Serial.println("F");
  }

  uint16_t c = tcs.read16(TCS34725_CDATAL);
  uint16_t r = tcs.read16(TCS34725_RDATAL);
  uint16_t g = tcs.read16(TCS34725_GDATAL);
  uint16_t b = tcs.read16(TCS34725_BDATAL);

  degrees = getRotation();
  String jsonOut = "";
  doc["gyro"] = degrees;
  doc["color"][0] = c;
  doc["color"][1] = r;
  doc["color"][2] = g;
  doc["color"][3] = b;
  doc["avDx"] = distAvDx();
  doc["dtDx"] = distDtDx();
  doc["avSx"] = distAvSx();
  doc["dtSx"] = distDtSx();
  doc["dxAv"] = distDxAv();
  doc["sxAv"] = distSxAv();
  serializeJson(doc, jsonOut);
  printSerial(jsonOut);
}
