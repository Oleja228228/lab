import datetime

def log_calls(filename):
    def decorator(func):
        def wrapper(*args, **kwargs):
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_line = f"[{now}] {func.__name__} called with args={args}, kwargs={kwargs}\n"
            with open(filename, "a", encoding="utf-8") as f:
                f.write(log_line)
            return func(*args, **kwargs)
        return wrapper
    return decorator


@log_calls("calls.log")
def add(a, b):
    return a + b

print(add(3, 5))

