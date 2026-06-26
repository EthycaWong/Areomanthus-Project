# Areomanthus-Project - By Ethan Wong
This repository consists of a hand detection system I made in Python that detects your hands using your built in computer camera, the 3D models for the designs of the parts printed, and also the overall code used as well as electronics.
The main purpose of this project is for an educational purpose while also to accomplish what I have seen rarely done.

As to begin my explanation for each step of the code and also their purpose, it's best to start with the design plan for the system.

# The Claw/Hand

The Claw/Hand of the arm will be it's primary purpose, which is to interact with it's surrounding environment when given the command.

For the electronics, I will be using an estimated amount of 2-3 ESP32 Developer Boards alongside approximately 10-20 SG90 Mirco Servos.
Essentially, the method in which the claw will operate will recive signals from a camera that detects the mapping of a hand and translate those movements to the SG90's.

