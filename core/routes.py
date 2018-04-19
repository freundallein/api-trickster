# -*- coding: utf-8 -*-
from core.handlers import index
from api.v1.handlers import get_buses, get_bus_stops, get_arrivals

routes = [
    ('GET', '/', index),
    ('GET', '/api/v1/buses', get_buses),
    ('GET', '/api/v1/stops/{line_id}', get_bus_stops),
    ('GET', '/api/v1/arrivals/{line_id}/{station_name}', get_arrivals),
]
