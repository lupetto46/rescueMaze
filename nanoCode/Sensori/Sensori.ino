#include <ArduinoJson.h>
#include <Arduino_LSM9DS1.h>
#include <MadgwickAHRS.h>
#include <Wire.h>
#include "Adafruit_TCS34725.h"


#define avDx A0
#define avSx A6
#define dtDx A2
#define dtSx A3
#define dxAv A1
#define sxAv A7
// Global Vars
Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_50MS, TCS34725_GAIN_4X);
StaticJsonDocument<200> doc;
Madgwick filter;
const float sensorRate = 104.00;
int degrees;
// Funcs

void printSerial(String input){
    Serial.flush();
    Serial.println(input);
}

String readSerial(){
    if(Serial.available() > 0){
        String readed = Serial.readStringUntil('#');
        return readed;
    }
    else
    {
        return "-1";
    }
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
    filter.updateIMU((int)xGyro,(int) yGyro,(int) zGyro,(int) xAcc,(int) yAcc,(int) zAcc);

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
    if (tcs.begin()) {                                              //if the sensor starts correctly
    Serial.println("Found sensor");                               //print the happy message
    } else {                                                        //if the sensor starts incorrectly
      Serial.println("No TCS34725 found ... check your connections");//print the not so happy message
      while (1); // halt!
    }
    // start the filter to run at the sample rate:
    filter.begin(sensorRate);
    doc["gyro"] = 0;
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


String readed;
void loop() {
  uint16_t c = tcs.read16(TCS34725_CDATAL);
  uint16_t r = tcs.read16(TCS34725_RDATAL);
  uint16_t g = tcs.read16(TCS34725_GDATAL);
  uint16_t b = tcs.read16(TCS34725_BDATAL);




  degrees = getRotation();
  readed = readSerial();
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
