from datetime import datetime
from threading import Thread
import logging


def factorize(*number):
    """Приймає список чисел та повертає список чисел, на які числа із вхідного списку поділяються без залишку"""

    result = []
    for el in number:
        result.append([i for i in range(el+1) if el>=i>0 and el%i == 0])
    logging.debug('Function finished work.')
    return result


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    start_time = datetime.now()
    list_of_args = [128, 255, 99999, 10651060]
    threads = []
    for el in list_of_args:
        thread = Thread(target=factorize, args=(el,))
        thread.start()
        threads.append(thread)

    [elem.join() for elem in threads]

    operation_time = datetime.now() - start_time
    logging.debug(f"Skript finished in {operation_time.microseconds} microseconds!")
