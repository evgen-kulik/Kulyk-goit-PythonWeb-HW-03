from datetime import datetime
import logging
from multiprocessing import Pool, current_process, cpu_count

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

def factorize(*number):
    """Приймає список чисел та повертає список чисел, на які числа із вхідного списку поділяються без залишку"""

    result = []
    for el in number:
        result.append([i for i in range(el+1) if el>=i>0 and el%i == 0])
    logging.debug(f'{current_process().name} finished work.')
    return result


if __name__ == '__main__':
    list_of_args = [128, 255, 99999, 10651060]
    start_time = datetime.now()
    with Pool(processes=cpu_count()) as pool:
        logger.debug(pool.map(factorize, list_of_args))

    operation_time = datetime.now() - start_time
    logging.debug(f"Skript finished in {operation_time.microseconds} microseconds!")

