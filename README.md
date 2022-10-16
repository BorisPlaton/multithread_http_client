# Multithread HTTP Client
It is my solution to a test task I have found in the Internet. The text of the task is in Russian:
```
Реализовать многопоточный HTTP клиент + websocket сервер.
1) Клиенту передается URL, каждый поток скачивает X байт параллельно другим, кол-во потоков и кол-во байт на поток ограничено сверху посредством конфига. При передаче URL клиенту, нужно проверить, поддерживаются ли ranges.
2) websocket - сервер, отдает список URL для скачивания, и их статус (размер, потоков запущено на обработку, прогресс), если контент скачан, то ссылку на файловую систему по протоколу file:///
```

## How it works
This project consists of two parts. First is a Websocket server that accepts new connections and URLs that must be downloaded. Second is a multithread HTTP-client that downloads the content of given URL, if all conditions to do it is matched. If content is downloaded, you will see it in your file system as file. Project doesn't require any databases or some message-brokers.

## Creating a virtual environment
Go to the root directory of the project. Execute the following commands in the terminal to install a virtual environment and to activate it.
```
$ virtualenv --python=3.10.4 venv
$ ./venv/bin/activate
$ pip install -r requirements.txt
```

## Start a Websocket server
Go to the `src` directory and run the following command:
```
$ python main.py
```
It will start the server and will spawn background workers

## Connect to the server
You can connect to the server via a `Postman` or using a `websocket` package that is used in this project. If you hadn't changed a `HOST` and a `PORT` default value in the `settings.py`, you would print the following command in your terminal:
```
$ python -m websockets ws://localhost:8888/
```
After this you can send a URL that must be downloaded. You must send it as a JSON. For example:
```
> {"url": "https://www.gravatar.com/avatar/17539586d5bb4e528d94f3bc4131e6c0?s=23&d=identicon&r=PG"}
> {"data": {"message": "URL has been added."}}
```
You will receive a message that the URL has been added. After a while you will receive a following message:
```
{
    "data": [
        {"url": "https://www.gravatar.com/avatar/17539586d5bb4e528d94f3bc4131e6c0?s=23&d=identicon&r=PG", 
        "path_to_file": "file:///home/kirill/projects/python/multithread_client/downloaded_content/7a7c2c92-1664-4615-b455-3ff052c893ef", 
        "process_status": "Downloaded"}
    ]
}
```
It means the content of requested URL was downloaded. You have a path to file which contains it.

## Configuration
You also have the `config.py` file in the `src/settings/` directory. You can specify a content directory which will contain: 
1. All downloaded data - `CONTENT_DIRECTORY`
2. A workers amount - `THREADS_AMOUNT`
3. A bytes amount that is downloaded by one worker - `BYTES_AMOUNT`
4. How often URLs' statuses are broadcasted among all existing connections - `BROADCAST_TIMEOUT`
5. Host and Port of Websocket server - `HOST`, `PORT`







