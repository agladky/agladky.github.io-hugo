+++
title = "Почему стоит использовать zsh вместо bash"
date = "2015-11-26T13:10:07+03:00"
tags = ["shell"]
categories = ["Development"]
draft = true
description = "Чем zsh лучше чем bash для повседневных задач. Установка oh-my-zsh."
keywords = "zsh, zshell, bash, shell, cd, oh-my-zsh, git, aliases"
slug = "why-zsh-is-better-than-bash"
aliases = [
    "/posts/why-zsh-is-better-than-bash/",
    "/2015/11/zsh-bash.html"
]
+++

Zsh не такая уж и новая оболочка, первая версия появилась еще в 1990 году. С историей и основными особенностями можно познакомится в википедии, [русская](https://ru.wikipedia.org/wiki/Zsh) и [английская](https://en.wikipedia.org/wiki/Z_shell).

Давайте рассмотрим особенности zsh, которые покажут чем эта оболочка лучше чем bash. И почему стоит хотя бы попробовать использовать её в повседневной жизни.

### Cd completition (автодополнение)
Что происходит, если в bash набрать `cd` и нажать Tab?

![bash cd tab first](https://lh3.googleusercontent.com/-8iOm_Ix2cxE/VlawDdhnxPI/AAAAAAAAAjo/fybejZjCiJs/s640-Ic42/Screenshot%2525202015-11-23%25252009.44.27.png)

А если еще раз?

![bash cd tab second](https://lh3.googleusercontent.com/-9EtosbNV72U/VlawDQ65VCI/AAAAAAAAAkE/hQ1XsEusWbA/s640-Ic42/Screenshot%2525202015-11-23%25252009.44.47.png)

Каждый раз будет выводится только список файлов в текущей директории. Так будет продолжаться до тех пор, пока не начать вводить первые буквы в названии нужного файла, тогда мы получим отфильтрованный список. И, только если введенные данные позволяют точно определить необходимое значение, то подставится полное имя файла или папки.

Тем временем, что будет происходить в zsh при тех же действиях пользователя. Набираем `cd` и нажимаем Tab.

![zsh cd tab first](https://lh3.googleusercontent.com/-BSBLwCuwbGw/VlawDaG8oEI/AAAAAAAAAjw/dB7bM5n6iqg/s640-Ic42/Screenshot%2525202015-11-23%25252009.46.15.png)

В строку ввода подставилось первое значение из списка. Нажимаем tab еще раз.

![zsh cd tab second](https://lh3.googleusercontent.com/-Dc119BYH764/VlawD4ymcII/AAAAAAAAAkI/V7EzDl0DuJA/s640-Ic42/Screenshot%2525202015-11-23%25252009.47.34.png)

В строку ввода подставилось второе значение из списка!

Вроде бы мелочь, но позволяет быстрее производить навигацию по дереву фалов.

### Автодополнение для команд на примере git
Для cd стало ясно, zsh позволяет быстрее производить навигацию по дереву фалов. А что будет для команд, например для git.

Произведем знакомые действия. Напишем в bash `git` и нажмем tab.

![bash git tab](https://lh3.googleusercontent.com/-2XI7N9lTfA4/VlawD66cYSI/AAAAAAAAAj4/3Pi57w0iQbA/s640-Ic42/Screenshot%2525202015-11-26%25252009.32.26.png)

Никакой помощи не появляется. Только отображаются файлы данной директории.

Проделаем ту же операцию в zsh.

![zsh git tab](https://lh3.googleusercontent.com/-8dn01qWVJd4/VlawEI4aHTI/AAAAAAAAAjk/i2wF_bGGo7c/s640-Ic42/Screenshot%2525202015-11-26%25252009.33.24.png)

Что мы видим? Список команд с их описанием. Удобно!

Да, возможно получить подобное поведение для bash, например, установив пакет bash-completion. Но, все равно, не получится такой же вывод информации, как и в zsh:

* Не будет такой же итерации по значениям, как в пункте про `cd`.
* Не будет справочной информации, только список значений.

### Path expansion
Zsh поддерживает раскрытие полного пути на основе неполных данных. Введем в терминал следующий шаблон пути.

![zsh path expansion first](https://lh3.googleusercontent.com/-JkUKjONlTM0/VlawEFd1zdI/AAAAAAAAAkM/cU-dPKShFg8/s640-Ic42/Screenshot%2525202015-11-26%25252009.59.58.png)

Нажмем tab.

![zsh path expansion second](https://lh3.googleusercontent.com/-dA_uysuc3-s/VlawEcceJZI/AAAAAAAAAkA/naoYDI9fJQc/s640-Ic42/Screenshot%2525202015-11-26%25252010.00.08.png)

Путь до директории полностью раскрылся. И не пришлось вводить лишних символов.

Но что, если заданному может соответствовать несколько путей? Например, вместо `cd /u/lo/g` из примера выше напишем `cd u/l/g`. Нажмем tab.

![zsh path expansion third](https://lh3.googleusercontent.com/-RXcaxKd0UZc/VlawEQAE_II/AAAAAAAAAkQ/nePq8mG_mJc/s640-Ic42/Screenshot%2525202015-11-26%25252010.00.31.png)

Путь раскрылся до тех пор, пока не возникла неопределенность. Нажимаем tab еще раз, и перед нами предстанет та же самая картина что и в пункте про **cd completition**.

![zsh path expansion third](https://lh3.googleusercontent.com/-YvpzsGE9ZiU/VlawEt6KbRI/AAAAAAAAAjs/8J7ogcuB5YU/s640-Ic42/Screenshot%2525202015-11-26%25252010.00.46.png)

Можно так же проводить итерацию по tab пока не дойдем до нужного пункта и не выберем его. Дальнейшее нажатие tab раскроет задуманный путь до конца.

### Path replacement
Zsh поддерживает замену части пути. Рассмотрим на примере. Введем `cd /usr/local/bin`. Но подождите, я хотел  `cd /usr/local/share`!  Не проблема, вводим команду `cd bin share` и получим заветный путь. Как это выглядит в терминале:

![zsh path replacement first](https://lh3.googleusercontent.com/-P_Kx_CFBWx4/VlawEm_jwkI/AAAAAAAAAj8/F1bj2sVrwgk/s640-Ic42/Screenshot%2525202015-11-26%25252010.02.49.png)

Возможно, это не самый убедительный пример. Того же эффекта можно достичь просто написав `cd ../share`.  Но рассмотрим следующий случай:

![zsh path replacement second](https://lh3.googleusercontent.com/-_eKSxUA5xWc/VlawE9que7I/AAAAAAAAAkU/SuGQ0fm9awE/s640-Ic42/Screenshot%2525202015-11-26%25252010.05.16.png)

B bash, тут бы пришлось изрядно постараться (`cd ../../../`).

### Aliases
Обычные псевдонимы (aliases) задаются в следующем виде:
``` sh
alias ls='ls --color=auto'
```

В zsh существует еще 2 типа псевдонима, которые помогут в повседневной работе.

Первый из них – *глобальный (global)*. Основное отличие от обычного, его можно вызывать в любом месте команды. Для его определения необходимо добавить ключ `-g`.  Рассмотрим на примере:
``` sh
alias -g gp='| grep -i'

$ ps ax gp docker
=> ps ax | grep -i docker
```

Как видно, вместо того, что бы писать `| grep -i` В середине выражения, просто использовался псевдоним `gp`. Удобно.

Второй тип – суфиксный (suffix). Он позволяет описывать, в каком приложении следует открывать файл, основываясь на его расширении. Задается с помощью ключа `-s`.
``` sh
alias -s log='less -MN'
alias -s html='chromium'

$ development.log
=> less -MN development.log
$ index.html
=> chromium index.html
```

### Right prompt
Zsh позволяет настроить правую строку приглашения. Туда можно выводить, например, текущую дату, или состояние ветки в git. Иллюстрация из [книги по git](https://git-scm.com/book/tr/v2/Git-in-Other-Environments-Git-in-Zsh):

![zsh right prompt example](https://lh3.googleusercontent.com/-m6u_sxiII2k/VlbDByw8w2I/AAAAAAAAAkw/E1PlhRAqQw0/s640-Ic42/zsh-prompt.png)

### Поиск в истории по введенной подстроке
Одна из самых полезных и удобных вещей, которую позволяет делать zsh. (Включается плагином, history-substring-search в oh-my-zsh, о котором будет ниже).

Например, вводим `git pu` и нажимаем стрелку вверх

![zsh-history-substring-search](https://lh3.googleusercontent.com/-JcZi_xvm-gM/VlawE0ZiSVI/AAAAAAAAAj0/igudlxn0iDQ/s640-Ic42/Screenshot%2525202015-11-26%25252010.06.25.png)

Сразу получили последний запрос, который соответствует данной строке. Если еще раз нажать стрелку вверх, то перейдем к следующему и т.д.

### oh-my-zsh
Фреймворк для легкой настройки и установки [плагинов](https://github.com/robbyrussell/oh-my-zsh/wiki/Plugins-Overview) и [тем оформления](https://github.com/robbyrussell/oh-my-zsh/wiki/Themes). Содержит в себе уже более 200 плагинов. Проект доступен на [github](https://github.com/robbyrussell/oh-my-zsh).

Обзор некоторых плагинов, которые установлены на моем компьютере:

* git – добавляет много полезных [сокращений](https://github.com/robbyrussell/oh-my-zsh/wiki/Plugin:git) для команд git'a.
* colored-man-pages – добавляет подсветку на man страницы
* command-not-found – подсказывает название команды, если она была напечатана с ошибкой
* bwana – позволяет открывать man страницы в браузере
* sublime – псевдонимы для вызова sublime text
* history – псевдонимы для истории команд и поиска по ним
* history-substring-search – реализация поиска по истории команд как было описано выше
* docker – помощь для команд докера.

Вид одной из самых популярных тем для zsh:

![](https://cloud.githubusercontent.com/assets/2618447/6316862/70f58fb6-ba03-11e4-82c9-c083bf9a6574.png)

### Заключение
Я не сомневаюсь, что некоторое из написанного можно достигнуть с помощью различных плагинов и скриптов для bash. Но зачем? Когда уже есть хорошее решение "из коробки". Которое работает, и работает очень хорошо.
