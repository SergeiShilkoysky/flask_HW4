""" Задание №7
-Напишите программу на Python, которая будет находить сумму элементов массива из
 1000000 целых чисел.
Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
-Массив должен быть заполнен случайными целыми числами от 1 до 100.
-При о решении задачи нужно использовать многопоточность, многопроцессорность
и асинхронность.
-В каждом решении нужно вывести время выполнения вычислений.
"""
import multiprocessing
import threading
import time
from random import randint
import asyncio

COUNT = 10  # количество потоков, процессов, задач


def generate_array():
    arr = [randint(1, 100) for i in range(1_000_000)]
    # arr = [19, 25, 73, 17, 11, 14, 15, 18, 2, 23, 25, 27, 30, 34, 60, 555]
    return arr


sum_arr = 0


def sum_array(arr, num):
    global sum_arr
    for i in arr:
        sum_arr += i
    print(f"Сумма элементов массива ({num}): {sum_arr}")


async def sum_array_async(arr, num):
    global sum_arr
    for i in arr:
        sum_arr += i
    print(f"Сумма элементов массива ({num}): {sum_arr}")


def sum_use_threading(arr):
    threads = []
    start_time = time.time()
    # Разбиваем на массив на COUNT частей (по количеству потоков)
    for thread_part in range(COUNT):
        thread_start = int(thread_part * (len(arr) / COUNT))
        thread_end = int((thread_part + 1) * (len(arr) / COUNT))
        t = threading.Thread(target=sum_array(arr[thread_start:thread_end], thread_part + 1), args=(arr,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    end_time = time.time() - start_time
    print('завершение  потоков')
    print('результат суммирования массива:', sum_arr)
    print(f"Общее время работы при многопоточном подходе: {end_time:.10f} seconds \n")
    return end_time


def sum_with_process(arr):
    start_time = time.time()
    processes = []
    for proc_part in range(COUNT):
        proc_start = int(proc_part * (len(arr) / COUNT))
        proc_end = int((proc_part + 1) * (len(arr) / COUNT))
        p = multiprocessing.Process(target=sum_array(arr[proc_start:proc_end], proc_part + 1), args=(arr,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    end_time = time.time() - start_time
    print('завершение  процессов')
    print('результат суммирования массива:', sum_arr)
    print(f"Общее время работы при мультипроцессорном подходе: {end_time:.10f} seconds \n")
    return end_time


async def sum_with_async(arr):
    tasks = []
    sum_arr = 0
    for assync_part in range(COUNT):
        assync_start = int(assync_part * (len(arr) / COUNT))
        assync_end = int((assync_part + 1) * (len(arr) / COUNT))
        task = asyncio.ensure_future(sum_array_async(arr[assync_start:assync_end], assync_part + 1))
        tasks.append(task)
    await asyncio.gather(*tasks)
    end_time = time.time() - start_time
    print('завершение  асинхронного метода')
    print('результат суммирования массива:', sum_arr)
    print(f"Общее время работы при асинхронном  подходе: {end_time:.10f} seconds \n")
    return end_time


if __name__ == "__main__":
    arr = generate_array()

    print('\t Старт потоков')
    sum_use_threading(arr)
    sum_arr = 0
    print('\t Старт процессов')
    sum_with_process(arr)
    sum_arr = 0
    print('\t Старт асинхронного метода')
    start_time = time.time()
    loop = asyncio.get_event_loop()  # получили цикл событий
    loop.run_until_complete(sum_with_async(arr))
