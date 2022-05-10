#!/usr/bin/env python3

from DotSim import DotSim
import math

import asyncio
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw, VelocityBodyYawspeed, PositionGlobalYaw)

async def run():

    drone = System()
    await drone.connect(system_address="udp://:14540")

    ds = DotSim(200,200)

    #asyncio.ensure_future(check_velocity(drone))

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

    angle = math.degrees(math.atan2(ds.getY(), ds.getX()))
    print(ds.getX())
    print(ds.getY())

    if(ds.getX() < 0 and ds.getY() > 0):
        angle = angle - 180
    elif(ds.getX() > 0 and ds.getY() < 0):
        angle = angle + 180

    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -10.0, angle))
    await asyncio.sleep(10)

    #while abs(ds.getX()) > .5 and abs(ds.getY()) > .5:
        
    
    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")
        

async def check_velocity(drone):
    async for v in drone.telemetry.velocity_ned():
        print(v.down_m_s)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())