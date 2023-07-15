"""This is the routine module
"""

import threading

class Routine:
    """Decorator class for running a function on a schedule"""
    def __init__(self, recurrence):
        self.schedule = recurrence

    def __repr__(self):
        return f"Routine every {self.schedule} seconds"

    def __call__(self, orig_func):
        decorator_self = self

        def wrap(*args, **kwargs):
            event = threading.Event()

            def loop():
                while not event.wait(decorator_self.schedule):
                    orig_func(*args, **kwargs)

            thread = threading.Thread(target=loop)
            thread.daemon = True
            thread.start()

            return event

        return wrap
