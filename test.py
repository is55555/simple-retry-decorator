from __future__ import print_function
from retry import retry, retry_catch
import random


def fails_the_first_3_times():  # this may be a bit convoluted, fails75percent is a lot simpler
    n = 3
    while n > 0:
        print("no")
        yield False
        n -= 1
    print("yes")
    yield True

x = fails_the_first_3_times()


@retry(5, loud=True)
def fails3():
    return next(x)


@retry(10, initial_delay=0.5, exponential_backoff=1.5, loud=True)
def fails75percent():
    if random.random() < 0.75:
        return False
    else:
        return True


@retry(10, initial_delay=1, exponential_backoff=1.2, loud=True)
def fails75percent_truthy():
    r = random.random()
    if r < 0.75:
        return 0
    else:
        return r * 100.0


@retry_catch(10, exception=ValueError, initial_delay=1, exponential_backoff=1.2, loud=True)
def fails75percent_nottruthy_raisy():
    r = random.random()
    if r < 0.75:
        raise ValueError("oops")
    else:
        return 0  # return a falsy value on success to test this is fine


@retry_catch(2, exception=ValueError, initial_delay=1, exponential_backoff=1.2, loud=True)
def fails75percent_nottruthy_raisy_twice():
    r = random.random()
    if r < 0.75:
        raise ValueError("oops")
    else:
        return 0  # return a falsy value on success to test this is fine


print("calling fails75percent with retry(10, initial_delay=0.5, exponential_backoff=1.5, loud=True)")
print(fails75percent())

print("calling fails75percent_truthy with retry(10, initial_delay=1, exponential_backoff=1.2, loud=True)")
print(fails75percent_truthy())

print("calling fails3 with retry(5)")
print(fails3())

try:
    print("calling fails75percent_nottruthy_raisy with " +
          "@retry_catch(10, exception=ValueError, initial_delay=1, exponential_backoff=1.2, loud=True)")
    print(fails75percent_nottruthy_raisy())
except ValueError:
    print("Failed with the expected exception")

try:
    print("calling fails75percent_nottruthy_raisy_twice with " +
          "@retry_catch(2, exception=ValueError, initial_delay=1, exponential_backoff=1.2, loud=True)")
    print(fails75percent_nottruthy_raisy_twice())   # note that this is expected to fail often, and do it with the
    # original exception
except ValueError:
    print("Failed with the expected exception")

print("end")

