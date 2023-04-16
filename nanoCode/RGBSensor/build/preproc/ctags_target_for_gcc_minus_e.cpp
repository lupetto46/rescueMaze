# 1 "D:\\User\\Documenti\\ClonedGitRepos\\rescueMaze\\nanoCode\\RGBSensor\\RGBSensor.ino"
# 2 "D:\\User\\Documenti\\ClonedGitRepos\\rescueMaze\\nanoCode\\RGBSensor\\RGBSensor.ino" 2
# 3 "D:\\User\\Documenti\\ClonedGitRepos\\rescueMaze\\nanoCode\\RGBSensor\\RGBSensor.ino" 2


Adafruit_TCS34725 tcs = Adafruit_TCS34725((0xEB) /**< 50.4ms - 21 cycles - Max Count: 21504 */, TCS34725_GAIN_4X);
void setup() {
  Serial.begin(9600); //Sart serial comms @ 9600 (you can change this)
  Serial.println("Color View Test"); //Title info             

  if (tcs.begin()) { //if the sensor starts correctly
    Serial.println("Found sensor"); //print the happy message
  } else { //if the sensor starts incorrectly
    Serial.println("No TCS34725 found ... check your connections");//print the not so happy message
    while (1); // halt!
  }
}

void loop() {
  uint16_t clear, red, green, blue; // takes 50ms to read 

  tcs.getRawData(&red, &green, &blue, &clear);

  Serial.print("C:\t"); Serial.print(clear); //print color values
  Serial.print("\tR:\t"); Serial.print(red);
  Serial.print("\tG:\t"); Serial.print(green);
  Serial.print("\tB:\t"); Serial.print(blue);

                                                                    // Figure out some basic hex code for visualization
  uint32_t sum = clear;
  float r, g, b;
  r = red; r /= sum;
  g = green; g /= sum;
  b = blue; b /= sum;
  r *= 256; g *= 256; b *= 256;
  Serial.print("\t");
  Serial.print((int)r, 16); Serial.print((int)g, 16); Serial.print((int)b, 16);
  Serial.println();

}
