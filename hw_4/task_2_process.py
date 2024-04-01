import os
import math
import concurrent.futures
import logging
import time

logging.basicConfig(filename='artifacts/4_2/process.txt', level=logging.INFO, format='%(asctime)s - %(message)s')


def integrate_range(f, a, step, start, end):
    local_acc = 0
    for i in range(start, end):
        local_acc += f(a + i * step) * step
    return local_acc


def integrate(f, a, b, *, n_jobs=1, n_iter=10000000):
    acc = 0
    step = (b - a) / n_iter

    with concurrent.futures.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        futures = []
        for i in range(n_jobs):
            start = i * (n_iter // n_jobs)
            end = (i + 1) * (n_iter // n_jobs) if i != n_jobs - 1 else n_iter
            futures.append(executor.submit(integrate_range, f, a, step, start, end))

        for future in concurrent.futures.as_completed(futures):
            acc += future.result()

    return acc


def time_execution(f, n_jobs):
    start_time = time.time()
    result = f(math.cos, 0, math.pi / 2, n_jobs=n_jobs)
    end_time = time.time()
    return end_time - start_time


if __name__ == '__main__':
    cpu_num = os.cpu_count()

    for n_jobs in range(1, cpu_num * 2 + 1):
        logging.info(f'Starting integrate with {n_jobs} jobs')
        time_process = time_execution(integrate, n_jobs)
        logging.info(f'Time taken with {n_jobs} jobs using ProcessPoolExecutor: {time_process}')