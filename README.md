# Areomanthus-Project - By Ethan Wong
This repository consists of a hand detection system I made in Python that detects your hands using your built in computer camera, the 3D models for the designs of the parts printed, and also the overall code used as well as electronics.
The main purpose of this project is for an educational purpose while also to accomplish what I have seen rarely done.

As to begin my explanation for each step of the code and also their purpose, it's best to start with the design plan for the system.

# The Claw/Hand

The Claw/Hand of the arm will be it's primary purpose, which is to interact with it's surrounding environment when given the command.

For the electronics, I will be using an estimated amount of 2-3 ESP32 Developer Boards alongside approximately 10-15 SG90 Mirco Servos.
Essentially, the method in which the claw will operate will recive signals from a camera that detects the mapping of a hand and translate those movements to the SG90's.

The first thing I had to do was code the mapping via camera on python. The best libraries to use for this are cv2 and mediapipe. Essentially, the camera used on my computer will run its standard amount of frames and this only changes when mediapipe begins detecting for my hand whilst cv2 will be used to have mediapipe analyze the frames from the camera. In order to do this, cv2 will constantly take frames and let mediapipe map out the planes of my hand with "landmarkers." The numbers i'm trying to use here are 8 and 4. This is because 8 is the tip of your pointer finger and 4 is the tip of your thumb. 

```python
distance = ((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2) ** 0.5
```

This line of code is the distance formula, basically to calculate the distance between landmarker 8 and 4 and with that data an "if" statement will run to see what is considered "pinching" as a boolean value 'T'

However, the issue of repetitive pinching may arise so I added a cooldown:

```python
last_pinch_time = 0
cooldown = 1.0 
is_pinching = False
current_time = time.time()
if current_time - last_pinch_time > cooldown:
     last_pinch_time = current_time
```

Additionally, there has to be a linkage between my python code and my ESP32, so we use 

```python
import serial

ser = serial.Serial('/dev/tty.usbserial-0001', 9600, timeout=1)
```

If the distance in less than 40, then: 

```python
          if not is_pinching and current_time - last_pinch_time > cooldown:
               is_pinching = True
               last_pinch_time = current_time
               ser.write(b'T')
               print(f"Pinch detected! Distance: {distance:.1f}")
```

We'll send a boolean value over to the ESP32 and reset the cooldown.

The first inititative I took in order to construct the hand was to 3D model it on Fusion360. 
