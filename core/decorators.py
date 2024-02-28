import time

from vm_server.settings import location_for_the_log_file, desired_format_of_the_logged_date_and_time


def _execute_with_try_except(func, *args, **kwargs):
    """
    Wraps a function with a try-except block
    @param func: the function to be wrapped
    @param args: the arguments of the function
    @param kwargs: the keyword arguments of the function
    @return: result of the function or exception
    """
    try:
        result = func(*args, **kwargs)
    except Exception as e:
        return e
    return result


def _turn_to_seconds(measurement):
    """
    Turns a measurement in seconds to milliseconds if it is less than 0.001
    @param measurement: the measurement in seconds
    @return: the measurement in seconds or milliseconds
    """
    if measurement < 0.001:
        measurement *= 1000
        return measurement
    else:
        return measurement


def _log_the_result(result):
    """
    Logs the result in a txt file
    @param result: the result to be logged
    @return: None
    """
    log_location = location_for_the_log_file

    with open(log_location, 'a', encoding='utf-8', ) as file:
        file.write('\n')
        file.write(result)


def _get_current_date_time():
    """
    Returns the current date and time
    @return: current date and time
    """
    current_date_and_time = time.localtime()
    result = time.strftime(desired_format_of_the_logged_date_and_time, current_date_and_time)
    return result


def time_measurement_decorator(func):
    """
    Measures the time a function takes to execute and prints the result in the console.
    Also uses _execute_with_try_except to wrap the function with a try-except block
    and logs the result in a txt file together with the current date and time
    @param func: the function to be wrapped
    @return: result of the function
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = _execute_with_try_except(func, *args, **kwargs)
        end = time.time()
        measurement = end - start

        current_date_time = _get_current_date_time()
        info = f"[{current_date_time}]: {func.__name__} took: {_turn_to_seconds(measurement):.3f}s with result: {result}"
        _log_the_result(info)
        print(info)

        return result
    return wrapper
