# -*- coding: utf-8 -*-
from motor.motor_asyncio import AsyncIOMotorClient


class DBImproperlyConfigured(Exception):
    pass


def get_db_connection(app):
    try:
        mongo_host = app['config']['mongo']['host']
        mongo_port = app['config']['mongo']['port']
        mongo_database = app['config']['mongo']['database']
        mongo_user = app['config']['mongo']['user']
        mongo_password = app['config']['mongo']['password']
    except Exception as err:
        raise DBImproperlyConfigured(
            f"Set mongo:{err} value in settings.yaml!"
        )
    credentials = f"{mongo_user}:{mongo_password}"
    dsn = f'mongodb://{credentials}@{mongo_host}:{mongo_port}/{mongo_database}'
    client = AsyncIOMotorClient(dsn)
    db = client[mongo_database]

    async def cleanup(app):
        client.close()

    return db, cleanup
