+++
title = "Почему стоит использовать zsh вместо bash"
date = "2015-11-26T13:10:07+03:00"
tags = ["shell"]
categories = ["Development"]
draft = false
description = "Чем zsh лучше чем bash для повседневных задач. Установка oh-my-zsh."
keywords = "zsh, zshell, bash, shell, cd, oh-my-zsh, git, aliases"
slug = "why-zsh-is-better-than-bash"
aliases = [
    "/posts/why-zsh-is-better-than-bash/",
    "/2015/11/zsh-bash.html"
]
+++

Zsh не такая уж и новая оболочка, первая версия появилась еще в 1990 году. С историей и основными особенностями можно познакомится в [русской](https://ru.wikipedia.org/wiki/Zsh) или [английской](https://en.wikipedia.org/wiki/Z_shell) википедии.

Давайте рассмотрим особенности zsh, которые покажут чем эта оболочка лучше bash. И почему стоит хотя бы попробовать использовать её в повседневной жизни.

### Автодополнение для cd
Наберем в баш `cd` и нажмем таб.

![bash cd tab first](https://lh3.googleusercontent.com/-8iOm_Ix2cxE/VlawDdhnxPI/AAAAAAAAAjo/fybejZjCiJs/s640-Ic42/Screenshot%2525202015-11-23%25252009.44.27.png)

Еще раз.

![bash cd tab second](https://lh3.googleusercontent.com/-9EtosbNV72U/VlawDQ65VCI/AAAAAAAAAkE/hQ1XsEusWbA/s640-Ic42/Screenshot%2525202015-11-23%25252009.44.47.png)

Каждый раз будет выводится только список файлов в текущей директории. Так продолжится пока не ввести первые буквы искомого файла, тогда отобразиться отфильтрованный список. И, только если введенные данные позволяют точно определить значение, то подставится полное имя файла или папки.

Теперь наберем `cd` в zsh и нажмем таб.

![zsh cd tab first](https://lh3.googleusercontent.com/-BSBLwCuwbGw/VlawDaG8oEI/AAAAAAAAAjw/dB7bM5n6iqg/s640-Ic42/Screenshot%2525202015-11-23%25252009.46.15.png)

В строку ввода подставилось первое значение из списка. Нажимаем таб еще раз.

![zsh cd tab second](https://lh3.googleusercontent.com/-Dc119BYH764/VlawD4ymcII/AAAAAAAAAkI/V7EzDl0DuJA/s640-Ic42/Screenshot%2525202015-11-23%25252009.47.34.png)

Подставилось второе значение из списка! Удобно.

### Автодополнение для команд на примере git
Введем в баш `git` и нажмем таб.

![bash git tab](https://lh3.googleusercontent.com/-2XI7N9lTfA4/VlawD66cYSI/AAAAAAAAAj4/3Pi57w0iQbA/s640-Ic42/Screenshot%2525202015-11-26%25252009.32.26.png)

Никакой помощи не появилось. Только отображаются файлы данной директории.

Проделаем ту же операцию в zsh.

![zsh git tab](https://lh3.googleusercontent.com/-8dn01qWVJd4/VlawEI4aHTI/AAAAAAAAAjk/i2wF_bGGo7c/s640-Ic42/Screenshot%2525202015-11-26%25252009.33.24.png)

Отобразился список команд с описанием. Это гораздо информативнее.

Да, установив пакет bash-completion подобное поведение появится и в баше. Но выводить информацию как в zsh не получится:

* Не будет итерации по значениям, как в пункте про `cd`;
* Не будет справочной информации, только список значений.

### Раскрытие полного пути
Zsh поддерживает раскрытие полного пути на основе неполных данных. Введем шаблон пути:

![zsh path expansion first](https://lh3.googleusercontent.com/-JkUKjONlTM0/VlawEFd1zdI/AAAAAAAAAkM/cU-dPKShFg8/s640-Ic42/Screenshot%2525202015-11-26%25252009.59.58.png)

Нажмем tab.

![zsh path expansion second](https://lh3.googleusercontent.com/-dA_uysuc3-s/VlawEcceJZI/AAAAAAAAAkA/naoYDI9fJQc/s640-Ic42/Screenshot%2525202015-11-26%25252010.00.08.png)

Путь до директории полностью раскрылся. Не пришлось вводить лишних символов.

Но что, если заданному пути соответствует несколько путей? Введем `cd u/l/g` и нажмем таб.

![zsh path expansion third](https://lh3.googleusercontent.com/-RXcaxKd0UZc/VlawEQAE_II/AAAAAAAAAkQ/nePq8mG_mJc/s640-Ic42/Screenshot%2525202015-11-26%25252010.00.31.png)

Путь раскрылся до возникновения неопределенности. Нажимаем таб еще раз, и перед нами предстанет выбор папки.

![zsh path expansion third](https://lh3.googleusercontent.com/-YvpzsGE9ZiU/VlawEt6KbRI/AAAAAAAAAjs/8J7ogcuB5YU/s640-Ic42/Screenshot%2525202015-11-26%25252010.00.46.png)

Выбираем табом нужную папку. Последующее нажатие таба раскроет задуманный путь до конца.

### Замена пути
Zsh поддерживает замену части пути. Рассмотрим на примере. Введем `cd /usr/local/bin`. Но подождите, я хотел `cd /usr/local/share`! Не проблема, вводим команду `cd bin share` и получаем заветный путь:

![zsh path replacement first](https://lh3.googleusercontent.com/-P_Kx_CFBWx4/VlawEm_jwkI/AAAAAAAAAj8/F1bj2sVrwgk/s640-Ic42/Screenshot%2525202015-11-26%25252010.02.49.png)

Возможно, это не самый убедительный пример. Того же эффекта можно достичь просто написав `cd ../share`. Но рассмотрим следующий случай:

![zsh path replacement second](https://lh3.googleusercontent.com/-_eKSxUA5xWc/VlawE9que7I/AAAAAAAAAkU/SuGQ0fm9awE/s640-Ic42/Screenshot%2525202015-11-26%25252010.05.16.png)

B баш тут бы пришлось изрядно постараться (`cd ../../../`).

### Псевдонимы
Обычные псевдонимы задаются так:
``` sh
alias ls=’ls —color=auto’
```

В zsh существует еще 2 типа псевдонима.

Первый — *глобальный (global)*. Может вызываться в любом месте команды. Задается ключом `-g`.
``` sh
alias -g gp='| grep -i'

$ ps ax gp docker
=> ps ax | grep -i docker
```

В примере, вместо написания `| grep -i`, в середине выражения, использовался псевдоним `gp`. Удобно.

Второй тип — *суфиксный (suffix)*. Указывает в каком приложении открывать файл, основываясь на расширении. Задается ключом `-s`.
``` sh
alias -s log='less -MN'
alias -s html='chromium'

$ development.log
=> less -MN development.log
$ index.html
=> chromium index.html
```

### Правая строка
Zsh позволяет настроить правую строку приглашения. Туда можно выводить текущую дату, состояние ветки в git и многое другое. Иллюстрация из [книги Pro Git](https://git-scm.com/book/tr/v2/Git-in-Other-Environments-Git-in-Zsh):

![zsh right prompt example](https://lh3.googleusercontent.com/-m6u_sxiII2k/VlbDByw8w2I/AAAAAAAAAkw/E1PlhRAqQw0/s640-Ic42/zsh-prompt.png)

### Поиск в истории по подстроке
Одна из самых кайфовых вещей, которую позволяет делать zsh. (Включается плагином, history-substring-search в oh-my-zsh, о котором ниже).

Например, вводим `git pu` и нажимаем стрелку вверх.

![zsh-history-substring-search](https://lh3.googleusercontent.com/-JcZi_xvm-gM/VlawE0ZiSVI/AAAAAAAAAj0/igudlxn0iDQ/s640-Ic42/Screenshot%2525202015-11-26%25252010.06.25.png)

Получили последний запрос, который соответствует введенному шаблону. Дальнейшие нажатия будут выводить следующий результат. Удобно, что для поиска совершаются минимальные действия.

### oh-my-zsh
Фреймворк для легкой настройки и установки [плагинов](https://github.com/robbyrussell/oh-my-zsh/wiki/Plugins-Overview) и [тем оформления](https://github.com/robbyrussell/oh-my-zsh/wiki/Themes). Содержит в себе уже более 200 плагинов. Проект доступен на [github](https://github.com/robbyrussell/oh-my-zsh).

Плагины которыми я пользуюсь:
* _git_ — добавляет много полезных [сокращений](https://github.com/robbyrussell/oh-my-zsh/wiki/Plugin:git) для команд гита.
* _colored-man-pages_ — добавляет подсветку на man страницы
* _command-not-found_ — подсказывает название команды, если она напечатана с ошибкой
* _bwana_ — позволяет открывать man страницы в браузере
* _sublime_ — псевдонимы для вызова sublime text
* _history_ — псевдонимы для истории команд и поиска по ним
* _history-substring-search_ — реализация поиска в истории по подстроке
* _docker_ — помощь для команд докера.

Вид популярной темы для zsh:

![](https://cloud.githubusercontent.com/assets/2618447/6316862/70f58fb6-ba03-11e4-82c9-c083bf9a6574.png)

### Заключение
Я не сомневаюсь, что многое из написанного можно достигнуть с помощью различных плагинов и скриптов для баша. Но зачем если есть хорошее решение «из коробки». Которое работает, и работает очень хорошо.
