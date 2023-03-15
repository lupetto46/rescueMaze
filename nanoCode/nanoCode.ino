int bin1 = D2;
int bin2 = D3;
int sensore_di_colore = A0;

bool bin1in;
bool bin2in;
void setup() {
  bin1in = false;
  bin2in = false;
  // put your setup code here, to run once:
  Serial.begin(9600);
}

int colore;

void loop() {
  // put your main code here, to run repeatedly:
  colore = analogRead(sensore_di_colore);
  //Serial.println(colore);

  if(colore > 940)
  {
    bin1in = true;
    bin2in = false;
    Serial.print("Nero: ");
    Serial.print(bin1in);
    Serial.println(bin2in);
  }
  else if (colore > 900)
  {
    bin1in = false;
    bin2in = false;
    Serial.print("Bianco: ");
    Serial.print(bin1in);
    Serial.println(bin2in);
  }
}
