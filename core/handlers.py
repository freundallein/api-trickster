# -*- coding: utf-8 -*-
from aiohttp import web


async def index(request):
    data = {"message": "Welcome to Bus Proxy Server!"}
    return web.json_response(data)


async def handle_404(request, response):
    return web.HTTPFound('/')


async def handle_500(request, response):
    data = {"error": "Something goes wrong. Try again later."}
    return web.json_response(data)
