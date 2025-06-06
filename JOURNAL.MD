---
title: "Cubert"
author: "Mohit Srinivasan and Alex Masin"
description: "A fully custom Rubik's cube solver!"
created_at: "2025-05-26"
---

### Total Time Spent
- Mohit: 10h
- Alex: 8.5h

# Day 1&2: Mohit
Hi everyone, this is where I'll be documenting the software aspect of the Cubert project. My name is Mohit and I'm excited to begin this project. The following content is the barebones software implementation for our project.

## Software Overview
The plan right now for the rubik's cube solver is that the user will upload images of all 6 faces of the cube to an app, and the app will convey this information to either a Raspberry Pi or an ESP32 which will algorithmically solve the rubik's cube. This idea is rooted in the basis that the center blocks of rubik's cubes do not change. To that end, we can ask the user to upload an image of the yellow side, the white side, the green side, etc. After the user uploads this image, we will send it up to AWS Rekognition which will run an image recognition model/CV that we can use to identify the images. I plan on converting this image data using like an AWS Lambda function to a text representation like using JSON or something, and then upload that back to the user. The user will then be uploading this text representation directly to the RPI which will compute the moves to solve the cube. Initially, I had a plan to keep all of the image recognition, etc. running on the RPI but realized how slow this actually is and decided to bring that part up to the cloud. We can also have a 3D Rubik's cube we display on the app for users that don't want to upload images, and instead they can just paint the cube with colors instead of actually taking images.

## Rough Excalidraw Diagram
<img width="1201" alt="image" src="https://github.com/user-attachments/assets/2ae406ea-b957-4250-a2fe-972f384ba253" />

## Code setup
I have the starter code setup in the repository. I am currently on vacation, hence I don't have access to my hardware. So, I have setup an ESP32 Simulation using Wokwi and PlatformIO. The code consists of a Turborepo monorepo management system which has an app called `mobile`. This `mobile` app inside Turborepo will contain all of the code for the mobile app. The current plan is to have the mobile app built using React Native and Expo, however I might change this if I run into some annoying issues and move to Flutter instead. I want to stay as far away from custom building apps for both Android and iOS and would love to just use a phone-agnostic library like Flutter or React Native.

### Time Spent: 1.5 hours

# Day 1&2: Alex

Hey all, this is where I'll be documenting my progress on the design/fabrication portion of the build. My name is Alex, and I am really excited to get started! 

Below is the rough proposal for the mechanical aspect of the build. This was the first step of the planning and is obviously very vague. But, here it is, to give you some context: 

## Design Process Overview

### Structure
Lightweight PLA 3D printed see-through web-design cage encompasses the rubik's cube, with a hole in the center of each face for where the servo motors will go.
There will be an armature piece on each face that directly connects from the servo output to the centerpiece of the rubik's cube face, either completely replacing the center piece or encompassing the center piece

### Unique Adapters
An adapter will be designed and fabricated for the servo output, as well as an adapter for the centerpiece on each rubik's cube face. Purdue ECE did it by creating new center pieces that mounted to the rubik’s cube and also could mount to the armature.

### Wire Routing
The cage will have sides to which all the wires will be fastened
### Potential issue(s)
The main issue I'm foreseeing with this design is figuring out the adapters and figuring out a way to make the rubik's cube easily removable from the cage.

## V0 Adapter 

