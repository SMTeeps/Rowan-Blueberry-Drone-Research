#!/usr/bin/env python3

from DotSim import DotSim
import math

import asyncio
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw, VelocityBodyYawspeed, VelocityNedYaw)

async def run():

    drone = System()
    await drone.connect(system_address="udp://:14540")

    dots = [DotSim(100,100),DotSim(100,100),DotSim(100,100),DotSim(100,100),DotSim(100,100),DotSim(100,100),DotSim(100,100),DotSim(100,100),DotSim(100,100),DotSim(100,100)]

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        await drone.action.disarm()
        return

    print("-- Go 0m North, 0m East, 10m Up within local coordinate system")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -10.0, 0.0))
    await asyncio.sleep(10)

    tempY = 0
    tempX = 0

    # distance = 999
    for dot in dots:
        print(f"-- Turn to face {dot.getY()}N, {dot.getX()}E")
        angle = 90 - math.degrees(math.atan2(dot.getY() - tempY, dot.getX() - tempX))
        await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, angle))
        await asyncio.sleep(8) 

        async for pos in drone.telemetry.position_velocity_ned():
            # prevDist = distance
            distance = math.sqrt((dot.getX()-pos.position.east_m)**2+(dot.getY()-pos.position.north_m)**2)
            if distance > 20:
                speed = 4.0
            elif distance > 10:
                speed = 2.0
            else:
                speed = 1.0

            # print(distance > prevDist)
            # if (distance > prevDist):
            #     angle = 90 - math.degrees(math.atan2(dot.getY() - tempY, dot.getX() - tempX))
            #     await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, angle))
            #     await asyncio.sleep(5) 

            # angle2 = 90 - math.degrees(math.atan2(dot.getY() - pos.position.north_m, dot.getX() - pos.position.east_m))
            # print(angle2 - angle)
            # if abs(angle2 - angle > 1):
            #     print("angle adjusted")
            #     await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, angle2))
            #     await asyncio.sleep(5)
            #     angle = angle2

            #print(f"Moving {speed} m/s")
            await drone.offboard.set_velocity_body(VelocityBodyYawspeed(speed, 0.0, 0.0, 0.0))

            #print(distance)
            if distance < 3:
            #if (dot.getY()-2 <= pos.position.north_m <= dot.getY()+2) and (dot.getX()-2 <= pos.position.east_m <= dot.getX()+2):
                print(f"-- Destination reached. Current pos: {pos.position.north_m}N, {pos.position.east_m}E")
                await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
                await asyncio.sleep(3)
                tempY = pos.position.north_m
                tempX = pos.position.east_m
                break
    
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(10)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())