#декоратор который разрешает определенное количество вызововза количествовремни
import time


def calls(call, times):
    def decorator(func):
        count = 0
        all_calls = []
        def wrapper(*args, **kwargs):
            nonlocal count, all_calls
            now = time.time()
            all_calls.append(now)
            if count >= call and sum(all_calls) >= times:
                print("error")
                count =0
                all_calls = []
                time.sleep(3)
            else:
                count += 1
                func(*args, **kwargs)
        return wrapper
    return decorator


@calls(5, 3)
def func(a,b):
    print(a + b)


func(1, 2)
func(1, 2)
func(1, 2)
func(1, 2)
func(1, 2)
func(1, 2)
func(1, 2)