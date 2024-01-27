import asyncio
import aiohttp
import threading
import requests
import os
import time
from multiprocessing import Process

URLS = ['https://i.pinimg.com/originals/ae/52/51/ae52514ccb20bfa9c1b468638e95f1f9.jpg',
        'https://w.forfun.com/fetch/4a/4af0bcc2b0c34fd573eca9f1be9ab245.jpeg',
        'https://gas-kvas.com/uploads/posts/2023-02/1675489758_gas-kvas-com-p-izobrazheniya-i-kartinki-na-fonovii-risuno-41.jpg',
        'https://w.forfun.com/fetch/29/2942cda3da91073bcaf9915bec9195d5.jpeg',
        'https://proprikol.ru/wp-content/uploads/2019/10/delfiny-krasivye-kartinki-27.jpg',
        ]


def downloads():
    folder = 'picture_sync'
    if not os.path.exists(folder):
        os.mkdir(folder)
    for url in URLS:
        filename = os.path.join(folder, os.path.basename(url))
        download_data(url, filename)


def download_data(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)


async def async_download_data(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            pict = await response.read()
            with open(filename, 'wb') as f:
                f.write(pict)


if __name__ == '__main__':

    start_time = time.time()
    downloads()
    print(f'sync {time.time() - start_time:.2f}')

    threads = []
    start_time = time.time()
    folder = 'picture_thread'
    if not os.path.exists(folder):
        os.mkdir(folder)
    for url in URLS:
        filename = os.path.join(folder, os.path.basename(url))
        thread = threading.Thread(target=download_data, args=[url, filename])
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print(f'threads {time.time() - start_time:.2f}')

    proces = []
    start_time = time.time()
    folder = 'picture_proc'
    if not os.path.exists(folder):
        os.mkdir(folder)
    for url in URLS:
        filename = os.path.join(folder, os.path.basename(url))
        proc = Process(target=download_data, args=[url, filename])
        proces.append(proc)
        proc.start()
    for proc in proces:
        proc.join()
    print(f'proc {time.time() - start_time:.2f}')

    tasks = []
    start_time = time.time()
    folder = 'picture_task'
    if not os.path.exists(folder):
        os.mkdir(folder)
    for url in URLS:
        filename = os.path.join(folder, os.path.basename(url))
        task = asyncio.ensure_future(async_download_data(url, filename))
        tasks.append(task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    print(f'async {(time.time() - start_time):.2f}')

