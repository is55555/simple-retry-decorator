import time

import sys
if sys.version_info < (3,):  # pragma: no cover
    integer_types = (int, long,)
else:  # pragma: no cover
    integer_types = (int,)


# decorator
def retry(tries, initial_delay=1, exponential_backoff=1, loud=False):
    """Retries a function/method until it returns True.

    initial_delay: initial delay in seconds
    exponential_backoff: multiplicative factor of delay with each extra try. 1 means the delay stays the same."""
    if not isinstance(tries, integer_types):
        raise ValueError("tries must be an integer type")
    if tries < 0:
        raise ValueError("tries must be >= 0")
    if initial_delay <= 0:
        raise ValueError("delay must be greater than 0")
    if exponential_backoff < 1:
        # back-offs between 0 and 1 would mean accelerating retries, which doesn't make much sense so I've disabled it.
        # the default back-off at 1 makes the delay stay the same across tries. 2 would double the delay every time.
        raise ValueError("exponential back-off must be >= 1")

    def decorator(f):
        def closure(*args, **kwargs):
            mutable_tries = tries
            mutable_delay = initial_delay
            return_value = f(*args, **kwargs)  # initial call
            while mutable_tries > 0:
                if return_value:
                    return return_value
                mutable_tries -= 1
                if loud:
                    print("retrying")
                time.sleep(mutable_delay)
                mutable_delay *= exponential_backoff
                return_value = f(*args, **kwargs)  # retry call
            return return_value
        return closure  # decorator -> decorated function

    return decorator  # @retry(args) -> decorator

