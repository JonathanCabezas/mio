from functools import wraps


def run_only_once(f):
    """Runs a function (successfully) only once.
    The running can be reset by setting the `has_run` attribute to False
    """
    attr_name = "has_run"

    @wraps(f)
    def wrapper(*args, **kwargs):
        if not hasattr(wrapper, attr_name):
            result = f(*args, **kwargs)
            setattr(wrapper, attr_name, True)
            return result

    return wrapper
