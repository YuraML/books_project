# Библиотека книг с сайта tululu.org

![Alt text](https://dvmn.org/media/image_TLlI3D8.png "books")


Сайт с книгами раздела "Научная фантастика" с сайта [tululu.org](https://tululu.org/). Помимо него вам также доступен парсер, который позволяет скачивать книги на свой компьютер напрямую с сайта.

## Сайт с книгами в жанре научной фантастики

Ознакомиться с сайтом можно [здесь](https://yuraml.github.io/books_project/pages/index1.html). Для полноценной работы сайта вам необходимо полностью скачать данный репозиторий.


## Подготовка

Для запуска у вас уже должен быть установлен Python 3.

- Скачайте код из данного репозитория, откройте командную строку
- Установите нужные версии библиотек, необходимых для скрипта, командой: 

```console
python -m pip install -r requirements.txt
```

## Сайт в офлайн режиме

Сайт с книгами также полностью функционирует без интернета. Для запуска в офлайн режиме откройте файл `index1.html` в папке `pages`.

## Сайт в локальном режиме

Для запуска веб сервера введите в консоль команду:

```console
python render_website.py --json_path
```
В этом случае `--json_path` - опциональный параметр, в котором вы можете указать путь к файлу с описанием книг.

Для просмотра сайта в локальном режиме перейдите по [этой ссылке](http://127.0.0.1:5500/pages/index1.html)

Для перехода на сайт воспользуйтесь [этой ссылкой](http://127.0.0.1:5500).

## Запуск парсера


Запустите скрипт командой:

```console
python3 parse_tululu_category.py 
```

После ввода команды начнется скачивание книг из раздела "Научная фантастика" с сайта tululu.org. Книги для скачивания берутся из [списка научно-фантастических книг](https://tululu.org/l55/1/), разделенного по страницам. 
Чтобы скачать книги с определенных страниц раздела (например с 10 по 20), введите следующую команду с опциональными аргументами:

```console
python3 parse_tululu_category.py --start_page 10 --end_page 20 
```

Для удобства работы с программой, созданы и другие опциональные аргументы. Чтобы узнать о них больше, введите команду:

```console
python3 parse_tululu_category.py --help 
```


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
