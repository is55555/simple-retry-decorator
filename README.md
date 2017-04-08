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
 
The "loud" parameter simply makes the retry decorator print "retrying" before every retry (but not on the first call).
By default is set to False, meaning it will silently retry.

Obviously not all functions/methods will return True or False, so you will often have to create a small utility
supervisor function that does return True or False, set some variable to keep track of the output of the actual
function and then decorate that. See TODO.

# TODO

1. More realistic examples with supervisor functions

2. Generic supervisor to convert any function to a function returning True/False
based on whether an exception was thrown or not.

3. Maybe it would be interesting to allow for customising the retry message rather than passing a boolean to "loud"

# Licence

MIT
