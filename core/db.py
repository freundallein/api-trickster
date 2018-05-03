# -*- coding: utf-8 -*-
from core.db_drivers import MongoDriver, PostgresDriver


class DBImproperlyConfigured(Exception):
    pass


def get_db_connection(app):
    supported_dbs = {
        'mongo': MongoDriver,
        'postgres': PostgresDriver
    }
    database = app['config'].get('db')
    try:
        driver = supported_dbs.get(database)
        db = driver(app)
        cleanup = db.get_cleanup()
        return db, cleanup
    except Exception as error:
        raise DBImproperlyConfigured(
            f"[{error}]: Only Mongo and Postgres supported, check settings.")
