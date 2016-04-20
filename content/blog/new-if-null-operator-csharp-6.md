+++
title = "Новый оператор ?. в C# 6"
date = "2016-02-17T13:10:07+03:00"
tags = [".net"]
categories = ["Development"]
draft = true
description = "Использование оператора ?. с цепочкой вызова, индексатором и делегатами. Комбинация с ??"
keywords = "?., C#, C# 6, csharp, .net. оператор, null, проверка на null, ??"
aliases = [
    "/posts/new-if-null-operator-csharp-6/",
    "/2016/02/c-6.html"
]
+++

Одно из нововведений в С# 6 это оператор `?.`. Давайте рассмотрим, где и как его использовать.

### Цепочка вызовов

Новый оператор позволяет уменьшить количество проверок на `null` в цепочке вызовов. Например:

``` csharp
var documentName = taskManager.CurrentTask == null ? null :
  (taskManager.CurrentTask.GetDocument() == null ? null :
    taskManager.CurrentTask.GetDocument().Name);
```

можно записать в одну строчку используя оператор `?.`

``` csharp
var documentName = taskManager.CurrentTask?.GetDocument()?.Name;
```

`documentName` будет присвоено значение `null`, если кто-либо из `CurrentTask`, `GetDocument()` или `Name` вернет `null`.

Во втором варианте код стал чище. Так же, в первом блоке кода метод `GetDocument()` вызывается два раза, в то время как во втором блоке только один раз. Для реализации подобного поведения без использования `?.` необходима дополнительная переменная, для сохранения значения из `GetDocument()`.

### Использование с индексатором

Рассмотрим задачу получения значения из коллекции по индексу, с проверкой набора значений на `null`:

``` csharp
var tasks = (taskManager.Tasks != null) ? taskManager.Tasks[index] : null;
```

Теперь, вместо явной проверки на `null` перед индексацией коллекции, можно воспользоваться новым оператором:

``` csharp
var tasks = taskManager.Tasks?[index];
```

### Типы значений и оператор ?.

Как известно, возвращаемый тип функции `String.Equals()` – `bool`. Скомпилируется ли следующий код?

``` csharp
public void Main()
{
  String str = "x";
  bool result = str?.Equals("x");
}
```

Ответ - нет. Возникнет следующая ошибка: `Cannot implicitly convert type 'bool?' to 'bool'`. Такое поведение ожидаемо, так как `str?.Equals("x")` вернет `null` если переменная `str` не инициализирована и значение типа `bool` в остальных случаях.

Для всех операций, возвращающих типы значений, итоговый тип превратится в соответствующий `Nullable<T>` тип.

### Использование в условии

Допустим, необходимо проверить коллекцию на наличие в ней хотя бы одного элемента. Рассмотрим типичный код:

``` csharp
if (taskManager.Tasks != null && taskManager.Tasks.Any())
  Console.Write("Tasks has items!");
```

Попробуем переписать:

``` csharp
// Ошибка!
if (taskManager.Tasks?.Any())
  Console.Write("Tasks has items!");
```

Возникнет ошибка! Как было указано в предыдущем пункте, конструкция `taskManager.Tasks?.Any()` вернет `Nullable<bool>` тип, который нельзя однозначно трактовать в условии `if`. Поэтому, дополним код:

``` csharp
if (taskManager.Tasks?.Any() == true)
  Console.Write("Tasks has items!");
```

Теперь все работает как надо и на одно условие стало меньше. Так же, используя знания из следующего пункта, можно написать эквивалентный код:

``` csharp
if (taskManager.Tasks?.Any() ?? false)
  Console.Write("Tasks has items!");
```

### Комбинация с оператором ??

Оператор `??` используется для предоставления значения по умолчанию, если результат операции возвращает `null`.

``` csharp
var documentName = taskManager.CurrentTask?.GetDocument()?.Name ?? "No Name";
```

В случае, если `CurrentTask`, `GetDocument()` или `Name` вернет `null`, то переменной будет присвоено значение `"No Name"`.

### Использование с делегатами

До появления оператора `?.` код для вызова делегата обычно писали так:

``` csharp
var handler = this.PropertyChanged;
if (handler != null)
  handler(…)
```

Теперь, вызов можно написать в одной строчке:

``` csharp
PropertyChanged?.Invoke(e)
```

Компилятор создает код для вычисления PropertyChanged только один раз, запоминая результат во временной переменной.

Обратите внимание, следующий код вызовет ошибку:

``` csharp
PropertyChanged?(e)
```

Необходимо явно вызывать метод `Invoke`.

### Полезные ссылки

* [Оператор ??](https://msdn.microsoft.com/ru-ru/library/ms173224.aspx)
* [Операторы ?. и ?](https://msdn.microsoft.com/ru-RU/library/dn986595.aspx)
* [Новый и более совершенный C# 6.0](https://msdn.microsoft.com/ru-ru/magazine/dn802602.aspx)
