import functools


def log(filename=None):
    """
    Декоратор для логирования выполнения функций.
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            func_name = func.__name__
            args_repr = [repr(arg) for arg in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            inputs_str = f"({', '.join(args_repr + kwargs_repr)})"

            start_msg = f"{func_name} start. Inputs: {inputs_str}"
            if filename:
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write(start_msg + '\n')
            else:
                print(start_msg)
            try:
                result = func(*args, **kwargs)
                success_msg = f"{func_name} ok"
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(success_msg + '\n')
                else:
                    print(success_msg)
                return result
            except Exception as e:
                error_type = type(e).__name__
                error_msg = f"{func_name} error: {error_type}. Inputs: {inputs_str}"
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(error_msg + '\n')
                else:
                    print(error_msg)
                raise
        return inner
    return wrapper
