# Assembly Guide

## Parts:
- Front/Back Shell for Pip-Boy
- 4.5 in Display
- 1 Raspberry Pi Zero 2 W
- 3 analog buttons
- ~24 jumper cables
- 3 10 Ohm resistors
- 3 220 Ohm resistors
- 1 rotary encoders
- ~ 5-6 popsicle sticks
- 2 small hinges
- Superglue
- Flat Angled HMDI cable
- Flat angled micro b usb cable
- Small Breadboard

## Instructions:
- Start by soldering the pin stack onto the raspberry pi.
![](/img/solder1.jpeg)
![](/img/solder2.jpeg)

- Wire up 3 buttons for your navigation:
![](/img/bread.jpeg)

- Wire up rotary encoder and connect directly to raspberry pi. Ground and Power can go to the breadboard.

- Assemble Shell.
    - I user a popsicle stick as a spacer between the shell and the hinges on both sides. 
    ![](/img/hinge.jpeg)
    - You can use screws, but superglue proved successful as the support structure either cracks or can't maintain the threading of a screw because of the support structure. 

- Assemble screen frame:
    - Make a rectangular frame out of popsicle sticks that fits around your display
    ![](/img/frame.jpeg)
    - Use superglue to connect the frame to the inside of the shell

- Start inner assembly:
    - After messing around with it for a long time, I couldn't find a reliable way to connect the raspberry pie to the inside of the shell
    - Screen should slot in nicely. If it doesn't, trim down the edges of the frame. 
    - Use the sticky side of the breadboard to connect to the back of the display.
    - Since the shell is rather restrictive, I was not able to fit the buttons through the typical holes. I improvised and routed the up next to the screen.
    - Similarly, since the crame was restrictive, I was only able to attach the rotary encoder to the side by routing it through another hole in the frame. I mounted it with superglue.
    - Power was another issue. The battery I bought could not handle the screen and the Pie, and the power amplifier I found in discovery was sold out / alternatives were way more expensive, and I already spent too much money on this thing. 
