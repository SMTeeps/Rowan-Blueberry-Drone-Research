#!/usr/bin/env python3
import random

import asyncio
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw, VelocityBodyYawspeed, PositionGlobalYaw)

async def run():

    drone = System()
    await drone.connect(system_address="udp://:14540")

    #asyncio.ensure_future(check_heading(drone))

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

    x = random.randint(-25, 25)
    y = random.randint(-25, 25)

    print("-- Go to (%s, %s)" %(x,y))
    await drone.offboard.set_position_ned(PositionNedYaw(x, y, -15.0, 0.0))
    await asyncio.sleep(10)
    
    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")


    # Point drone north
    # async for heading in drone.telemetry.heading():
    #     if(heading.heading_deg > 0):
    #         await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, -.1))
    #     if(heading.heading_deg < 0):
    #       await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, .1))
    
    

async def check_heading(drone):
    async for pos in drone.telemetry.heading():
        print(pos.heading_deg)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())