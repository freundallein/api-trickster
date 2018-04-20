# -*- coding: utf-8 -*-
import aiohttp
from trickster.utils import create_auth_query_string
from trickster.processing import aggregate_buses_and_stops, process_arrivals


def create_trickster(loop, app):
    db = app['db']
    config = app['config']['tfl']
    constant_earner(config, db, loop=loop)


def constant_earner(config, db, loop=None):
    service_url = config['service_url']
    app_id = config['application_id']
    app_key = config['application_key']
    bus_and_stop_schedule = config['bus_and_stops_update_time']
    arrivals_interval = config['arrivals_update_frequency']
    auth_params = create_auth_query_string(app_id, app_key)
    loop.create_task(aggregate_buses_and_stops(db, service_url, auth_params,
                                               bus_and_stop_schedule))
    loop.create_task(process_arrivals(db, service_url, auth_params,
                                      arrivals_interval))
