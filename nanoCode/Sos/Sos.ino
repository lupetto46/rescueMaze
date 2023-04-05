
unsigned int distance;

class IRSensor {
	private:
		int pin;
		int prevReaded;

	public:
		IRSensor(int Pin) {
			pin = Pin;
			prevReaded = analogRead(pin);
		}

		unsigned int getDistance() {
			float readed;
			//Serial.print(i);
			unsigned int distance;
			readed = analogRead(pin);
			//Serial.println(readed);
			//Serial.println("");
			readed = readed * (5/1023);
			//Serial.print("Readed True: "); Serial.println(readed);
			distance = 13*pow(readed, -1);
      delay(10);
			return distance;
		}
};

IRSensor sxAv(A0);
IRSensor dxAv(A1);
IRSensor dxPt(A2);
IRSensor sxPt(A3);
IRSensor avDx(A6);
IRSensor avSx(A7);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);
}


void loop() {
  	// put your main code here, to run repeatedly:
  //Serial.print("A0: ");Serial.print(sxAv.getDistance());Serial.println("cm");
  Serial.print("A1: ");Serial.print(dxAv.getDistance());Serial.println("cm");
  /*Serial.print("A2: ");Serial.print(dxPt.getDistance());Serial.println("cm");
  Serial.print("A3: ");Serial.print(sxPt.getDistance());Serial.println("cm");
  Serial.print("A6: ");Serial.print(avDx.getDistance());Serial.println("cm");
  Serial.print("A7: ");Serial.print(avSx.getDistance());Serial.println("cm");*/
  Serial.println("---------------");
  delay(300);
}
