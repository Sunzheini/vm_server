import time


def return_hello_world():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f'Hello world {current_time}!')


return_hello_world()
