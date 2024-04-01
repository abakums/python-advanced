import time
import threading
import multiprocessing


FIB_CALLS_COUNT = 10


def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


def time_measure(message):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.monotonic()
            result = func(*args, **kwargs)
            end_time = time.monotonic()
            print(f"{message}: {end_time - start_time:.6f} seconds")
            return result
        return wrapper
    return decorator


@time_measure("Synchronously time")
def run_synchronously(n):
    for i in range(FIB_CALLS_COUNT):
        fibonacci(n)


@time_measure("Threads time")
def run_with_threads(n):
    threads = []
    for _ in range(FIB_CALLS_COUNT):
        thread = threading.Thread(target=fibonacci, args=(n,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


@time_measure("Processes time")
def run_with_processes(n):
    processes = []
    for _ in range(FIB_CALLS_COUNT):
        process = multiprocessing.Process(target=fibonacci, args=(n,))
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()


if __name__ == "__main__":
    fib_count = 37  # Укажите здесь большое значение n

    print("Synchronously")
    run_synchronously(fib_count)

    print("Threads")
    run_with_threads(fib_count)

    print("Processes")
    run_with_processes(fib_count)
