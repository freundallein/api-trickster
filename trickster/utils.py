# -*- coding: utf-8 -*-
import asyncio


def create_auth_query_string(app_id, app_key):
    return f"app_id={app_id}&app_key={app_key}"


async def parse_buses(buses):
    parsed_buses = []
    for bus in buses:
        await asyncio.sleep(0)
        parsed_buses.append({'id': bus.get('id'),
                             'type': bus.get('modeName'),
                             'number': bus.get('name')})
    return parsed_buses


def parse_lines(lines):
    return [line.get('id') for line in lines]


async def parse_stops(stops, line):
    stops = stops.get('stations')
    parsed_stops = []
    for stop in stops:
        await asyncio.sleep(0)
        parsed_stops.append({
            'line': line,
            'id': stop.get('id'),
            'station_id': stop.get('stationId'),
            'station_name': stop.get('name'),
            'lines': parse_lines(stop.get('lines')),
            'lat': stop.get('lat'),
            'lon': stop.get('lon')
        })
    return parsed_stops


async def parse_arrivals(arrivals):
    parsed_arrivals = []
    for arrival in arrivals:
        await asyncio.sleep(0)
        if arrival.get('stationName') is None:
            print(arrival)
        parsed_arrivals.append({
            'station_name': arrival.get('stationName'),
            'direction': arrival.get('direction'),
            'vehicle_id': arrival.get('vehicleId'),
            'destination': arrival.get('destinationName'),
            'expected': arrival.get('expectedArrival'),
            'line_id': arrival.get('lineId'),
            'line_name': arrival.get('lineName')
        })
    return parsed_arrivals


async def aggregate_lines_by_20(lines):
    AMOUNT = 20
    result = []
    while lines:
        await asyncio.sleep(0)
        pack = lines[:AMOUNT]
        lines = lines[AMOUNT:]
        result.append(pack)
    return result


async def generate_arrivals_url(lines, service, auth):
    for pack in lines:
        buses = ",".join(pack)
        yield f"{service}/Line/{buses}/Arrivals?direction=all&{auth}", pack


async def generate_stops_url(lines, service, auth):
    for line in lines:
        yield f"{service}/Line/{line}/Route/Sequence/all?{auth}", line
