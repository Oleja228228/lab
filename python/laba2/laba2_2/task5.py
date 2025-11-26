def cache(func):
    saved_results = {}

    def wrapper(*args):
        if args in saved_results:
            print(f"Returning cached result for {func.__name__}{args}")
            return saved_results[args]

        result = func(*args)
        saved_results[args] = result
        print(f"Caching result for {func.__name__}{args}")
        return result

    return wrapper


@cache
def square(x):
    print(f"Calculating square of {x}: ")
    return x * x

print(square(5))
print(square(5))
print(square(10))
print(square(10))
