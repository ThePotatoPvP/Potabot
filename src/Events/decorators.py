import pytz
tz = pytz.timezone('Europe/Paris')

import functools
import asyncio
import datetime
import discord
import re, random

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


def TriggeredEvent(keyword: str = None,
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
        keyword (str, optional): RegEx to be matched by message.content. Defaults to None.
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
                                if (keyword is None or (type(keyword) is str and
                                re.match(f'(|.*\s){keyword}(\s.*|)', message.content))):
                                    await func(client, message)
                            else:
                                if (keyword is None or (type(keyword) is str and
                                re.match(f'(|.*\s){keyword.lower()}(\s.*|)', message.content.lower()))):
                                    await func(client, message)
        return wrapper

    if guild_ids is None: guild_ids = []
    if user_ids is None: user_ids = []
    if channel_ids is None: channel_ids = []
    return decorator
