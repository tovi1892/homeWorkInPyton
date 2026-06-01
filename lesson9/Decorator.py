import  datetime
def time(func):
    def wrapper():
        start=(datetime.datetime.now())
        func()
        end=(datetime.datetime.now())
        print(f"the time func runing:{end-start}" )
    return  wrapper()



@time
def func():
    for _ in range(0):
        i=0






