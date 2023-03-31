#include <Arduino.h>
#line 1 "D:\\User\\Documenti\\ClonedGitRepos\\rescueMaze\\nanoCode\\CodiceNano\\CodiceNano.ino"
#include <ArduinoJson.h>
#include <Arduino_LSM9DS1.h>
#include <MadgwickAHRS.h>

// Global Vars

StaticJsonDocument<200> doc;
Madgwick filter;
const float sensorRate = 104.00;
int heading;
// Funcs

#line 13 "D:\\User\\Documenti\\ClonedGitRepos\\rescueMaze\\nanoCode\\CodiceNano\\CodiceNano.ino"
void printSerial(String input);
#line 18 "D:\\User\\Documenti\\ClonedGitRepos\\rescueMaze\\nanoCode\\CodiceNano\\CodiceNano.ino"
String readSerial();
#line 29 "D:\\User\\Documenti\\ClonedGitRepos\\rescueMaze\\nanoCode\\CodiceNano\\CodiceNano.ino"
int getRotation();
#line 52 "D:\\User\\Documenti\\ClonedGitRepos\\rescueMaze\\nanoCode\\CodiceNano\\CodiceNano.ino"
void setup();
#line 68 "D:\\User\\Documenti\\ClonedGitRepos\\rescueMaze\\nanoCode\\CodiceNano\\CodiceNano.ino"
void loop();
#line 13 "D:\\User\\Documenti\\ClonedGitRepos\\rescueMaze\\nanoCode\\CodiceNano\\CodiceNano.ino"
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
  float heading_;
  // check if the IMU is ready to read:
  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
  // read accelerometer & gyrometer:
    IMU.readAcceleration(xAcc, yAcc, zAcc);
    IMU.readGyroscope(xGyro, yGyro, zGyro);

      
    // update the filter, which computes orientation:
    filter.updateIMU((int)xGyro,(int) yGyro,(int) zGyro,(int) xAcc,(int) yAcc,(int) zAcc);

    // print the heading, pitch and roll
    heading_ = filter.getYaw();
    return heading_;
  }
  return heading;
}

void setup() {
    Serial.begin(19200);
    // attempt to start the IMU:
    if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU");
    // stop here if you can't access the IMU:
    while (true);
    }
    // start the filter to run at the sample rate:
    filter.begin(sensorRate);
    doc["gyro"] = 0;
}

String readed;
String jsonz;

void loop() {
    heading = getRotation();
    readed = readSerial();
    jsonz = "";
    doc["gyro"] = heading;
    serializeJson(doc, jsonz);
    if(readed == "get") {
        printSerial(jsonz);
    }
}

