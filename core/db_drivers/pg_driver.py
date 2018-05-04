# -*- coding: utf-8 -*-
import aiopg
import asyncio

__all__ = (
    'PostgresDriver',
)


class PostgresImproperlyConfigured(Exception):
    pass


class PostgresDriver:
    def __init__(self, app):
        self.dsn = self.make_dsn(app)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.init_connection())
        self.cleanup = self.get_cleanup()

    def make_dsn(self, app):
        try:
            host = app['config']['postgres']['host']
            port = app['config']['postgres']['port']
            database = app['config']['postgres']['database']
            user = app['config']['postgres']['user']
            password = app['config']['postgres']['password']
        except Exception as err:
            raise PostgresImproperlyConfigured(
                f"Set postgres:{err} value in settings.yaml!"
            )
        credentials = f"{user}:{password}"
        dsn = f'postgres://{credentials}@{host}:{port}/{database}'
        return dsn

    async def init_connection(self):
        self.pool = await aiopg.create_pool(self.dsn)

    def get_cleanup(self):
        pool = self.pool

        async def cleanup(app):
            pool.clear()

        return cleanup

    async def get_buses(self):
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT * from lines where type='bus'")
                    data = [
                        {'id': bus[0], 'number': bus[2]} async for bus in cur
                    ]
                    return data
        except Exception as err:
            print(err)

    async def get_bus_stops(self, line_id):
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        "SELECT station_id, line, station_name from stops where line=%s",
                        (line_id,))
                    data = [
                        {'id': row[0],
                         'line': row[1],
                         'name': row[2]} async for row in cursor
                    ]
                    return data
        except Exception as err:
            print(err)

    async def get_arrivals(self, line_id, station_name):
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        "SELECT line, station_name, direction, destination, expected from arrivals where line=%s and station_name=%s order by expected",
                        (line_id, station_name))
                    data = [
                        {'line': row[0],
                         'station_name': row[1],
                         'direction': row[2],
                         'destination': row[3],
                         'arrival': row[4]}
                        async for row in cursor
                    ]
                    return data
        except Exception as err:
            print(err)

    async def get_all_lines(self):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * from lines where type='bus'")
                data = [bus[0] async for bus in cur]
        return data

    async def update_buses(self, buses):
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("DELETE from lines where type='bus'")
                    for bus in buses:
                        await cur.execute(
                            "INSERT INTO lines (id, type, number) VALUES (%s, %s, %s) ",
                            (
                                bus.get('id'), bus.get('type'),
                                bus.get('number')))
        except Exception as err:
            print(err)

    async def update_bus_stops(self, line, stops):
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("DELETE from stops where line=%s",
                                      (line,))
                    for stop in stops:
                        await cur.execute(
                            "INSERT INTO stops (line, station_id, station_name, lat, lon) VALUES (%s, %s, %s, %s, %s) ",
                            (stop.get('line'), stop.get('id'),
                             stop.get('station_name'), stop.get('lat'),
                             stop.get('lon')))
        except Exception as err:
            print(err)

    async def update_arrivals(self, lines, arrivals):
        # Update per list of lines [:20]
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    for line in lines:
                        await cur.execute("DELETE from arrivals where line_id=%s",
                                          (line,))
                    for arrival in arrivals:
                        await cur.execute(
                            "INSERT INTO arrivals (station_name, line, line_id, direction, vehicle_id, destination, expected) VALUES (%s, %s, %s, %s, %s, %s, %s) ",
                            (arrival.get('station_name'),
                             arrival.get('line_name'),
                             arrival.get('line_id'), arrival.get('direction'),
                             arrival.get('vehicle_id'),
                             arrival.get('destination'),
                             arrival.get('expected')))
        except Exception as err:
            print(err)
