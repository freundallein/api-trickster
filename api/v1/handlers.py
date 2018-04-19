# -*- coding: utf-8 -*-
from aiohttp import web
from core.handlers import handle_500


async def get_buses(request):
    db = request.app['db']
    try:
        cursor = db.buses.find()
        data = [
            {'id': bus['id'], 'number': bus['number']} async for bus in cursor
        ]
        return web.json_response(data)
    except Exception as error:
        request.app.logger.error(error)
        return await handle_500(request, None)


async def get_bus_stops(request):
    try:
        line_id = request.match_info['line_id']
        db = request.app['db']
        records = db.stops \
            .find({'line': line_id}) \
            .sort([("station_name", 1)])
        data = [
            {'id': stop['station_id'],
             'line': stop['line'],
             'name': stop['station_name']} async for stop in records
        ]
        return web.json_response(data)
    except Exception as error:
        request.app.logger.error(error)
        return await handle_500(request, None)


async def get_arrivals(request):
    try:
        db = request.app['db']
        line_id = request.match_info['line_id']
        station_name = request.match_info['station_name']
        records = db.arrivals \
            .find({'line_id': line_id, 'station_name': station_name}) \
            .sort([("expected", 1)])
        data = [
            {'line': arrival['line'],
             'station_name': arrival['station_name'],
             'direction': arrival['direction'],
             'destination': arrival['destination'],
             'arrival': arrival['expected']} async for arrival in records
        ]
        return web.json_response(data)
    except Exception as error:
        request.app.logger.error(error)
        return await handle_500(request, None)
