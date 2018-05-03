# -*- coding: utf-8 -*-
from aiohttp import web
from core.handlers import handle_500


async def get_healthcheck(request):
    data = {"status": "OK"}
    return web.json_response(data)


async def get_buses(request):
    db = request.app['db']
    try:
        data = await db.get_buses()
        return web.json_response(data)
    except Exception as error:
        request.app.logger.error(error)
        return await handle_500(request, None)


async def get_bus_stops(request):
    try:
        line_id = request.match_info['line_id']
        db = request.app['db']
        data = await db.get_bus_stops(line_id)
        return web.json_response(data)
    except Exception as error:
        request.app.logger.error(error)
        return await handle_500(request, None)


async def get_arrivals(request):
    try:
        db = request.app['db']
        line_id = request.match_info['line_id']
        station_name = request.match_info['station_name']
        data = await db.get_arrivals(line_id, station_name)
        return web.json_response(data)
    except Exception as error:
        request.app.logger.error(error)
        return await handle_500(request, None)
