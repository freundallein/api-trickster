# -*- coding: utf-8 -*-
import datetime
import asyncio

import aiohttp

from trickster.api_requests import *
from trickster.utils import parse_buses, parse_stops, parse_arrivals


__all__ = (
    'aggregate_buses_and_stops'
)


async def aggregate_buses_and_stops(db, service_url, auth_params,
                                    scheduled, forced):
    forced = bool(forced)
    async with aiohttp.ClientSession() as session:
        while True:
            now = datetime.datetime.now().strftime('%H:%M')
            if scheduled == now or forced:
                forced = False
                await process_buses(db, session, service_url, auth_params)
                await process_stops(db, session, service_url, auth_params)
            await asyncio.sleep(1)


async def process_buses(db, session, service_url, auth_params):
    try:
        print('processing buses')
        buses = await obtain_buses(session, service_url, auth_params)
        buses = await parse_buses(buses)
        await db.update_buses(buses)
    except Exception as err:
        print(err)


async def process_stops(db, session, service_url, auth_params):
    try:
        print('processing stops')
        all_lines = await db.get_all_lines()
        async for stops, line in obtain_stops(session, service_url,
                                              auth_params, all_lines):
            stops = await parse_stops(stops, line)
            await db.update_bus_stops(line, stops)
    except Exception as err:
        print(err)


async def process_arrivals(db, service_url, auth_params, interval):
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                print('processing arrivals')
                all_lines = await db.get_all_lines()
                async for arrivals, lines in obtain_arrivals(session,
                                                             service_url,
                                                             auth_params,
                                                             all_lines):
                    arrivals = await parse_arrivals(arrivals)
                    await db.update_arrivals(lines, arrivals)
                await asyncio.sleep(interval)
            except Exception as err:
                print(err)
