import pytz
tz = pytz.timezone('Europe/Paris')

import functools
import asyncio
import datetime
import discord
import re, random
import time
from dateutil.relativedelta import relativedelta


async def getDelay(hour, minute, day_of_week, day_of_month):
    now = datetime.datetime.now(tz)
    s = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if day_of_week is not None:
        s += datetime.timedelta(days=(day_of_week - s.weekday()) % 7)
    elif day_of_month is not None:
        s += relativedelta(day=day_of_month)
    t = (s - now).total_seconds()
    return t


def ScheduledEvent(hour: int = 0, minute: int = 0, day_of_week: int = None, day_of_month: int = None):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(client: discord.Client):
            while True:
                time_to_wait = await getDelay(hour, minute, day_of_week, day_of_month)
                if time_to_wait < 0 and time_to_wait > -60:
                    await func(client)
                    time.sleep(60)
                await asyncio.sleep(60)
        return wrapper
    return decorator


def TriggeredEvent(rgx: str = None,
                guild_id: int = None,
                guild_ids: list[int] = None,
                channel_id: int = None,
                channel_ids: list[int] = None,
                user_id: int = None,
                user_ids: list[int] = None,
                chance: int = 100,
                case_sensitive = False):
    """Will run a function when a message matches criterias.

    Args:
        rgx (str, optional): RegEx to be matched by message.content. Defaults to None.
        guild_id (int, optional): id of the server that can trigger the event. Defaults to all.
        guild_ids (list[int], optional): list of guild_id. Defaults to [].
        channel_id (int, optional): id of the channel that can trigger the event. Defaults to all.
        channel_ids (list[int], optional): list of channel_id. Defaults to [].
        user_id (int, optional): id of the user that can trigger the event. Defaults to all.
        user_ids (list[int], optional): list of user_id. Defaults to [].
        chance (int, optional): % of chance to trigger the event. Defaults to 100.
        case_sensitive (bool, optional): Defaults to False.
    """
    def decorator(func):
        async def wrapper(client, message):
            if guild_id is not None: guild_ids.append(int(guild_id))
            if user_id is not None: user_ids.append(int(user_id))
            if channel_id is not None: channel_ids.append(int(channel_id))

            perc = random.uniform(0.0, 100.0)
            if chance >= perc:
                if not message.guild or (guild_ids == [] or message.guild.id in guild_ids):
                    if user_ids == [] or message.author.id in user_ids:
                        if channel_ids == [] or message.channel.id in channel_ids:
                            if case_sensitive:
                                if (rgx is None or (type(rgx) is str and
                                re.match(f'{rgx}', message.content))):
                                    await func(client, message)
                            else:
                                if (rgx is None or (type(rgx) is str and
                                re.match(f'{rgx.lower()}', message.content.lower()))):
                                    await func(client, message)
        return wrapper

    if guild_ids is None: guild_ids = []
    if user_ids is None: user_ids = []
    if channel_ids is None: channel_ids = []
    return decorator
