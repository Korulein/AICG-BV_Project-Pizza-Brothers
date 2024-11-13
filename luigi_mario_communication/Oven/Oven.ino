#include "Display.h"
const int max = 10;
int timer[max]; //timer that received from serial
int displaymode = 0;
int add_pizza = 0;
int pizzacount=0;
int ovencmd=0;

const int PIN_BUZZER = 3;
const int pizza_add = 9;  //add 1 pizza
const int start_oven = 8; //send message to start oven
int lastleft=HIGH; //reads last button
int lastright=HIGH; //reads last button
const int empty = 4; //red led
const int done = 5; //green led
const int working =7; //yellow led
String cmd;
int currentpizza=0;

bool doneSent = false; //checking if cmd has been sent or not
void setup() {
  // put your setup code here, to run once:
 Serial.begin(9600);
 pinMode(pizza_add, INPUT_PULLUP);
 pinMode(start_oven, INPUT_PULLUP);
 pinMode(empty, OUTPUT);
 pinMode(done, OUTPUT);
 pinMode(working, OUTPUT);
 pinMode(PIN_BUZZER, OUTPUT);
 digitalWrite(PIN_BUZZER, LOW);
 Display.show(0);
 
 for (int i = 0; i < max; i++) {
      timer[i] = 0; // Set all elements to zero
  }
}
void playSmallTone() {
  tone(PIN_BUZZER, 1000); 
  delay(200);            // Tone duration=
  noTone(PIN_BUZZER);     // Turn off the tone
}
void playMediumTone() {
  tone(PIN_BUZZER, 1000); 
  delay(750);            // Tone duration
  noTone(PIN_BUZZER);     // Turn off the tone
}
void playOvenAlarmTone() {
  int beepFrequency = 1700; 
  int beepDuration = 200;   // Duration of each beep
  int pauseDuration = 100;   // Pause between beeps 
  
  // Play three quick beeps on repeat for 3 times
  for (int repeat = 0; repeat < 3; repeat++) {
  for (int i = 0; i < 3; i++) {
    tone(PIN_BUZZER, beepFrequency); // Start the beep
    delay(beepDuration);             // Hold the beep
    noTone(PIN_BUZZER);              // Turn off the beep
    delay(pauseDuration);            // Pause before the next beep
  }
  delay(300);                // Pause before the next cycle
}
}
void removepizza() {
    if (currentpizza > 0) {
        for (int i = 1; i < currentpizza; i++) {
            timer[i - 1] = timer[i]; // remove the first elemeny by sliding everything
        }
        currentpizza--; // repeat it 
        timer[currentpizza] = 0; 
    }
}
void loop() {
  // put your main code here, to run repeatedly:
   cmd="";
   int currenttime=timer[0];
   // DISPLAY SHOWING AND COUNTDOWN
   if (Serial.available()) {                  // Check if theres a python command
    cmd = Serial.readStringUntil('\n'); 
   }
    if (cmd.length() == 0 && timer[0] ==0){
      digitalWrite(empty, HIGH);
      digitalWrite(done, LOW);
      digitalWrite(working, LOW);
    }
   else if (cmd == "ERROR"){
    playMediumTone();
    cmd="nothing";
    
   }
   
   else if (cmd.length() > 0){
    // reads the time from python
    for (int i = 0; i < max; i++) {
      if (timer[i] ==0){
        timer[i]=cmd.toInt();
        currentpizza++;
         break;}
      }}
    if (currenttime > 1){
      
      Display.show(currenttime);
      digitalWrite(empty, LOW);
      digitalWrite(done, LOW);
      digitalWrite(working, HIGH);
    }
    static unsigned long lastMillis = 0;  // Stores the last time the countdown occurred
    unsigned long currentMillis = millis(); // 
   if (currentMillis - lastMillis >= 1000) { // 1000 milliseconds = 1 second
        lastMillis = currentMillis; // Update lastMillis to the current time
        for (int countdown = 0; countdown < max; countdown++) {
            if (timer[countdown] > 1) {
                timer[countdown] -= 1; // Decrement the timer value
           
            }
        }
}
    Display.show(currenttime);
    

    // BUTTONS FUNCTIONS
    add_pizza=digitalRead(pizza_add); //button to add 1 pizza
    ovencmd=digitalRead(start_oven); //button to start oven
    if (currenttime ==1) {
        digitalWrite(done, HIGH); // Turn on DONE LED
        digitalWrite(working, LOW); // Turn off WORKING LED
        digitalWrite(empty, LOW); // Make sure EMPTY LED is off
    if (doneSent==false){
      playOvenAlarmTone();
      doneSent=true;
    }
   }
   
    if (ovencmd == LOW && lastright == HIGH && currenttime == 1) {
            Serial.print("DONE"); // Send DONE message to Python
            digitalWrite(done, LOW); // Turn off DONE LED
            playMediumTone(); //sound queue
            doneSent=false;
            removepizza();
            

        }
     if(add_pizza==LOW && lastleft==HIGH ){
       pizzacount++;
       playSmallTone();
       //add small buzzer sound to confirm pizza has been added
     }
     
     else if(ovencmd==LOW && lastright==HIGH && pizzacount>0 && digitalRead(done==LOW)){
      Serial.print(pizzacount); //send how many pizzas you've added
      playSmallTone(); //sound queue
      pizzacount=0;}
     
    
    lastright = ovencmd;
    lastleft = add_pizza;
    
    delay(100); // Prevent accidental double looping
}




