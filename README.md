# Image-Processing-Object-Sorting-Robot
A Python- and Arduino-powered robotic arm that detects objects using image processing with OpenCV and sorts them into categories. Features real-time image analysis, text-to-speech announcements, and precise robotic arm control for automated sorting tasks.

Image Processing Object Sorting Robot
This project combines Python, OpenCV, and Arduino to create an automated robotic arm capable of sorting objects based on color detection using image processing techniques. It features real-time image analysis, text-to-speech feedback, and servo motor control for precise movements.

Key Features
Image Processing: Uses OpenCV to detect objects based on their colors (orange, green, and purple).
Robotic Control: Arduino-driven robotic arm with servos for movement and a gripper for object handling.
Text-to-Speech Feedback: Provides audible announcements for detected objects using pyttsx3.
Seamless Communication: Python script communicates with Arduino via serial for synchronized actions.
Components Used
Hardware:

Arduino board
Servo motors (base, arm, gripper)
Camera for real-time image capture
Software:

Python with OpenCV for object detection
pyttsx3 for speech synthesis
Arduino code for servo motor control
How It Works
The camera captures a live video feed and detects objects based on predefined color ranges.
Detected objects are classified and highlighted in the video stream.
The Python script sends commands to the Arduino to move the robotic arm and sort the detected object.
The robotic arm adjusts its base, arm, and gripper to place the object in the correct location.
Applications
Automated sorting in manufacturing or packaging lines.
Educational projects showcasing the integration of computer vision and robotics.
Prototyping intelligent sorting systems.
Getting Started
Clone this repository.
Set up the Arduino and servo motors as described in the documentation.
Install required Python libraries: OpenCV, pyttsx3, and serial communication.
Run the Python script while the Arduino is connected and powered.
