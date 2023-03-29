void setup()
{
	Serial.begin(9600);
	Serial.setTimeout(1);
}

void printSerial(String input){
  input+="#";
	Serial.print(input);
}

String readSerial(){
  String readed = Serial.readStringUntil('#');
	return readed;
}

void loop()
{
	
  //printSerial();
  
	String input = readSerial();
  printSerial(input);
  delay(1200);
	
}
