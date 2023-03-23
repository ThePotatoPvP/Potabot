import sched
import time

scheduler = sched.scheduler(time.time, time.sleep)

def ScheduledEvent(*, hour=0, minute=0, day_of_week=None, day_of_month=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Check if the event should run today based on the specified schedule
            now = datetime.datetime.now()
            if day_of_week is not None and now.weekday() != day_of_week:
                return
            if day_of_month is not None and now.day != day_of_month:
                return
            
            # Schedule the event to run at the specified time
            event_time = datetime.datetime(now.year, now.month, now.day, hour, minute)
            if event_time < now:
                event_time += datetime.timedelta(days=1)
            delay = (event_time - now).total_seconds()
            scheduler.enter(delay, 1, func, args, kwargs)

        # Schedule the event to run immediately on startup, then schedule it daily
        wrapper()
        scheduler.enterabs(time.time() + 86400, 1, wrapper)

        return wrapper
    return decorator
