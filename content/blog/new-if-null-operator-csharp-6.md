+++
title = "Новый оператор ?. в C# 6"
date = "2016-02-17T13:10:07+03:00"
tags = [".net"]
categories = ["Development"]
draft = false
description = "Использование оператора ?. с цепочкой вызова, индексатором и делегатами. Комбинация с ??"
keywords = "?., C#, C# 6, csharp, .net. оператор, null, проверка на null, ??"
slug = "new-if-null-operator-csharp-6"
aliases = [
    "/posts/new-if-null-operator-csharp-6/",
    "/2016/02/c-6.html"
]
+++

Одно из нововведений в С# 6 — оператор `?.`. Давайте рассмотрим, где и как его использовать.

### Преобразование цепочки вызовов
С новым оператором уменьшается количество проверок на `null` в цепочке вызовов:
``` csharp
var documentName = taskManager.CurrentTask == null ? null :
  (taskManager.CurrentTask.GetDocument() == null ? null :
    taskManager.CurrentTask.GetDocument().Name);
```

Перепишем в одну строчку используя `?.`:
``` csharp
var documentName = taskManager.CurrentTask?.GetDocument()?.Name;
```

`documentName` примет значение `null`, если `CurrentTask`, `GetDocument()` или `Name` вернет `null`.

Второй вариант компактнее. Так же, в первом блоке кода метод `GetDocument()` вызывается два раза, а во втором — один. Для реализации подобного поведения без использования `?.` нужна дополнительная переменная для сохранения значения из `GetDocument()`.

### Использование с индексатором
Рассмотрим получение значения из коллекции по индексу, с проверкой набора значений на `null`:
``` csharp
var tasks = (taskManager.Tasks != null) ? taskManager.Tasks[index] : null;
```

С новым оператором проверка на `null` условным оператором не расписывается. Бонус — выражение в 2 раза короче:
``` csharp
var tasks = taskManager.Tasks?[index];
```

### Оборачивание в нулевые типы
Результат выполнения `String.Equals()` — `bool`. Скомпилируется ли следующий код?
``` csharp
public void Main()
{
  String str = "x";
  bool result = str?.Equals("x");
}
```

Нет. Возникнет ошибка: `Cannot implicitly convert type ’bool?’ to ’bool’`. Такое поведение ожидаемо, так как `str?.Equals("x")` вернет `null` если переменная `str` не инициализирована и `bool` в остальных случаях.

В подобных ситуациях, при использовании оператора `?.`, возвращаемый тип функции `T` будет оборачиваться в `Nullable<T>`.

### Использование в условии
Есть задача — проверить коллекцию на наличие в ней элементов. Типичный код:
``` csharp
if (taskManager.Tasks != null && taskManager.Tasks.Any())
  Console.Write("Tasks has items!");
```

Попробуем переписать:
``` csharp
if (taskManager.Tasks?.Any())
  Console.Write("Tasks has items!");
```

Код не скомпилируется. Как написано в предыдущем пункте, `taskManager.Tasks?.Any()` вернет `Nullable<bool>` тип, который нельзя однозначно трактовать в условии `if`. Дополним код:
``` csharp
if (taskManager.Tasks?.Any() == true)
  Console.Write("Tasks has items!");
```

Работает. И на одно условие стало меньше.

Комбинируя с оператором `??` перепишем в эквивалентный код:
``` csharp
if (taskManager.Tasks?.Any() ?? false)
  Console.Write("Tasks has items!");
```

### Комбинация с оператором ??
Оператор `??` называется оператором объединения со значением `null`. Если операция возвращает `null`, оператор `??` подставит значение из правой части выражения.

``` csharp
var documentName = taskManager.CurrentTask?.GetDocument()?.Name ?? "No Name";
```

Если `CurrentTask`, `GetDocument()` или `Name` вернет `null`, то переменная примет значение `"No Name"`.

### Использование с делегатами
Стандартный код для вызова делегата:
``` csharp
var handler = this.PropertyChanged;
if (handler != null)
  handler(…)
```

Используя `?.`, больше не надо каждый раз писать такой код, делегат вызывается одной строкой:
``` csharp
PropertyChanged?.Invoke(e)
```

Компилятор создает код для вычисления PropertyChanged только один раз, запоминая результат во временной переменной.

Обратите внимание, следующий код вызовет ошибку:
``` csharp
PropertyChanged?(e)
```

Вызов метода `Invoke` обязателен.

### Полезные ссылки
* [Оператор ??](https://msdn.microsoft.com/ru-ru/library/ms173224.aspx)
* [Операторы ?. и ?](https://msdn.microsoft.com/ru-RU/library/dn986595.aspx)
* [Новый и более совершенный C# 6.0](https://msdn.microsoft.com/ru-ru/magazine/dn802602.aspx)
