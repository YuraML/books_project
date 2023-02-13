# Парсер книг с сайта tululu.org

Данный скрипт позволяет скачивать книги на свой компьютер напрямую с сайта [tululu.org](https://tululu.org/).

## Подготовка

Для запуска у вас уже должен быть установлен Python 3.

- Скачайте файл `books_script.py`, откройте командную строку
- Установите нужные версии библиотек, необходимых для скрипта, командой: 

```console
python -m pip install -r requirements.txt
```


## Запуск скрипта


Запустите скрипт командой:

```console
python3 books_script.py {start_id} {end_id}
```

В данном случае аргумент `start_id` - id первой книги, которой вам необходимо скачать, а `end_id` - id последней книги.

Узнать id книги можно в адресной строке страницы конкретной книги на tululu.org. 

На примере [этой](https://tululu.org/b10/) книги:

```
https://tululu.org/b10/   	#id книги идет после 'b', т.е. id книги - число 10.  	
```



Скрипт выведет названия и имена авторов книг, id которых вы указали. Затем скрипт скачает эти книги, а также обложки к ним, в случае если они доступны на сайте tululu.org.

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
