+++
title = "Что такое монады на примере C#"
date = "2016-01-27T13:10:07+03:00"
tags = [".net", "functional"]
categories = ["Development"]
draft = false
description = "Краткий перевод статьи Эрика Липперта о реализации монад в .net на примере c#"
keywords = "Монад, монады, c#, функциональное, программирование, bind, util, haskell, Nullable, func, IEnumerable"
slug = "what-is-a-monad-on-csharp-example"
aliases = [
    "/posts/what-is-a-monad-on-csharp-example/",
    "/2016/01/c.html"
]
+++

Конспект — вольный перевод одного из лучших циклов статей о монадах. Эрик Липперт, на протяжении 13 глав, отвечает на вопрос:

> Я C# разработчик без опыта в «функциональном программировании». Что такое «монада» и как можно её использовать для себя?

Оригинальный цикл статей доступна по [тегу monads](http://ericlippert.com/category/monads/).

### Часть первая
Монада в функциональном программировании — абстракция линейной цепочки связанных вычислений. Её основное назначение — инкапсуляция функций с побочным эффектом от чистых функций, а точнее их выполнений от вычислений. (Определение из википедии).

«Шаблон монады» это еще один шаблон для типов. Как, например, одиночка (синглтон).

### Часть вторая
- `Nullable<T>` — представляет объект типа T, который может быть `null` (в дальнейшем, подразумевается что `Nullable<T>` может работать с любым типом данных).
- `Func<T>` — представляет объект типа T, который будет вычислен отложено (в дальнейшем, для бльшей ясности, будет использоваться делегат `delegate T OnDemand<T>();`).
- `Lazy<T>` — представляет объект типа T, который будет вычислен отложено в первый раз, а после, закеширован.
- `Task<T>` — представляет объект типа T, который будет вычислен асинхронно и будет доступен в будущем, если уже не вычислен.
- `IEnumerable<T>` — представляет упорядоченную, доступную только для чтения последовательность от нуля и более элементов типа T.

### Часть третья
Первое требование для монад: «если `M<T>` это тип-монада, тогда должен быть простой путь по превращению любого значение типа `T` в значение типа `M<T>`». Например:
``` csharp
static Nullable<T> CreateSimpleNullable<T>(T item) { return new Nullable<T>(item); }
static OnDemand<T> CreateSimpleOnDemand<T>(T item) { return () => item; }
static IEnumerable<T> CreateSimpleSequence<T>(T item) { yield return item; }
```

Кажется, что второе требование просто сформулировать: «из монады `M<T>`можно получить значение типа `T`». Но не все так однозначно. Начнем с очень специфичного вопроса. Можно легко прибавить единицу к целочисленному типу, но как «прибавить единицу» к типу-монаде обернутого вокруг целочисленного типа?

Для `Nullable<T>`:
``` csharp
static Nullable<int> AddOne(Nullable<int> nullable)
{
  if (nullable.HasValue)
  {
    int unwrapped = nullable.Value;
    int result = unwrapped + 1;
    return CreateSimpleNullable(result);
  }
  else  
    return new Nullable<int>();
}
```

Т.е. можно развернуть, произвести операцию и завернуть? Не совсем, если проделать ту же операцию для `OnDemand<T>()`, который обернут вокруг `DateTime.Now.Seconds`, то получится статическое значение. Поэтому проделанную операцию вместе с разворачиванием необходимо завернуть в функцию, как показано здесь:
``` csharp
static OnDemand<int> AddOne(OnDemand<int> onDemand)
{
  return () =>
  {
    int unwrapped = onDemand();
    int result = unwrapped + 1;
    return result;
  };
}
```

Т.е. тип монады по требованию, не просто оболочка вокруг значения. Она производит объект, структура которого кодирует последовательность операций, которые будут происходить по требованию. Это одна из особенностей, которая делает монады полезными. Но об этом позже.

Для `Lazy<T>`:
``` csharp
static Lazy<int> AddOne(Lazy<int> lazy)
{
  return new Lazy<int>(() =>
  {
    int unwrapped = lazy.Value;
    int result = unwrapped + 1;
    return result;
  });
}
```

Для `Task<T>`:
``` csharp
async static Task<int> AddOne(Task<int> task)
{
  int unwrapped = await task;
  int result = unwrapped + 1;
  return result;
}
```

И, наконец, для `IEnumerable<T>`:
``` csharp
static IEnumerable<int> AddOne(IEnumerable<int> sequence)
{
  foreach(int unwrapped in sequence)
  {
    int result = unwrapped + 1;
    yield return result;
  }
}
```

Таким образом, одно из полезных правил для шаблона монад — добавление единицы к завернутому целочисленному типу производит другой завернутый целочисленный тип, с сохранением всех особенностей.

### Часть четвертая
Напишем метод, который позволит делать оболочку над любыми `Nullable<T>` функциями, а не только операцией по добавлению единицы:
``` csharp
static Nullable<T> ApplyFunction<T>(
  Nullable<T> nullable,
  Func<T, T> function)
{
  if (nullable.HasValue)
  {
    T unwrapped = nullable.Value;
    T result = function(unwrapped);
    return new Nullable<T>(result);
  }
  else
    return new Nullable<T>();
}
```

Теперь метод `AddOne(...)` будет выглядеть так:
``` csharp
static Nullable<int> AddOne(Nullable<int> nullable)
{
  return ApplyFunction(nullable, (int x) => x + 1);
}
```

Но, допустим мы хотим функцию которая принимает тип `int` и возвращает `double`. Например, поделить 2 целых числа и получить результат типа `double`. Для этого, перепишем метод `ApplyFunction` в следующий вид:
``` csharp
static Nullable<R> ApplyFunction<A, R>(
  Nullable<A> nullable,
  Func<A, R> function)
{
  if (nullable.HasValue)
  {
    A unwrapped = nullable.Value;
    R result = function(unwrapped);
    return new Nullable<R>(result);
  }
  else
    return new Nullable<R>();
}
```

Для остальных типов, можно сделать по аналогии. По сути, получился способ превращения типов из `A` в `R` в монадические типы из `М<А>` в `М<R>` такие, что сохраняется действие функции и значения предоставляемые в монадическом («расширенном») типе.

### Часть пятая
Ранее было указано, что можно взять любую функцию с одним параметром и любым не пустым возвращаемым типом и применить эту функцию к монаде с возвращаемым типом `M<R>`. Любой возвращаемый тип, так? Предположим, что есть функция с одним параметром:
``` csharp
static Nullable<double> SafeLog(int x)
{
  if (x > 0)
    return new Nullable<double>(Math.Log(x));
  else
    return new Nullable<double>();
}
```

Обычная функция с одним параметром. Значит, ее можно применить к `Nullable<int>` и получить обратно... `Nullable<Nullable<double>>`! Это неправильно.

Создадим новую версию `ApplyFunction`, которая избегает описанной проблемы:
``` csharp
static Nullable<R> ApplySpecialFunction<A, R>(
  Nullable<A> nullable,
  Func<A, Nullable<R>> function)
{
  if (nullable.HasValue)
  {
    A unwrapped = nullable.Value;
    Nullable<R> result = function(unwrapped);
    return result;
  }
  else
    return new Nullable<R>();
}
```

Просто, не так ли? Создадим функции для остальных операторов:
``` csharp
static OnDemand<R> ApplySpecialFunction<A, R>(
  OnDemand<A> onDemand,
  Func<A, OnDemand<R>> function)
{
  return () =>
  {
    A unwrapped = onDemand();
    OnDemand<R> result = function(unwrapped);
    return result();
  };
}

static Lazy<R> ApplySpecialFunction<A, R>(
  Lazy<A> lazy,
  Func<A, Lazy<R>> function)
{
  return new Lazy(() =>
  {
    A unwrapped = lazy.Value;
    Lazy<R> result = function(unwrapped);
    return result.Value;
  };
}

static async Task<R> ApplySpecialFunction<A, R>(
  Task<A> task,
  Func<A, Task<R>> function)
{
  A unwrapped = await task;
  Task<R> result = function(unwrapped);
  return await result;
}

static IEnumerable<R> ApplySpecialFunction<A, R>(
  IEnumerable<A> sequence,
  Func<A, IEnumerable<R>> function)
{
  foreach(A unwrapped in sequence)
  {
    IEnumerable<R> result = function(unwrapped);
    foreach(R r in result)
      yield return r;
  }
}
```

В итоге, для «шаблона монады» имеются 3 правила:

1. Всегда существует возможность преобразовать тип `T` в тип `M<T>`.
   ``` csharp
   static M<T> CreateSimpleM<T>(T value)
   ```

2. Если существует функция преобразующая `A` в `R`, тогда можно применить эту функцию к экземпляру `M<A>` и получить экземпляр `M<R>`.
   ``` csharp
   static M<R> ApplyFunction<A, R>(
   M<A> wrapped,
   Func<A, R> function)
   ```

3. Если существует функция преобразующая `A` в `M<R>`, тогда можно применить эту функцию к экземпляру `M<A>` и получить экземпляр `M<R>`.
   ``` csharp
   static M<R> ApplySpecialFunction<A, R>(
   M<A> wrapped,
   Func<A, M<R>> function)
   ```

Но, правило 2 является частным случаем правила 3. Его можно представить в как комбинацию 1 и 3 правила:
``` csharp
static M<R> ApplyFunction<A, R>(
  M<A> wrapped,
  Func<A, R> function)
{
  return ApplySpecialFunction<A, R>(
    wrapped,
    (A unwrapped) => CreateSimpleM<R>(function(unwrapped)));
}
```

Остается всего два правила. Они являются полными правилами «шаблона монады»? В принципе, да.

### Часть шестая
Необходимо, чтобы операции упаковки и распаковки сохраняли значение.

Пусть имеются 2 метода:
``` csharp
static M<T> CreateSimpleM<T>(T t) { ... }
static M<R> ApplySpecialFunction<A, R>(
  M<A> monad, Func<A, M<R>> function) {...}
```

Тогда, результат следующего выражения:
``` csharp
ApplySpecialFunction(someMonadValue, CreateSimpleM)
```

по значению идентичен `someMonadValue`, а результат следующего выражения:
``` csharp
ApplySpecialFunction(CreateSimpleM(someValue), someFunction)
```

по значению идентичен:
``` csharp
someFunction(someValue)
```

### Часть седьмая
Допустим, имеются 2 функции:
``` csharp
Func<int, Nullable<double>> log = x => x > 0
    ? new Nullable<double>(Math.Log(x))
    : new Nullable<double>();
Func<double, Nullable<decimal>> toDecimal = y => Math.Abs(y) < decimal.MaxValue
    ? new Nullable<decimal>((decimal)y)
    : new Nullable<decimal>();
```

Тогда, с помощью определенного ранее метода `ApplySpecialFunction` можно написать следующий метод-помощник:
``` csharp
static Func<X, Nullable<Z>> ComposeSpecial<X, Y, Z>(
  Func<X, Nullable<Y>> f,
  Func<Y, Nullable<Z>> g)
{
  return x => ApplySpecialFunction(f(x), g);
}
```

который позволяет объединить определенные выше функции в одну:
``` csharp
Func<int, Nullable<decimal>> both = ComposeSpecial(log, toDecimal);
```

Отсюда следует последнее правило — метод `ApplySpecialFunction` должен гарантировать работу композиции. Пример:
``` csharp
Func<X, M<Y>> f = whatever;
Func<Y, M<Z>> g = whatever;
M<X> mx = whatever;
M<Y> my = ApplySpecialFunction(mx, f);
M<Z> mz1 = ApplySpecialFunction(my, g);
Func<X, M<Z>> h = ComposeSpecial(f, g);
M<Z> mz2 = ApplySpecialFunction(mx, h);
```

Значения `mz1` и `mz2` должны быть одинаковыми.

Наконец, можно полностью описать «шаблон монады» в C#:

Монада это обобщенный тип `M<T>`, такой что:

- Для нее существует конструирующий механизм, который принимает на вход переменную типа `T` и возвращает `M<T>`:
  ``` csharp
  static M<T> CreateSimpleM<T>(T t)
  ```

- Если существует способ преобразования значения типа `A` в `M<R>`, то можно применить эту функцию к экземпляру `M<A>` и получить экземпляр `M<R>`:
  ``` csharp
  static M<R> ApplySpecialFunction<A, R>(
    M<A> monad, Func<A, M<R>> function)
  ```

Оба этих метода должны подчинятся следующим законам:

- Применение функции создающую простую монаду (правило-метод 1) к конкретному экземпляру монады должно приводить к логически идентичному экземпляру монады.
- Применение функции к результату функции создающей простую монаду из определенного значения и применение этой функции к определенному значению напрямую должно приводить к логически идентичным экземплярам монад.
- Результат применения к значению первой функции второй функции и результат применения первоначального значения к функции-композиции первых двух функций должен приводить к двум логически идентичным экземплярам монад.

### Часть восьмая
Традиционное имя для функции `CreateSimple` — `unit`. В Haskell — `return`.

Традиционное имя для функции `ApplySpecialFunction` — `bind`. В Haskell она является встроенной функцией, для того чтобы применить функцию `f` на экземпляр монады `m` необходимо написать `m >>= f`.

Фактически, функция привязки берет неизменный рабочий процесс и операцию над ним и возвращает новый рабочий процесс.

Мой конспект на этом оканчивается. В последующих частях серии рассматривается практическое применение монад в коде.

- [Часть 9](http://ericlippert.com/2013/03/21/monads-part-nine/). О простых монадах «присоединяющих дополнительные данные к значению».
- [Часть 10](http://ericlippert.com/2013/03/25/monads-part-ten/). О запросах и LINQ на примере `SelectMany`.
- [Часть 11](http://ericlippert.com/2013/03/28/monads-part-eleven/). Дополнения к предыдущей главе. Аддитивная монада.
- [Часть 12](http://ericlippert.com/2013/04/02/monads-part-twelve/). Продолжение про запросы и `SelectMany`.
- [Часть 13](http://ericlippert.com/2013/04/03/monads-part-thirteen/). О `Task` монадах.
