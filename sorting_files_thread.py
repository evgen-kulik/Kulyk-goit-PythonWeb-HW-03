"""
Сортування файлів в теці з використанням потоків
"""

import argparse
import logging
import os
from pathlib import Path
from threading import Thread


parser = argparse.ArgumentParser(description="Sorting files in folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="sorted_folder")
args = vars(parser.parse_args())  # перетворює в словник

source = Path(args.get("source"))
output = Path(args.get("output"))
folders = []

lst_images = ['jpeg', 'png', 'jpg', 'svg', 'bmp']
lst_videos = ['avi', 'mp4', 'mov', 'mkv']
lst_documents = ['docx', 'doc', 'txt', 'pdf', 'xlsx', 'pptx']
lst_music = ['mp3', 'ogg', 'wav', 'amr']
lst_archives = ['zip', 'gz', 'rar', 'tar']
new_path = None

def grabs_folder(path: Path) -> None:
    """Рекурсивно проходить по всім вкладеним текам і додає їх шляхи в список"""

    for el in path.iterdir():
        if el.is_dir():  # якщо елемент є текою
            folders.append(el)
            grabs_folder(el)


def remove_file(path: Path) -> None:
    """Переміщує файл для у відповідну теку"""

    global new_path
    for el in path.iterdir():
        if el.is_file():
            old_address = Path(el)  # отримаємо абсолютну адресу файла
            ext = el.suffix[1:]
            if ext in lst_images:
                new_path = output / 'images'
            elif ext in lst_videos:
                new_path = output / 'videos'
            elif ext in lst_documents:
                new_path = output / 'documents'
            elif ext in lst_music:
                new_path = output / 'music'
            elif ext in lst_archives:
                new_path = output / 'archives'
            try:
                new_path.mkdir(exist_ok=True, parents=True)
            except OSError as error:
                logging.error(error)
            try:
                os.rename(old_address, new_path / el.name)
            except OSError as error:
                logging.error(error)
    logging.debug("Файли відсортовано.")


def del_empty_folder(path: Path) -> None:
    """Рекурсивно видаляє порожні теки"""

    for address, dirs, files in os.walk(path, topdown=False):
        # topdown=False означає, що ідемо пошуком зсередини назовні, інакше якщо в теці-1 буде порожня тека-2,
        # то тека-1 не видалиться, видалиться тільки тека-2
        for d in dirs:
            way = os.path.join(address, d)
            if not os.listdir(way):
                os.rmdir(way)
    logging.debug("Порожні теки видалено.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    folders.append(source)
    grabs_folder(source)

    # відсортуємо файли з використанням потоків
    threads = []
    for folder in folders:
        th = Thread(target=remove_file, args=(folder,))
        th.start()
        threads.append(th)
        th.join()  #Блокування роботи наступного потоку, доки попередній не завершить роботу (інакше програма працює некоректно)

    # видалимо порожні теки з використанням потоків
    threads = []
    for folder in folders:
        th = Thread(target=del_empty_folder, args=(folder,))
        th.start()
        threads.append(th)
        th.join()

    print(f"Програму завершено.")

# python sorting_files_thread.py -s D:\Projects\python_web\HW_3_python_web\\test_sort -o D:\Projects\python_web\HW_3_python_web\\test_sort