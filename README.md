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
  hugo server --verbose
  ```

Установка зависимостей
  ```sh
  npm ci
  ```

Деплой происходит автоматически c помощью GitHub Actions

![CD](https://github.com/agladky/agladky.github.io-hugo/workflows/CD/badge.svg)
