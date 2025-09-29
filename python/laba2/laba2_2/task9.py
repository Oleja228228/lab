def type_check(*types):
    def decorator(func):
        def wrapper(*args):
            for i, (arg, expected_type) in enumerate(zip(args, types)):
                if not isinstance(arg, expected_type):
                    raise TypeError(
                        f"Argument {i+1} of {func.__name__} must be {expected_type.__name__}, "
                        f"got {type(arg).__name__}"
                    )
            return func(*args)
        return wrapper
    return decorator

@type_check(int, int)
def add(a, b):
    return a + b

@type_check(str, int)
def repeat_text(text, times):
    return text * times

print(add(5, 10))
#print(add(5, "10"))

print(repeat_text("lol", 3))
# print(repeat_text(5, 3))
