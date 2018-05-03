# -*- coding: utf-8 -*-
import asyncio
import datetime

from aiohttp import web

from core.utils import (configure_app, configure_db, setup_routes,
                        setup_middlewares, configure_logging)

from trickster.client import create_trickster


def init_app(loop):
    # Setup application and extensions
    app = web.Application(loop=loop)
    app = configure_app(app)
    app = configure_db(app)
    app = setup_routes(app)
    app = setup_middlewares(app)
    return app


def create_server(loop, app):
    handler = app.make_handler()
    host = app['config']['host']
    port = app['config']['port']
    http_server = loop.create_server(handler, host, port)
    loop.create_task(http_server)
    now = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    start_message = f"Start serving on {host}:{port} at {now}"
    print(start_message)
    app.logger.info(start_message)


def main():
    loop = asyncio.get_event_loop()
    app = init_app(loop)
    configure_logging(app['config']['logging'])
    server_only = bool(app['config']['server_only'])
    if not server_only:
        create_trickster(loop, app)
    create_server(loop, app)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
