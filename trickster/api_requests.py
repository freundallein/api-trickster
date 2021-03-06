# -*- coding: utf-8 -*-

from trickster.utils import (generate_arrivals_url, aggregate_lines_by_20,
                             generate_stops_url)

__all__ = (
    'obtain_buses',
    'obtain_stops',
    'obtain_arrivals'
)


async def obtain_buses(session, service_url, auth_params):
    api_url = f"{service_url}/Line/Mode/bus?{auth_params}"
    try:
        async with session.get(api_url) as resp:
            print("Buses")
            print(resp.status)
            buses = await resp.json()
            return buses
    except Exception as err:
        print("Buses")
        print(err)
        raise err


async def obtain_stops(session, service_url, auth_params, lines):
    try:
        async for api_url, line in generate_stops_url(lines, service_url,
                                                  auth_params):
            async with session.get(api_url) as resp:
                print("Stops")
                print(resp.status)
                stops = await resp.json()
                yield stops, line
    except Exception as err:
        print("Stops")
        print(err)
        raise err


async def obtain_arrivals(session, service_url, auth_params, lines):
    lines = await aggregate_lines_by_20(lines)
    try:
        async for api_url, buses in generate_arrivals_url(lines, service_url,
                                                          auth_params):
            # print(f"Arrivals for: {buses}")
            async with session.get(api_url) as resp:
                print("Arrivals")
                print(resp.status)
                arrivals = await resp.json()
                yield arrivals, buses
    except Exception as err:
        print("Arrivals")
        print(err)
        raise err
