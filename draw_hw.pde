import ddf.minim.*;
import ddf.minim.analysis.*;
import ddf.minim.effects.*;
import ddf.minim.signals.*;
import ddf.minim.spi.*;
import ddf.minim.ugens.*;

import cc.arduino.*;
import org.firmata.*;
import processing.serial.*;

//activate libraries
Minim minim; // sound library
Arduino arduino; // arduino library

//creating colors, HSB
int H = 0;
int S = 500;
int B = 500;

int brushWidth = 8;
int brushHeight = 8;

AudioPlayer song;

int read;
boolean square = false;
boolean triangle = false;
boolean circle = true;
boolean party = false;
int n = 0;

int prevX = 0;
int prevY = 0;

void setup() {

  //GRAPHICS SETUP

  //Creating Canvas
  colorMode(HSB, 700);
  size(1010, 800);
  background(0,0,700);
  noStroke();

  //Creating interface panel
  fill(0,0,0);
  rect(600, 0, 410, 800);
  
  PImage img = loadImage("img.jpg");
  image(img, 605, 50);
  fill(100,500,500);
  textSize(25);
  text("Advanced Digital Design", 680, 450);
  
  fill(0,0,700);
  textSize(20);
  text("Choose color by turning knob:",680,490);
  text("Press:", 709, 642);
  int step = 20;
  text("N for a new canvas", 709, 667);
  text("S for a square brush", 709, 667+step);
  text("T for a triangle brush", 709, 667+step*2);
  text("C for a circle brush", 709, 667+step*3);
  text("P for party mode", 709, 667+step*4);
  text("Q to quit party mode", 709, 667+step*5);
  
  // initiate sound library
  minim = new Minim(this);
  song = minim.loadFile("song.mp3");
  
  arduino = new Arduino(this, "COM5", 57600);
  arduino.pinMode(0, Arduino.INPUT);
  arduino.pinMode(13, Arduino.OUTPUT);
  arduino.pinMode(12, Arduino.OUTPUT);
  arduino.pinMode(11, Arduino.OUTPUT);
}

void draw() {
  
  //paintbrush color from pot
  read=arduino.analogRead(0);
  //println(read);
  H = read;
  fill(H, S, B);
  rect(750, 500, 120, 120);
  
  n++;
  if (n>10) {
    n=0;
    if (party){
      //flash leds
      for (int led = 11; led <= 13; led = led+1) {
        int power = int(random(2));
        if (power == 1){
          arduino.digitalWrite(led, Arduino.HIGH); 
        }
        else {
          arduino.digitalWrite(led, Arduino.LOW); 
        }
      }
    }
  }
}

void mouseDragged() {

  // paint brush draw with mouse
  if (mouseX < 590) {
    fill(H, 500, 500);
    if (square){
      rect(mouseX-10, mouseY-10, brushWidth, brushHeight);
    }
    if (triangle){
      triangle(mouseX-10, mouseY-10, mouseX, mouseY, mouseX+10, mouseY-10);
    }
    if (circle) {
      ellipse(mouseX-10, mouseY-10, brushWidth, brushHeight);
    }
  }
  
  //playing around with speed of mouse and brightness of led on pwm pin
  //int pwm = 5*(abs(mouseX - prevX) + abs(mouseY - prevY))/2;
  //println(pwm);
  //prevX = mouseX; prevY=mouseY;
  //if (pwm > 255){pwm=255;}
  //arduino.analogWrite(11, pwm);  
}

void keyPressed() {

  if (key == 'n') // Clears canvas for new painting
  {
    fill(0,0,700);
    rect(0, 0, 600, 800);
  }
  
  if (key == 's')
  {
    square = true; 
    circle = false;
    triangle = false;
  }
  
  if (key == 't')
  {
    square = false; 
    circle = false;
    triangle = true;
  }
  
  if (key == 'c')
  {
    square = false; 
    circle = true;
    triangle = false;
  }
  
  if (key == 'p')
  {
    party = true; 
    println("!!!!!party!!!!!");
    song.play();
    song.rewind();
  }
  
  if (key == 'q'){
    party = false;
    for (int led = 11; led <= 13; led = led+1) {
      arduino.digitalWrite(led, Arduino.LOW); 
    }
    song.pause();
    song.rewind();
  }
}
