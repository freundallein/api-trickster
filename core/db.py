# -*- coding: utf-8 -*-
from motor.motor_asyncio import AsyncIOMotorClient


class DBImproperlyConfigured(Exception):
    pass


class MongoDriver:
    def __init__(self, app):
        self.dsn = self.make_dsn(app)
        self.database = self.get_database_name(app)
        self.client = self.init_client()
        self.cleanup = self.get_cleanup()
        self.db = self.get_db()

    def get_database_name(self, app):
        return app['config']['mongo']['database']

    def make_dsn(self, app):
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
        return dsn

    def init_client(self):
        client = AsyncIOMotorClient(self.dsn)
        return client

    def get_cleanup(self):
        client = self.client

        async def cleanup(app):
            client.close()

        return cleanup

    def get_db(self):
        db = self.client[self.database]
        return db

    async def get_buses(self):
        cursor = self.db.buses.find()
        data = [
            {'id': bus['id'], 'number': bus['number']} async for bus in cursor
        ]
        return data

    async def get_bus_stops(self, line_id):
        records = self.db.stops \
            .find({'line': line_id}) \
            .sort([("station_name", 1)])
        data = [
            {'id': stop['station_id'],
             'line': stop['line'],
             'name': stop['station_name']} async for stop in records
        ]
        return data

    async def get_arrivals(self, line_id, station_name):
        records = self.db.arrivals \
            .find({'line_id': line_id, 'station_name': station_name}) \
            .sort([("expected", 1)])
        data = [
            {'line': arrival['line_name'],
             'station_name': arrival['station_name'],
             'direction': arrival['direction'],
             'destination': arrival['destination'],
             'arrival': arrival['expected']} async for arrival in records
        ]
        return data

    async def get_all_lines(self):
        return [bus['id'] async for bus in self.db.buses.find()]

    async def update_buses(self, buses):
        await self.db.buses.remove()
        await self.db.buses.insert_many(buses)

    async def update_bus_stops(self, line, stops):
        # Update per line
        await self.db.stops.remove({"line": line})
        await self.db.stops.insert_many(stops)

    async def update_arrivals(self, lines, arrivals):
        # Update per list of lines [:20]
        await self.db.arrivals.remove({"line_id": {"$in": lines}})
        await self.db.arrivals.insert_many(arrivals)


def get_db_connection(app):
    db, cleanup = None, None
    if app['config']['db'] == 'mongo':
        db = MongoDriver(app)
        cleanup = db.get_cleanup()
    elif app['config']['db'] == 'postgres':
        db = None
        cleanup = None
    if db and cleanup:
        return db, cleanup
    else:
        raise DBImproperlyConfigured(
            'Only Mongo and Postgres supported, check settings.')
