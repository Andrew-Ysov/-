import random
from datetime import time, timedelta

START_TIME = timedelta(hours=9)
END_TIME = timedelta(hours=17, minutes=30)

def timedelta_to_time(td: timedelta) -> time:
    'перевод из datetime.timedelta в формат datetime.time'

    total_seconds = td.total_seconds()
    hours = int(total_seconds // 3600) % 24
    minutes = int((total_seconds % 3600) // 60)

    return time(hours, minutes)

def time_to_timedelta(t: time) -> timedelta:
    return timedelta(
        hours=t.hour,
        minutes=t.minute)

def main(num_of_devices: int) -> list:
    'возвращает матрицу с временем отправления сообщения для num_of_devices девайсов'

    result = []

    for _ in range(num_of_devices):
        time_to_send = []
        message_time = START_TIME

        num_of_messages = random.randrange(8,11)
        prev_delta = timedelta(minutes=0)

        for _ in range(num_of_messages):
            if prev_delta > timedelta(minutes=60):
                # в среднем для отправления 10 сообщения за 8 часов 
                # нужно отправлять 1 сообщение каждые 48 минут
                # эта проверка создана для того, чтобы приблизиться к этому среднему
                delta = timedelta(minutes=30)
            else:
                interval = random.randrange(30, 91, 5)
                delta = timedelta(minutes=interval)
            
            message_time += delta
            prev_delta = delta
            if message_time > END_TIME:
                break
            time_to_send.append(timedelta_to_time(message_time))

        result.append(time_to_send)
    return result

def test(num_of_devices):
    result = main(num_of_devices)

    for time_list in result:
        n = len(time_list)
        if n < 8 or n > 10:
            print(f'количество сообщений должно быть в пределах от 8 до 10, а получено {n}')

        for message_time in time_list:
            if message_time < time(hour=9, minute=30) or message_time > time(hour=17, minute=30):
                print(f'сообщение должно быть отправлено в промежуток между 9:30 и 17:30, а \
                      время отправления {message_time}')
        
        for i in range(1, len(time_list)):
            prev_message_time = time_to_timedelta(time_list[i-1])
            message_time = time_to_timedelta(time_list[i])

            time_difference = message_time - prev_message_time

            if (time_difference < timedelta(minutes=30)) or (time_difference > timedelta(minutes=90)):
                print(f'интервал между сообщениями должен быть от 30 до 90 минут, а \
                      интервал был {time_difference}')

if __name__ == '__main__':
    devices = 2

    ans = main(devices)
    for time_list in ans:
        for time_to_sent in time_list:
            print(time_to_sent)
        print('//////')

    devices_for_test = 1000
    test(devices_for_test)