# Created by Peter Norvig

# TODO: need to somehow enable sys._getframe()
# even though 'sys' is technically locked down

#import inspect  # old and really slow!
import sys

class watchedlist(list):
    """A class that wraps a list, and monitors sets and gets.  
    Optionally monitors local variables."""
    def __setitem__(self, i, val):
        print('setting A[{}] = {}'.format(i, val))
        self.watchlocals()
        return list.__setitem__(self, i, val)
    def __getitem__(self, i):
        print('fetching A[{}]; value is {};'.format(
          self, i, list.__getitem__(self, i)))
        self.watchlocals()
        return list.__getitem__(self, i)
        
    def watchlocals(self):
        if hasattr(self, 'watchedlocals'):
            #D = inspect.stack()[2][0].f_locals # old and really slow!
            D = sys._getframe(2).f_locals
            print('    watched locals: {}'.format(
                   {var: D[var] for var in self.watchedlocals}))
        
        
def watch(object, watchedspec):
    """Wrap object with a wrapper class (like watchedlist).
    watchedspec is either None or a callable (like watchedlist), or
    a 2-tuple of (callable, local_var_names), where local_var_names
    can be a string or a sequence of strings."""
    if not watchedspec:
        return object
    kind, locals = (watchedspec if isinstance(watchedspec, (tuple, list)) else
                    (watchedspec, ()))
    if isinstance(locals, str): locals = locals.split()
    watched = kind(object)
    watched.watchedlocals = locals
    return watched
        

class watchfn(object):
    """Decorator that watches the arguments of a function.
    Specify watchedspecs for each positional argument, and optionally 
    for keyword arguments."""
    def __init__(self, *args, **kwargs):
        self.args, self.kwargs = args, kwargs
        
    def __call__(self, fn):
        def wrapped_fn(*args, **kwargs):
            args = [watch(obj, spec) for (obj, spec) in zip(args, self.args)]
            kwargs = {k: watch(kwargs[k], self.args.get(k, None)) for k in kwargs}
            return fn(*args, **kwargs)
        #wrapped_fn.__name__ = fn.__name__
        return wrapped_fn

