# -*- coding: utf-8 -*-
from trickster.utils import create_auth_query_string
from trickster.processing import aggregate_buses_and_stops, process_arrivals
from trickster.debug_processing import debug_aggregate_buses_and_stops, \
    debug_process_arrivals


def create_trickster(loop, app):
    db = app['db']

    constant_earner(app, db, loop=loop)


def constant_earner(app, db, loop=None):
    forced = bool(app['config']['forced'])
    debug = app['config']['debug']
    config = app['config']['tfl']
    service_url = config['service_url']
    app_id = config['application_id']
    app_key = config['application_key']
    bus_and_stop_schedule = config['bus_and_stops_update_time']
    arrivals_interval = config['arrivals_update_frequency']
    auth_params = create_auth_query_string(app_id, app_key)
    if debug:
        loop.create_task(debug_aggregate_buses_and_stops(db, service_url,
                                                         auth_params,
                                                         bus_and_stop_schedule,
                                                         forced))
        loop.create_task(debug_process_arrivals(db, service_url, auth_params,
                                                arrivals_interval))
    else:
        loop.create_task(aggregate_buses_and_stops(db, service_url,
                                                   auth_params,
                                                   bus_and_stop_schedule,
                                                   forced))
        loop.create_task(process_arrivals(db, service_url, auth_params,
                                          arrivals_interval))
