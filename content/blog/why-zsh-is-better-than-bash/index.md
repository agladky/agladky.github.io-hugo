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

Zsh не такая уж и новая оболочка, первая версия появилась еще в 1990 году. С историей и основными особенностями можно познакомиться в [русской](https://ru.wikipedia.org/wiki/Zsh) или [английской](https://en.wikipedia.org/wiki/Z_shell) википедии.

Давайте рассмотрим особенности zsh, которые покажут чем эта оболочка лучше bash. И почему стоит хотя бы попробовать использовать её в повседневной жизни.

### Автодополнение для cd
Наберем в баш `cd` и нажмем таб.

{{% imgres src="images/bash-cd-tab-first" alt="bash cd tab first" /%}}

Еще раз.

{{% imgres src="images/bash-cd-tab-second" alt="bash cd tab second" /%}}

Каждый раз будет выводиться только список файлов в текущей директории. Так продолжится пока не ввести первые буквы искомого файла, тогда отобразиться отфильтрованный список. И только если введенные данные позволяют точно определить значение, то подставится полное имя файла или папки.

Теперь наберем `cd` в zsh и нажмем таб.

{{% imgres src="images/zsh-cd-tab-first" alt="zsh cd tab first" /%}}

В строку ввода подставилось первое значение из списка. Нажимаем таб еще раз.

{{% imgres src="images/zsh-cd-tab-second" alt="zsh cd tab second" /%}}

Подставилось второе значение из списка! Удобно.

### Автодополнение для команд на примере git
Введем в баш `git` и нажмем таб.

{{% imgres src="images/bash-git-tab" alt="bash git tab" /%}}

Никакой помощи не появилось. Только отображаются файлы данной директории.

Проделаем ту же операцию в zsh.

{{% imgres src="images/zsh-git-tab" alt="zsh git tab" /%}}

Отобразился список команд с описанием. Это гораздо информативнее.

Да, установив пакет bash-completion, подобное поведение появится и в баше. Но выводить информацию как в zsh не получится:

* Не будет итерации по значениям, как в пункте про `cd`;
* Не будет справочной информации, только список значений.

### Раскрытие полного пути
Zsh поддерживает раскрытие полного пути на основе неполных данных. Введем шаблон пути:

{{% imgres src="images/zsh-path-expansion-first" alt="zsh path expansion first" /%}}

Нажмем tab.

{{% imgres src="images/zsh-path-expansion-second" alt="zsh path expansion second" /%}}

Путь до директории полностью раскрылся. Не пришлось вводить лишних символов.

Но что, если заданному пути соответствует несколько путей? Введем `cd u/l/g` и нажмем таб.

{{% imgres src="images/zsh-path-expansion-third" alt="zsh path expansion third" /%}}

Путь раскрылся до возникновения неопределенности. Нажимаем таб еще раз, и перед нами предстанет выбор папки.

{{% imgres src="images/zsh-path-expansion-fourth" alt="zsh path expansion fourth" /%}}

Выбираем табом нужную папку. Последующее нажатие таба раскроет задуманный путь до конца.

### Замена пути
Zsh поддерживает замену части пути. Рассмотрим на примере. Введем `cd /usr/local/bin`. Но подождите, я хотел `cd /usr/local/share`! Не проблема, вводим команду `cd bin share` и получаем заветный путь:

{{% imgres src="images/zsh-path-replacement-first" alt="zsh path replacement first" /%}}

Возможно, это не самый убедительный пример. Того же эффекта можно достичь просто написав `cd ../share`. Но рассмотрим следующий случай:

{{% imgres src="images/zsh-path-replacement-second" alt="zsh path replacement second" /%}}

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

Второй тип — *суффиксный (suffix)*. Указывает в каком приложении открывать файл, основываясь на расширении. Задается ключом `-s`.
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

{{% imgres src="images/zsh-right-prompt-example" alt="zsh right prompt example" /%}}

### Поиск в истории по подстроке
Одна из самых кайфовых вещей, которую позволяет делать zsh. (Включается плагином, history-substring-search в oh-my-zsh, о котором ниже).

Например, вводим `git pu` и нажимаем стрелку вверх.

{{% imgres src="images/zsh-history-substring-search" alt="zsh history substring search" /%}}

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

{{% imgres src="images/popular-zsh-theme" alt="popular zsh theme" /%}}

### Заключение
Я не сомневаюсь, что многое из написанного можно достигнуть с помощью различных плагинов и скриптов для баша. Но зачем если есть хорошее решение «из коробки». Которое работает, и работает очень хорошо.
