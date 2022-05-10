#!/usr/bin/env python3

from DotSim import DotSim
import math

import asyncio
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw, VelocityBodyYawspeed, PositionGlobalYaw, Attitude)

async def run():

    drone = System()
    await drone.connect(system_address="udp://:14540")

    ds = DotSim(100,100)

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

    print("-- Go 0m North, 0m East, 25m Up within local coordinate system")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -25.0, 0.0))
    await asyncio.sleep(20)

    angle = math.degrees(math.atan2(ds.getY(), ds.getX()))

    angle = 90 - angle

    print(f"-- Turn to face {ds.getY()}N, {ds.getX()}E")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -25.0, angle))
    await asyncio.sleep(10) 

    print("-- Start moving 2m/s forward")
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(2.0, 0.0, 0.0, 0.0)) 

    async for pos in drone.telemetry.position_velocity_ned():
        if int(pos.position.north_m) == ds.getY() and int(pos.position.east_m) == ds.getX():
            print(f"-- Destination reached. Current pos: {pos.position.north_m}N, {pos.position.east_m}E")
            print("-- Descend to 10m")
            await drone.offboard.set_position_ned(PositionNedYaw(pos.position.north_m, pos.position.east_m, -10.0, 0.0))
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