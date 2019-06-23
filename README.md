## Описание
Код и данные для персонального сайта на [Hugo](http://gohugo.io/).

Результат — [репозиторий](https://github.com/agladky/agladky.github.io) со статическим сайтом работающим с помошью [GitHub Pages](https://pages.github.com/) по адресу [agladky.ru](https://agladky.ru/).

## Установка и обновление hugo
[Инструкция по установке hugo.](https://gohugo.io/getting-started/installing/)

Обновление hugo на macOs:
  ```sh
  brew update && brew upgrade hugo
  ```

## Запуск и деплой
Запуск сервера hugo для разработки
  ```sh
  hugo server -verbose
  ```

Установка необходимых зависимостей
  ```sh
  npm install -g postcss-cli autoprefixer sass
  ```

Команда запуска процесса для преобразования scss в css
  ```sh
  sass --watch dev/scss:static/css
  ```

Деплой происходит автоматически c помощью drone.io

[![Build Status](https://cloud.drone.io/api/badges/agladky/agladky.github.io-hugo/status.svg)](https://cloud.drone.io/agladky/agladky.github.io-hugo)
