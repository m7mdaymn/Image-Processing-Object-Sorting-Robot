import cv2
import numpy as np
import serial
import time
import pyttsx3  # Library for speech synthesis

# Connect to Arduino
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)  # Adjust 'COM3' based on your port
time.sleep(2)  # Delay to ensure the connection stabilizes

# Configure speech synthesis library
engine = pyttsx3.init()

# Adjust speech rate (lower value for slower speech)
rate = engine.getProperty('rate')
engine.setProperty('rate', 120)  # Lower the rate for slower speech

# Variable to track processing status
processing = False

def send_command(command):
    """Send commands to Arduino"""
    global processing
    command_with_newline = command + '\n'
    arduino.write(command_with_newline.encode())
    print(f"Sent command: {command}")
    processing = True  # Indicates the system is processing
    time.sleep(0.1)  # Short delay to ensure data is received

def speak(text):
    """Speak the given text"""
    engine.say(text)
    engine.runAndWait()

def check_arduino_response():
    """Check Arduino's response"""
    global processing
    while arduino.in_waiting:
        response = arduino.readline().decode().strip()
        print(f"Arduino Response: {response}")
        if response == "DONE":  # Arduino's response when it finishes
            processing = False

def detect_objects_by_color(frame):
    """Detect objects based on color"""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Orange color range
    lower_orange = np.array([10, 150, 150])  # Minimum orange color
    upper_orange = np.array([25, 255, 255])  # Maximum orange color

    # Green color range
    lower_green = np.array([35, 100, 100])  # Minimum green color
    upper_green = np.array([85, 255, 255])  # Maximum green color

    # Purple color range
    lower_purple = np.array([120, 100, 100])  # Minimum purple color
    upper_purple = np.array([160, 255, 255])  # Maximum purple color

    # Create masks
    orange_mask = cv2.inRange(hsv, lower_orange, upper_orange)
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    purple_mask = cv2.inRange(hsv, lower_purple, upper_purple)

    # Find objects
    orange_contours, _ = cv2.findContours(orange_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    purple_contours, _ = cv2.findContours(purple_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return orange_contours, green_contours, purple_contours

def main():
    global processing
    cap = cv2.VideoCapture(1)  # You may need to change the index based on your connected camera

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Check Arduino status
        check_arduino_response()

        # Proceed with detection only if not processing
        if not processing:
            # Detect orange, green, and purple objects
            orange_contours, green_contours, purple_contours = detect_objects_by_color(frame)

            # Process orange objects
            if orange_contours:
                largest_orange = max(orange_contours, key=cv2.contourArea)
                if cv2.contourArea(largest_orange) > 1000:  # Ignore small objects
                    x, y, w, h = cv2.boundingRect(largest_orange)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 165, 255), 2)
                    cv2.putText(frame, "Orange Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)

                    send_command("ORANGE")  # Send orange command to Arduino
                    speak("Orange detected")  # Speak the text

            # Process green objects
            if green_contours:
                largest_green = max(green_contours, key=cv2.contourArea)
                if cv2.contourArea(largest_green) > 1000:  # Ignore small objects
                    x, y, w, h = cv2.boundingRect(largest_green)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, "Green Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    send_command("GREEN")  # Send green command to Arduino
                    speak("Apple detected")  # Speak the text

            # Process purple objects
            if purple_contours:
                largest_purple = max(purple_contours, key=cv2.contourArea)
                if cv2.contourArea(largest_purple) > 1000:  # Ignore small objects
                    x, y, w, h = cv2.boundingRect(largest_purple)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (128, 0, 128), 2)
                    cv2.putText(frame, "Purple Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 0, 128), 2)

                    send_command("PURPLE")  # Send purple command to Arduino
                    speak("corrupted object detected")  # Speak the text

        # Display the frame
        cv2.imshow("Frame", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
