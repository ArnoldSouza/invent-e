from time import (time,
                  strftime,
                  gmtime)


def timeit(method):
    """
    Decorator to use to get information about elapsed time
    of a certain method execution
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
