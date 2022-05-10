#!/usr/bin/env python3

from DotSim import DotSim
import math

d1 = DotSim(10,10)
d2 = DotSim(10, 10)

print(f"Dot 1: ({d1.getX()},{d1.getY()})")
print(f"Dot 2: ({d2.getX()},{d2.getY()})")

angle = 90 - math.degrees(math.atan2(d2.getY() - d1.getY(),d2.getX() - d1.getX()))

print(angle)