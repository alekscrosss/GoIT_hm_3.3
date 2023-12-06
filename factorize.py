import multiprocessing
import time

# Функция для факторизации одного числа
def factorize_single(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

# Функция для факторизации нескольких чисел однопоточным методом
def factorize(*numbers):
    return [factorize_single(number) for number in numbers]

start_time = time.time()
a, b, c, d = factorize(128, 255, 99999, 10651060)
single_threaded_time = time.time() - start_time

# Проверка результатов однопоточной факторизации
assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

print(single_threaded_time)

# Функция для факторизации нескольких чисел с использованием многопоточности
"""def factorize_parallel(*numbers):
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(factorize_single, numbers)
    return results

# Запуск многопоточной факторизации
start_time = time.time()
parallel_results = factorize_parallel(128, 255, 99999, 10651060)
parallel_time = time.time() - start_time

# Проверка результатов многопоточной факторизации
parallel_correct = (
    parallel_results[0] == [1, 2, 4, 8, 16, 32, 64, 128] and
    parallel_results[1] == [1, 3, 5, 15, 17, 51, 85, 255] and
    parallel_results[2] == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999] and
    parallel_results[3] == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
)
print(parallel_time)
"""


