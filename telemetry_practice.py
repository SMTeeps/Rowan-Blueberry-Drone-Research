#!/usr/bin/env python3

import asyncio
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)

async def run():

    drone = System()
    await drone.connect(system_address="udp://:14540")

    asyncio.ensure_future(check_alt(drone))

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
    
    print("-- Go 0m North, 0m East, 50m Up within local coordinate system")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -50.0, 0.0))

    await asyncio.sleep(10)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")
    

async def check_alt(drone):
    async for pos in drone.telemetry.position():
        if(pos.relative_altitude_m >= 5):
            print(pos.relative_altitude_m)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())