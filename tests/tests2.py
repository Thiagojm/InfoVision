import time


def fib_func(n):
    if n <2:
        return n
    return fib_func(n - 1) + fib_func(n - 2)


# Driver Program

t0 = time.time()
print(fib_func(33))
t1 = time.time()
print(t1-t0)