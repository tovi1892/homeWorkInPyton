def fibonacci_generator():
    x = 1
    y = 1
    z = 1
    while True:
        yield x
        z = x + y
        y = x
        x = z


gen = fibonacci_generator()
print(next(gen))
print(next(gen))


def unique_letters_generator(List):
    i = 0
    while i < len(List):
        yield set(List[i])
        i += 1


List = ["drejfgjhfadhs", "ahfashfakslhf"]
gen2 = unique_letters_generator(List)
print(next(gen2))
print(next(gen2))
print(next(gen2))
