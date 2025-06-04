---
title: "Cubert"
author: "Mohit Srinivasan and Alex Masin"
description: "A fully custom Rubik's cube solver!"
created_at: "2025-05-26"
---

# Day 1&2: Mohit
Hi everyone, this is where I'll be documenting the software aspect of the Cubert project. My name is Mohit and I'm excited to begin this project. The following content is the barebones software implementation for our project.

# Software Overview
The plan right now for the rubik's cube solver is that the user will upload images of all 6 faces of the cube to an app, and the app will convey this information to either a Raspberry Pi or an ESP32 which will algorithmically solve the rubik's cube. This idea is rooted in the basis that the center blocks of rubik's cubes do not change. To that end, we can ask the user to upload an image of the yellow side, the white side, the green side, etc. After the user uploads this image, we will send it up to AWS Rekognition which will run an image recognition model/CV that we can use to identify the images. I plan on converting this image data using like an AWS Lambda function to a text representation like using JSON or something, and then upload that back to the user. The user will then be uploading this text representation directly to the RPI which will compute the moves to solve the cube. Initially, I had a plan to keep all of the image recognition, etc. running on the RPI but realized how slow this actually is and decided to bring that part up to the cloud. We can also have a 3D Rubik's cube we display on the app for users that don't want to upload images, and instead they can just paint the cube with colors instead of actually taking images.

## Rough Excalidraw Diagram
<img width="1201" alt="image" src="https://github.com/user-attachments/assets/2ae406ea-b957-4250-a2fe-972f384ba253" />

## Code setup
I have the starter code setup in the repository. I am currently on vacation, hence I don't have access to my hardware. So, I have setup an ESP32 Simulation using Wokwi and PlatformIO. The code consists of a Turborepo monorepo management system which has an app called `mobile`. This `mobile` app inside Turborepo will contain all of the code for the mobile app. The current plan is to have the mobile app built using React Native and Expo, however I might change this if I run into some annoying issues and move to Flutter instead. I want to stay as far away from custom building apps for both Android and iOS and would love to just use a phone-agnostic library like Flutter or React Native.

### Time Spent: 1.5 hours

# Day 3: Mohit

Day 3 was the day where I started working on coding the vision aspect of the project. As I said earlier, I was initially planning on making it a mobile app using React Native or Flutter. I said that if React Native got annoying, I'd switch to Flutter. I changed my mind again. The final revision of the app will be.... **a Next.js app!**

The reason I made the switch is because a mobile app is overkill for the purpose of this project, and we just need the UI and the app to be barebones. As in the future we plan on turning this into a $350 project by possibly adding cameras (not confirmed). And, if we do decide to do that, a mobile app is quite pointless (boo overengineering 👎). 

## How vision works
So the vision code analyzes images of each face to find out its colors. First, an image of a single face is loaded, then its resized (to be consistent), and then it's converted from BGR to HSV (Hue, Saturation, Value) color space (this works quite better for color detection). I then apply a Gaussian blur to reduce any noise that might be present on the image. I then create a segmentation mask using predefined HSV thresholds (should be found inside `config.py`) and this isolates the background from the cube. There are other morphological operations that are at play that make the mask more clearer and better quality. So given that mask, the largest contour, is assumed to be the face of the cube, and is identified and approximated to a polygon. The area is then divided into a 3x3 grid and I map smaller ROIs (regions of interest) and define them within each of the 9 sticker areas. For each of the sampling ROI, I calculate the average HSV value. That avg HSV value tuple is compared against some other predefined HSV ranges (defined in the config) to determine the right color character (ex. `W` for white, `R` for red). Then the detected colors for each sticker are then put together into a 3x3 grid representing the face and then I repeat that same process to build a cube string (filled with the entire cube state). Throughout the entire thing I can run debug visualizations to make my life much easier.

## Why I moved away from AI?
At the beginning I started thinking of using AWS Rekognition for image recognition. However, I believe this is actual over-engineering and that a Raspberry Pi should be able to run moderate vision algos (like the one mentioned above) quite fast. Having everything locally would mean that the machine can run without a steady internet connection. 

## How can I improve this in the future?
I believe i can make the color detection more robust if instead of relying on predefined HSV thresholds, I can have some sort of automatic color calibration routine. Like the user can present each face's center sticker to the camera under their current lighting conditions & the system can learn the appropriate HSV ranges for each color. This is the closest I can get to actually using a machine learning model, but that's overkill. 

I can also probably improve the geometric analysis of the cube. Right now the system relies on finding the largest contour and then fitting a 3x3 grid to its bounding box. This can be less accurate if the cube is held at an angle which can lead to some kind of distortion. I guess in the future I can implement perspective correction based on the detected contour's shape (ex. by finding the 4 corner points of the face if it's sufficiently quadrilateral) before actually defining the sticker ROIs. There are some more advanced techniques, but I'm lowk just too dumb to figure them out.

The end solution to making everything work around 100% of the time would be to use a machine learning model like YOLO or SSD. This would remove all the tedious steps of contouring everything, making the grid, and the sampling all the ROIs individually. I think it would simplify the pipeline, but it's kinda overkill (idk my mind might change in the future after doing some electronics).

### Time spent: 3h

# Day 4: Mohit
Day 4 was an important day. It marks the first day I started designing, and thinking about the electronics for Cubert.

## Initial Plans
As mentioned in the previous days, we decided to ditch our effort towards having cameras on the robot, and instead the user just takes pictures of all the faces of the cube and then sends it to the robot. This is much more cost-efficient, because we believe we can keep the project under $150 if we take this approach to it. 

## Creating a BOM
This is the day I created a rough BOM of the items we'd need and then mapping it to listings I found on AliExpress (the cheapest ones I could find of course).

![image](https://github.com/user-attachments/assets/601c4863-0975-4426-8490-7051c5d0a9e6)

This is super rough and I'm only including the main components right now. We're still going to need filament, jumper cables, resistors, etc. Additionally, we have plans to turn our power distribution logic into a PCB so we're going to need money to print them out.

### Time Spent: 1.5 hr

# Day 5: Mohit

This is the biggest day in our project so far. This is the day I designed out the entire electronics. 

## Schematic
![image](https://github.com/user-attachments/assets/3808c597-f5b4-4caa-8fb9-885e0c2d6264)

## How this will work
The plan for the electronics is that we will have a 6V10A adapter that plugs into a wall. The Raspberry Pi requires 5V to run. So, we can use a DC-DC Buck Converter (I added the one we need to the BOM from Day 4) to step down the 6V to 5V and feed it into the RPI. When doing this in person, we'd need to make sure that the VOUT actually is stepping down 5.0V - 5.1V using a multimeter but that's a thought for another day. We then take 6V directly from the adapter and feed it to the servos on the PCA9685 servo board. The servo board's logic is powered by the 3.3V port from the RPI directly. Then each of the servos is connected to their respective PWM, V+, and GND. 

## Our main challenge
The main challenge right now is figuring out how we're going to place all the electronics inside the machine without it looking disgusting. We're both horrible at wire management and hiding everything, so we'll see how it all works out. We want to get all of these designs submitted & get our funding approved so we can start building it immediately!

This took way longer than I'd like to admit because to do this first, I had to learn Kicad 💀 

### Time Spent: 4h
