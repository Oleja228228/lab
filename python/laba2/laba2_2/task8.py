import time

def timing(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        duration = (end - start) * 1000
        print(f"Function {func.__name__} executed in {duration:.3f} ms")
        return result
    return wrapper

@timing
def function(n):
    total = 0
    for i in range(n):
        total += i ** 2
    return total

print(function(1000))