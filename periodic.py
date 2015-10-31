import time


def periodic(period):
    def decorator(func):
        def wrapped(*args, **kwargs):
            while True:
                start = time.now()
                func(*args, **kwargs)
                stop = time.now()
                duration = stop - start
                if duration < period:
                    time.sleep(period - duration)
        return wrapped
    return decorator