The first step for me was to design a temporary adapter that would serve as the connection from the servos that spin each side to the actual face of the Rubik's Cube. I'm currently using the [Purdubiks machine](https://www.youtube.com/watch?v=sXxh6QuY2ew) as inspiration, with the idea being to create an adapter that directly interacts with the interior of the center dot. I'm using a random 3-D model of a speed cube for reference for now, as I don't actually own a Rubik's cube yet, but I'm really hoping that the kind person who modeled the cube modeled it true to life. Enough yap, this is what we're working with currently:

![Screenshot 2025-05-25 163858](https://github.com/user-attachments/assets/a73c0fb4-12dd-4813-bce7-11e36956350d)

Bear in mind, this is just meant to be a proof of concept to me that my idea works. This will become much more refined once more details are finalized. but this is what we have for now. 

### Total Time Spent: 2 Hrs 

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
# Day 3

Day 3 was an easier day - I did a few minor things and that's about it. 

## Making my life easier 
 I created a reference cube (a cube with a hole on each face) to use for modeling purposes, as the imported model was not actually mated together. Here it is: 
![Screenshot 2025-05-29 204005](https://github.com/user-attachments/assets/30fb55bc-3c6d-44c9-b175-394057e4eebb)

## Assembling the Assembly  
I also started making the assembly of the cube - servo - adapter. 
![image](https://github.com/user-attachments/assets/8ab7e622-47e1-4765-acda-60e57a2f94d7)

With a few simple steps, I replicated this subassembly on each side of the reference cube. 
![image](https://github.com/user-attachments/assets/523c432f-052d-4809-a68b-7369eb552f94)

I also oriented each servo so that the cables would come out facing the front face (or could at least be easily routed towards the front face).

One thing Mohit and I have been worrying about is the adapter blocking the view of the cameras. Still, for now, we decided we won't be worrying about cameras and will require the user to upload pictures of each face of the cube before putting it in the machine. Perhaps in later stages we will incorporate cameras that will detect the color of each dot of each face. 
### Total Time Spent: 1.5 hr 

# Day 4: Mohit
Day 4 was an important day. It marks the first day I started designing, and thinking about the electronics for Cubert.

## Initial Plans
As mentioned in the previous days, we decided to ditch our effort towards having cameras on the robot, and instead the user just takes pictures of all the faces of the cube and then sends it to the robot. This is much more cost-efficient, because we believe we can keep the project under $150 if we take this approach to it. 

## Creating a BOM
This is the day I created a rough BOM of the items we'd need and then mapping it to listings I found on AliExpress (the cheapest ones I could find of course).

![image](https://github.com/user-attachments/assets/601c4863-0975-4426-8490-7051c5d0a9e6)

This is super rough and I'm only including the main components right now. We're still going to need filament, jumper cables, resistors, etc. Additionally, we have plans to turn our power distribution logic into a PCB so we're going to need money to print them out.

### Time Spent: 1.5 hr

# Day 4 

Today was the second big day, as I committed myself to designing the frame today. 

## Making the Frame 
I didn't really know where to start, so as before, I turned to [Purdue](https://www.youtube.com/watch?v=sXxh6QuY2ew). They obviously design at a much better level than me, but I figured I could still take inspiration from them. I also looked at [Aed Musa's Design](https://www.youtube.com/watch?v=m0bMMALYMYk), and decided to go for a middle of the road approach. This is what I came up with: 
![image](https://github.com/user-attachments/assets/cde46132-eb48-46d5-9d96-2a636db10d73)

Now, there are several issues with this design, so let's go through them. 
### 1. It's asymmetrical in a weird way 
Because of the way the servo is with the shaft being at one end of the overall block, I had to make the servo mounts off-center which makes everything look slightly weird, and also messes with the geometry. No big deal here other than being annoying. 
### 2. There's no real design for getting the cube in/out 
This is what I'm most worried about, but I figured for the prototype version I will just print the frame as is and wedge the Rubik's Cube in there. If my design concepts work, then I will redesign the frame to actually be user-friendly.
### 3. Bad visibility 
Mohit was complaining hard about this one, so I just got rid of the sides. All better now! 
![image](https://github.com/user-attachments/assets/37a8fb05-ebbe-42f0-ac41-173191252f40)

### Final Touches 
I added a base, so the frame has something to stand on, and before I print it (more on that later) I'll be adding bolt/ziptie holes for the servo mounting. 

I'm going to admit, this frame isn't perfect, but it will (hopefully) do exactly what I need it to do, which is being a proof of concept.

This is what the full assembly currently looks like: 

![image](https://github.com/user-attachments/assets/959015d0-4dee-4590-a7bb-d51105670947)


### Time Spent : 2 Hrs
 
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

# Day 5: Alex
Today is the day I finally got to printing parts of the project. 

## The Plan and Setup 
The first thing I wanted to verify was the dimensions of the adapter and make sure it actually interfaced properly with the cube. This was the scariest part, as I was finally going to have to test the trustworthiness of that random CAD model. Additionally, my current setup is a stock Prusa i3 MK3S+ with SUNLU Black PLA, and I use PrusaSlicer to slice all my files. 


## Printing the V0 adapter: First attempt
For this first one, I was foolish enough to think that it was going to work off the first attempt, so I printed it at 100% infill. It took roughly 3-4 hours to print, and was more or less a wasted time - 0-10% infill takes 1-1.5hrs. 
Here it is: 
![1000009309](https://github.com/user-attachments/assets/3d6a93b9-3460-4a98-9c29-e46c511e80a4)

## Printing the V0 adapter: Second attempt
The problem with the previous adapter is that the Rubik's end was too small in width, so for this one, I increased the width by 2mm to exactly match the size of the CAD model (it seems that the CAD model lines up with the GAN cube dimensions). I printed this one only at 5% infill, and it only took 1.5 hrs. As I probably should have expected, this one is about half a millimeter too big: 
![1000009308](https://github.com/user-attachments/assets/bcc5134f-8bc4-4d4d-92d3-7dfd4ccbcf09)

## Getting smarter: Third attempt 
This time, instead of printing the entire adapter, I only printed the end bit. I ended up sizing down the width by 0.5 millimeters, and it fit perfectly! 

![1000009312](https://github.com/user-attachments/assets/bce6c2ba-8824-47e2-9810-1134d0f7d649)

## V0 FINALIZED 
Alright, I finally printed the V0 adapter with the right sizing. I kept the infill low, _just in case_. Nothing to add, it fits perfectly, and is ready for further prototyping! 
![1000009311](https://github.com/user-attachments/assets/db7be04d-a331-418a-906a-b3b60b0edcfa)

That's a wrap for today, next day will involve more prototyping! 

### Time Spent: 1.5 Hours 



# Day 6: Mohit
I decided that it would be much better to add an SSD1306 to the schematics and electronics to make it more visual. It would be nice for the user to see like updates on the actual Cubert machine itself on if their app is connected, and if it's receiving the data and stuff (similar to a printer). So, I added an SSD1306.

![image](https://github.com/user-attachments/assets/c05b9042-1224-43b7-a257-fa54af163b9d)

One main issue is that the Raspberry Pi 3.3V output goes to the logic for the PCA9685 and we need another 3.3V port for the SSD1306. So a solution IRL would be to splice the wire, or we could have a 5V port and have a voltage regulator that steps down 5V to 3.3V for the SSD1306. Everything else is fine, but that's the only big issue.

### Time spent: 0.5h
