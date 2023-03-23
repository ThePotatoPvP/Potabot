import datetime
import asyncio
import functools

import asyncio
import functools
import datetime
import pytz
tz = pytz.timezone('Europe/Paris')

import functools
import datetime
import asyncio


def ScheduledEvent(hour: int=0, minute: int=0, day_of_week: int = None, day_of_month: int = None):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            while True:
                now = datetime.datetime.now(tz)
                if now.hour == hour and now.minute == minute:
                    if day_of_week is not None and now.weekday() == day_of_week:
                        await func(*args, **kwargs)
                    elif day_of_month is not None and now.day == day_of_month:
                        await func(*args, **kwargs)
                await asyncio.sleep(60)
        return wrapper
    return decorator

