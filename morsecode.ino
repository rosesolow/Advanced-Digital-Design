//morse code array
String dotdash[26] = {".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..",
".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.",
"...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.."};

int yellowLED = 12;
int redLED = 8;
int led = yellowLED;

void setup() {
  Serial.begin(9600);
  pinMode(yellowLED,OUTPUT);
  pinMode(redLED,OUTPUT);
  //speak(dotdash[0],redLED);
}

void loop() {
  while (Serial.available()) {
    //Serial.println();
    String phrase = Serial.readString(); //read phrase from serial monitor
    //Serial.println(phrase);
    phrase.toUpperCase(); //set phrase to all upper case characters
    int totalChars = phrase.length(); //total length of phrase
    int index = 0;
    //go through each character in word and find corresponding morse code
    while (index < totalChars) {
      char letter = phrase.charAt(index);
      int ascii = letter;
      if (ascii > 64 && ascii < 91) {
        String code = dotdash[ascii - 65];
        speak(code,led);
        Serial.print(letter);
        Serial.println();
        //Serial.println(letter);
      }
      index++;
    }
    led = switch_speakers(led);
    Serial.print('!');
    Serial.println();
  }

}

int switch_speakers(int led){
  if (led == redLED){
    led = yellowLED;
  }
  else {
    led = redLED;
  }
  return led;
}

void speak(String code, int led) {
  int codelength = code.length(); //number of chars in code string
  int i = 0;
  //go through each symbol in morse code and light up led accordingly
  while (i < codelength) {
    char symbol = code.charAt(i);
    //if '.' the light up led and turn buzzer on for 200 ms
    if (symbol == '.') {
      digitalWrite(led, HIGH);
      delay(200);
      digitalWrite(led, LOW);
      delay(200);
    }
    //if '-' then light up led and turn buzzer on for 400 ms
    if (symbol == '-') {
      digitalWrite(led, HIGH);
      delay(400);
      digitalWrite(led, LOW);
      delay(200);
    }
    i++;
  }
  delay(300);
  //Serial.print(code);
}
