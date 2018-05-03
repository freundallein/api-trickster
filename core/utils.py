# -*- coding: utf-8 -*-
import pathlib
import yaml
import logging

from core.db import get_db_connection
from core.routes import routes
from core.middlewares import error_pages
from core.handlers import handle_404, handle_500


def read_configuration():
    path = str(pathlib.Path('.') / 'config' / 'settings.yaml')
    with open(path, 'r') as stream:
        config = yaml.load(stream)
    return config


def configure_app(app):
    app['config'] = read_configuration()
    return app


def configure_db(app):
    try:
        db, cleanup = get_db_connection(app)
    except Exception as err:
        app.logger.error(f"[{err.__class__.__name__}]: {err}")
        raise err

    app['db'] = db
    app.on_cleanup.append(cleanup)
    return app


def setup_routes(app):
    for route in routes:
        app.router.add_route(route[0], route[1], route[2])
    return app


def setup_middlewares(app):
    error_middleware = error_pages({404: handle_404,
                                    500: handle_500})
    app.middlewares.append(error_middleware)
    return app


def configure_logging(app_config):
    filename = app_config['filename']
    level = getattr(logging, app_config['level'])
    format = app_config['format']
    datefmt = app_config['datefmt']
    logging.basicConfig(filename=filename,
                        level=level,
                        format=format,
                        datefmt=datefmt)
