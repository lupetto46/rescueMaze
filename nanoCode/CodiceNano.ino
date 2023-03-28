#include <Arduino_LSM9DS1.h>
#include <MadgwickAHRS.h>

// initialize a Madgwick filter:
Madgwick filter;
// sensor's sample rate is fixed at 104 Hz:
const float sensorRate = 104.00;

void setup() {
 Serial.begin(9600);
 // attempt to start the IMU:
 if (!IMU.begin()) {
   Serial.println("Failed to initialize IMU");
   // stop here if you can't access the IMU:
   while (true);
 }
 // start the filter to run at the sample rate:
 filter.begin(sensorRate);
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
    heading = filter.getYaw();
    return heading;
  }
  return -1;
}

int heading;

void loop() {
  heading = getRotation();
  if(!(heading == -1)){
    Serial.println(heading);
  }
}