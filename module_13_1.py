import asyncio
import time


print('------\nЗадача "Асинхронные силачи"\n------')


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнование')
    time_delay = 1 / power
    ball_number = 1
    while ball_number <= 5:
        await asyncio.sleep(time_delay)
        print(f'Силач {name} поднял {ball_number} шар')
        ball_number += 1
        if ball_number > 5:
            print(f'Силач {name} закончил соревнование')

async def start_tournament():
    task1 = asyncio.create_task((start_strongman('Иван', 1)))
    task2 = asyncio.create_task((start_strongman('Сергей', 3)))
    task3 = asyncio.create_task((start_strongman('Анатолий', 2)))
    await task1
    await task2
    await task3

asyncio.run(start_tournament())