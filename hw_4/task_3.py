import multiprocessing
import time
import codecs
from datetime import datetime


def process_a(queue_ab, pipe_ab):
    while True:
        message = queue_ab.get()
        time.sleep(5)
        message_lower = message.lower()
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Обработали сообщение в потоке А и отправили в B {message_lower}")
        pipe_ab.send(message_lower)


def process_b(pipe_ab, pipe_b_main):
    while True:
        message_lower = pipe_ab.recv()
        encoded_message = codecs.encode(message_lower, 'rot_13')
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Обработали сообщение в потоке B и отправили на вывод {encoded_message}")
        pipe_b_main.send(encoded_message)


if __name__ == '__main__':
    queue_ab = multiprocessing.Queue()
    pipe_ab = multiprocessing.Pipe()
    pipe_b_main = multiprocessing.Pipe()

    process_a = multiprocessing.Process(target=process_a, args=(queue_ab, pipe_ab[1]))
    process_b = multiprocessing.Process(target=process_b, args=(pipe_ab[0], pipe_b_main[1]))

    process_a.start()
    process_b.start()

    try:
        while True:
            message = input()
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Получили сообщение {message}")
            queue_ab.put(message)

            encoded_message = pipe_b_main[0].recv()
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Вывели результат для сообщения: {encoded_message}")
    except KeyboardInterrupt:
        process_a.terminate()
        process_b.terminate()
