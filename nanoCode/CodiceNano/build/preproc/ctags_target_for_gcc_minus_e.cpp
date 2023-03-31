# 1 "D:\\User\\Documenti\\ClonedGitRepos\\rescueMaze\\nanoCode\\CodiceNano\\CodiceNano.ino"
# 2 "D:\\User\\Documenti\\ClonedGitRepos\\rescueMaze\\nanoCode\\CodiceNano\\CodiceNano.ino" 2
# 3 "D:\\User\\Documenti\\ClonedGitRepos\\rescueMaze\\nanoCode\\CodiceNano\\CodiceNano.ino" 2
# 4 "D:\\User\\Documenti\\ClonedGitRepos\\rescueMaze\\nanoCode\\CodiceNano\\CodiceNano.ino" 2

// Global Vars

StaticJsonDocument<200> doc;
Madgwick filter;
const float sensorRate = 104.00;
int heading;
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
  float heading_;
  // check if the IMU is ready to read:
  if (IMU_LSM9DS1.accelerationAvailable() && IMU_LSM9DS1.gyroscopeAvailable()) {
  // read accelerometer & gyrometer:
    IMU_LSM9DS1.readAcceleration(xAcc, yAcc, zAcc);
    IMU_LSM9DS1.readGyroscope(xGyro, yGyro, zGyro);


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
    if (!IMU_LSM9DS1.begin()) {
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
