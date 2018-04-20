# -*- coding: utf-8 -*-
import datetime
import asyncio
from trickster.api_requests import *
from trickster.utils import parse_buses, parse_stops, parse_arrivals
from trickster.db import update_buses, update_stops, update_arrivals

__all__ = (
    'aggregate_buses_and_stops'
)


async def aggregate_buses_and_stops(db, session, service_url, auth_params,
                                    scheduled):
    forced = False
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
        await update_buses(db, buses)
    except Exception as err:
        print(err)


async def process_stops(db, session, service_url, auth_params):
    try:
        print('processing stops')
        all_lines = [bus['id'] async for bus in db.buses.find()]
        async for stops, line in obtain_stops(session, service_url,
                                              auth_params, all_lines):
            stops = await parse_stops(stops, line)
            await update_stops(db, line, stops)
    except Exception as err:
        print(err)


async def process_arrivals(db, session, service_url, auth_params, interval):
    while True:
        try:
            print('processing arrivals')
            all_lines = [bus['id'] async for bus in db.buses.find()]
            async for arrivals, lines in obtain_arrivals(session, service_url,
                                                         auth_params,
                                                         all_lines):
                arrivals = await parse_arrivals(arrivals)
                await update_arrivals(db, lines, arrivals)
            await asyncio.sleep(interval)
        except Exception as err:
            print(err)
