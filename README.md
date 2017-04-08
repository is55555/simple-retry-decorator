# Simple retry decorator
 
Example from test.py:

    @retry(10, initial_delay=0.5, exponential_backoff=1.5, loud=True)
    def fails75percent():
        if random.random() < 0.75:
            return False
        else:
            return True
    
    # 
    print("calling fails75percent with retry(10, initial_delay=0.5, exponential_backoff=1.5, loud=True)")
    print(fails75percent())

This snippet will retry up to 10 times a function that fails 75% of the time.

It will wait 0.5 seconds after the first failure.

Subsequent waiting times will increase by a factor of 1.5 - so the second waiting time will be 0.5 * 1.5 = 0.75, 
the third waiting time will be 0.75 * 1.5 = 1.125, then 1.6875, 2.53125, 3.796875, 5.6953125, 8.54296875 and so on.

Obviously one needs to take into account exponential increases not getting out of hand into a completely unreasonable
 wait. By default, exponential_backoff is 1 meaning all waits are the same as the initial one.

# TODO
1. Supervisor to convert any function to a function returning True/False
based on whether an exception was thrown or not.

2. Maybe it would be interesting to allow for customising the retry message rather than passing a boolean to "loud"

# Licence

MIT
