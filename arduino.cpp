#include <Servo.h>

Servo base;    // The base servo
Servo arm;     // The arm servo
Servo gripper; // The gripper servo

String command = ""; // To store received commands

void setup() {
  Serial.begin(9600); // Start serial communication
  base.attach(10);    // Connect base servo to pin 10
  arm.attach(11);     // Connect arm servo to pin 11
  gripper.attach(12); // Connect gripper servo to pin 12

  // Initial position
  arm.write(90);      // Arm raised
  gripper.write(0);   // Gripper closed
  base.write(90);     // Base centered
}

void loop() {
    delay(1000);
    startmotion();

  // Read commands from serial
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {  // When the entire line is received

      Serial.println("Command Received: " + command); // Confirm receipt
      handleCommand(command); // Execute the command
      command = "";           // Reset the command
    } else {
      command += c; // Append characters to the command
    }
  }
}

void handleCommand(String cmd) {
  if (cmd == "ORANGE") {
    // Execute the ORANGE command
    Serial.println("Executing ORANGE Command");
    base.write(0);      // Base to 0°
    delay(2000);
    arm.write(90);       // Lower the arm
    delay(2000);
    gripper.write(180); // Open the gripper
    delay(1000);
    Serial.println("DONE");
    resetPosition(); 
  } else if (cmd == "GREEN") {
    // Execute the GREEN command
    Serial.println("Executing GREEN Command");
    base.write(180);    // Base to 180°
    delay(2000);
    arm.write(90);       // Lower the arm
    delay(2000);
    gripper.write(180); // Open the gripper
    delay(1000);
    Serial.println("DONE"); 
    resetPosition();
  } else{
    Serial.println("Unknown Command: " + cmd); // Print message if the command is unknown
    }
}

void resetPosition() {
  arm.write(180); 
  delay(2000);      
  gripper.write(0); 
  delay(1000);      
  base.write(90); 
  delay(1000);      
}

void startmotion() {
  delay(1000);
  arm.write(90);
  delay(2000);       
  arm.write(0);
  delay(2000);       
  gripper.write(180);
  delay(5000);
  gripper.write(0);
  delay(4000);
  arm.write(180);
  delay(5000);
}

