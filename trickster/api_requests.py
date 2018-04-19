# -*- coding: utf-8 -*-
import json
import asyncio
from trickster.utils import (generate_arrivals_url, aggregate_lines_by_20,
                             generate_stops_url)

__all__ = (
    'obtain_buses',
    'obtain_stops',
    'obtain_arrivals'
)


async def obtain_buses(session, service_url, auth_params):
    # api_url = f"{service_url}/Line/Mode/bus?{auth_params}"
    # async with session.get(api_url) as resp:
    #     print(resp.status)
    #     # print(await resp.json())
    with open('test_fixtures/buses.json', 'r') as file:
        json_response = file.read()
        try:
            buses = json.loads(json_response)
            return buses
        except Exception as err:
            print(err)
            raise err


async def obtain_stops(session, service_url, auth_params, lines):
    async for api_url, line in generate_stops_url(lines, service_url,
                                                   auth_params):
        # print(api_url)
        print(f"Stops for: {line}")
        await asyncio.sleep(1)
    #     async with session.get(api_url) as resp:
    #         print(resp.status)
    #         print(await resp.text())
    #         await asyncio.sleep(1)
        with open('test_fixtures/stops.json', 'r') as file:
            json_response = file.read()
            try:
                stops = json.loads(json_response)
                # line = '134'
                yield stops, line
            except Exception as err:
                print(err)
                raise err


async def obtain_arrivals(session, service_url, auth_params, lines):
    lines = await aggregate_lines_by_20(lines)
    async for api_url, buses in generate_arrivals_url(lines, service_url,
                                                      auth_params):
        print(f"Arrivals for: {buses}")
        await asyncio.sleep(1)
    #     print(buses)
    #     async with session.get(api_url) as resp:
    #         print(resp.status)
    #         print(await resp.text())
    #         await asyncio.sleep(1)
        with open('test_fixtures/arrivals.json', 'r') as file:
            json_response = file.read()
            try:
                arrivals = json.loads(json_response)
                buses = ['134', '135', '136']
                yield arrivals, buses
            except Exception as err:
                print(err)
                raise err
