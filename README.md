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

Obviously, one needs to take into account exponential increases not getting out of hand into a completely unreasonable
 wait. By default, exponential_backoff is 1 meaning all waits are the same as the initial one.
 
The "loud" parameter simply makes the retry decorator print "retrying" before every retry (but not on the first call).
By default is set to False, meaning it will silently retry.

The initial version worked only for functions returning True on success and False on failure, but since it's trivial to
just pass the values over, I modified it to work on functions returning a truthy value on success and a falsy value on
failure. That means, values that will test true/false in a boolean context (namely an "if"). For instance, a function
returning 0 on failure and any other number in success. Or a function returning an empty list on failure and a list with
elements on success. Etc.

Not all functions/methods will return truthy/falsy values signifying success, so you will often have to create a small
utility supervisor function that does return a truthy/falsy value depending on success, maybe set some variable to keep
track of the output of the actual function if that is necessary, and then decorate that. See TODO.

# retry_catch

I added this decorator to deal with the problem of returned values and encapsulation of the errors/failures in a
different way.

In Python, failure is generally expressed by the raising of an exception rather than through returned values. The
decorator @retry_catch provides a mechanism to capture this.


    @retry_catch(10, exception=ValueError, initial_delay=1, exponential_backoff=1.2, loud=True)
    def fails75percent_nottruthy_raisy():
        r = random.random()
        if r < 0.75:
            raise ValueError("oops")
        else:
            return 0  # return a falsy value on success to test this is fine

The default exception caught by the retry_catch decorator is BaseException. In the example I set it to ValueError which
is the concrete exception raised on the failures we want to retry upon. You may want to define an exception class if 
you want the retrials to act only on certain situations or combinations of exceptions (I pondered whether it would make
sense to allow for a tuple with a number of exception classes but I believe it's better to deal with this from the 
outside, simply defining a new exception class).

This decorator will reraise the appropriate exception in Python 3 (In Python 2 it will reraise a generic Exception 
showing the detail in stdout - I did this for simplicity reasons but I might correct it in the future).

# TODO

1. More realistic examples with supervisor functions

2. ~~Generic supervisor to convert any function to a function returning True/False
based on whether an exception was thrown or not.~~ I believe @retry_catch is a better approach for the general case,
letting the user define helper functions to deal with special cases.

3. Maybe it would be interesting to allow for customising the retry message rather than passing a boolean to "loud"

# COMPATIBILITY

Tested on Python 2.7 and 3.6 (should be compatible with 2.6 and anything newer)

# Licence

MIT
