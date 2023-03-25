import pytz
tz = pytz.timezone('Europe/Paris')

import functools
import asyncio
import datetime
import discord

def ScheduledEvent(hour: int = 0, minute: int = 0, day_of_week: int = None, day_of_month: int = None):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(client: discord.Client):
            while True:
                now = datetime.datetime.now(tz)
                scheduled_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                if day_of_week is not None:
                    scheduled_time += datetime.timedelta(days=(day_of_week - scheduled_time.weekday()) % 7)
                elif day_of_month is not None:
                    scheduled_time += datetime.timedelta(days=(day_of_month - scheduled_time.day) % 30)
                time_to_wait = (scheduled_time - now).total_seconds()
                if time_to_wait < 0:
                    scheduled_time += datetime.timedelta(days=1)
                    time_to_wait = (scheduled_time - now).total_seconds()
                await asyncio.sleep(time_to_wait)
                await func(client)
        return wrapper
    return decorator