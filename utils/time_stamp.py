from time import (time,
                  strftime,
                  localtime,
                  gmtime)
from functools import wraps


# used in debugging
def timeit(method):
    """
    USE IN DEBUG
    Decorator to get information about elapsed time
    of a certain method execution.
    """
    def timed(*args, **kw):
        ts = time()
        result = method(*args, **kw)
        te = time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('method {} finished in (hh:mm:ss): {}'
                  .format(method.__name__,
                          strftime("%H:%M:%S", gmtime(te-ts))))
        return result
    return timed


# used in production, to print out info to the user
def timing(func):
    """
    USE IN PRODUCTION
    Decorator to get information about elapsed time
    of a certain method execution.
    """
    @wraps(func)
    def wrap(*args, **kw):
        ts = time()
        print('\n' + '-' * 79,
              '\n', 'starting at: {}h'.format(strftime("%H:%M:%S", localtime(ts))),
              end='\n'*2)
        result = func(*args, **kw)
        te = time()
        print('\n', 'finished (hh:mm:ss): {}'.format(strftime("%H:%M:%S", gmtime(te-ts))),
              sep='', end='\n' + '-' * 79 + '\n' * 2)
        return result
    return wrap


# test implementation
if __name__ == '__main__':
    @timing
    @timeit
    def f(a):
        for _ in range(a):
            pass
        return -1
    f(100000000)
