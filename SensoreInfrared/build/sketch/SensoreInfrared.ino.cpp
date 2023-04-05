#include <Arduino.h>
#line 1 "/home/luphh/Documents/vsCode/Arduino/SensoreInfrared/SensoreInfrared.ino"

unsigned int distance;

class IRSensor {
	private:
		int pin;
		int prevReaded;

	public:
		IRSensor(int Pin) {
			pin = Pin;
			prevReaded = map(analogRead(pin), 0, 700, 0, 1024);
		}

		unsigned int getDistance() {
			float readed;
			float readedTot = 0;
			//Serial.print(i);
			unsigned int distance;
			readed = analogRead(pin);
			//Serial.print("Readed: "); Serial.println(readed);
			//Serial.println("");
			readed = readed * 0.007142857;
			//Serial.print("Readed True: "); Serial.println(readed);
			distance = 13*pow(readed, -1);

			return distance;
		}
};

IRSensor sensor1(A0);

#line 33 "/home/luphh/Documents/vsCode/Arduino/SensoreInfrared/SensoreInfrared.ino"
void setup();
#line 39 "/home/luphh/Documents/vsCode/Arduino/SensoreInfrared/SensoreInfrared.ino"
void loop();
#line 33 "/home/luphh/Documents/vsCode/Arduino/SensoreInfrared/SensoreInfrared.ino"
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}


void loop() {
	int start = millis();
  	// put your main code here, to run repeatedly:
	distance = sensor1.getDistance();
	Serial.print("Readed: ");Serial.print(distance);Serial.print("cm in: ");Serial.println(millis() - start);
}

