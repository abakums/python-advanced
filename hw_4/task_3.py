import multiprocessing
import time
import codecs
from datetime import datetime


def process_a(queue_ab, queue_ab_b):
    while True:
        message = queue_ab.get()
        time.sleep(5)
        message_lower = message.lower()
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Обработали сообщение в потоке А и отправили в B {message_lower}")
        queue_ab_b.put(message_lower)


def process_b(queue_ab_b, queue_b_main):
    while True:
        message_lower = queue_ab_b.get()
        encoded_message = codecs.encode(message_lower, 'rot_13')
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Обработали сообщение в потоке B и отправили на вывод {encoded_message}")
        queue_b_main.put(encoded_message)


if __name__ == '__main__':
    queue_ab = multiprocessing.Queue()
    queue_ab_b = multiprocessing.Queue()
    queue_b_main = multiprocessing.Queue()

    process_a = multiprocessing.Process(target=process_a, args=(queue_ab, queue_ab_b))
    process_b = multiprocessing.Process(target=process_b, args=(queue_ab_b, queue_b_main))

    process_a.start()
    process_b.start()

    while True:
        message = input("[Введите]: ")
        if message:
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Получили сообщение {message}")
            queue_ab.put(message)

        if not queue_b_main.empty():
            encoded_message = queue_b_main.get()
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Вывели результат для сообщения: {encoded_message}")

