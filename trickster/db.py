# -*- coding: utf-8 -*-

async def update_buses(db, buses):
    await db.buses.remove()
    await db.buses.insert_many(buses)


async def update_stops(db, line, stops):
    # Update per line
    print(line)
    await db.stops.remove({"line": line})
    await db.stops.insert_many(stops)


async def update_arrivals(db, lines, arrivals):
    # Update per list of lines [:20]
    await db.arrivals.remove({"line_id": {"$in": lines}})
    await db.arrivals.insert_many(arrivals)
