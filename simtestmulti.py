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

    for i in range(len(dots)):
        print(f"-- Turn to face {dots[i].getY()}N, {dots[i].getX()}E")
        if i == 0:
            angle = 90 - math.degrees(math.atan2(dots[0].getY(), dots[0].getX()))
        else:
            angle = 90 - math.degrees(math.atan2(dots[i].getY() - dots[i-1].getY(), dots[i].getX() - dots[i-1].getX()))
        await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, angle))
        await asyncio.sleep(5) 
        print("-- Start moving 2m/s forward")
        await drone.offboard.set_velocity_body(VelocityBodyYawspeed(2.0, 0.0, 0.0, 0.0)) 
        async for pos in drone.telemetry.position_velocity_ned():
            if (dots[i].getY()-1.5 <= pos.position.north_m <= dots[i].getY()+1.5) and (dots[i].getX()-1.5 <= pos.position.east_m <= dots[i].getX()+1.5):
                print(f"-- Destination reached. Current pos: {pos.position.north_m}N, {pos.position.east_m}E")
                break
    
    await asyncio.sleep(10)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())