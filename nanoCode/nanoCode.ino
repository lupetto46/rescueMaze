int bin1 = D2;
int bin2 = D3;
int G = D4;
int B = D5;
int R = D6;
int sensore_di_colore = A0;
int vr, vg,vb;
bool bin1in;
bool bin2in;
void setup() {
  bin1in = false;
  bin2in = false; 
  pinMode(R,OUTPUT);
  pinMode(G,OUTPUT);
  pinMode(B,OUTPUT);
  // put your setup code here, to run once:
  Serial.begin(9600);
 
}

int colore;

void loop() {
  digitalWrite(R,HIGH);
  digitalWrite(G,LOW);
  digitalWrite(B,LOW);
  delay(1);
  vr= analogRead(sensore_di_colore)/4;

  digitalWrite(G,HIGH); //accende il blu
  digitalWrite(R,LOW);
  digitalWrite(B,LOW);
  delay(1);
  vg= analogRead(sensore_di_colore)/4;
  

  digitalWrite(B,HIGH);
  digitalWrite(G,LOW);
  digitalWrite(R,LOW);
  delay(1);
  vb= analogRead(sensore_di_colore)/4;

  Serial.print(vr);
  Serial.print(" ");
  Serial.print(vg);
  Serial.print(" ");
  Serial.println(vb);


  delay(100);
}
