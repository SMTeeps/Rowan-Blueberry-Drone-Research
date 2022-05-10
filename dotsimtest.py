#!/usr/bin/env python3

from DotSim import DotSim
import math

d = DotSim(10,10)

print(d.getX())
print(d.getY())

ogangle = math.degrees(math.atan2(d.getY(),d.getX()))
angle = ogangle % 360

# if(d.getX() < 0 and d.getY() > 0):
#     angle = angle - 180
# elif(d.getX() > 0 and d.getY() < 0):
#     angle = angle + 180

print(90 - ogangle)
print(90 - angle)