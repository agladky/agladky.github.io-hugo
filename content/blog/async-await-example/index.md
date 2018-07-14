+++
title = "Сравнение async await и Task.ContinueWith()"
date = "2016-12-13T17:10:07+03:00"
tags = ["dotnet"]
categories = ["Development"]
draft = false
description = "Краткая выжимка из рабочего доклада по работе с async/await в C#. Для наглядности, параллельно рассматривается подход с использованием Task.ContinueWith."
keywords = "C#, async, await, deadlock, continuewith, асинхронность, задачи, потоки, обработка ошибок"
slug = "async-await-example"
+++

Это краткая выжимка из рабочего доклада по работе с async/await в C#. Для наглядности, параллельно рассматривается подход с использованием блока `ContinueWith`.

### Основные паттерны асинхронного программирования
- [Asynchronous Programming Model (APM)](https://msdn.microsoft.com/en-us/library/ms228963.aspx)
- [Event Asynchronous Pattern (EAP)](https://msdn.microsoft.com/en-us/library/ms228969.aspx)
- [Task Asynchronous Pattern (TAP)](https://msdn.microsoft.com/en-us/library/hh873175.aspx)
  - Задачи представляют параллельные операции
  - Могут выполняться на отдельном или разных потоках.
  - Могут быть скомбинированы и выстроены в цепочку вызовов.

### async/await — синтаксическая обертка над задачами
- `await` ставит на паузу текущий метод, ожидая выполнения задачи.
- Выглядит как блокирующая (синхронная) операция.
- Не блокирует текущий поток.
- Выполнение продолжается в том же контексте, из которого была вызвана задача, если явно не указано иное.
- Ключевое слово `async` указывается, чтобы среда исполнения воспринимала `await` как ключевое слово.
- `await` метод начинает выполняться синхронно. Если он уже закончил свое выполнение то новый поток не создается. Все продолжается в том же потоке. Подробнее в [ответе на stackoverflow.com](http://stackoverflow.com/questions/17380070/c-sharp-async-awaitable-clarification).
- `await` работает с любым типом, для которого реализован метод `GetAwaiter()`. Подробнее в статье - [await anything](http://blogs.msdn.com/b/pfxteam/archive/2011/01/13/10115642.aspx).

### Демонстрационное приложение
Примеры показываются на тестовом Windows Form приложении. [GitHub репозиторий с приложением](https://github.com/agladky/async_await_article).

{{% imgres src="images/async-await-test-window" alt="async/await тестовое окно" /%}}

Асинхронные действия лежат в `PeopleRepositoryAsync`:
```csharp
public class PeopleRepositoryAsync
{
    public async Task<List<string>> GetPeopleList()
    {        
        await Task.Delay(2000);                       
        return new List<string>
        {
            "John Smith",  
            "Ivan Ivanov",
            "Joao Fetucini"
        };
    }
}
```

Метод `GetPeopleList()` асинхронно ожидает 2 секунды и возвращает список пользователей.

### Первое сравнение TAP и async/await подхода
#### Реализация с Task и ContinueWith
Добавим код для получения списка пользователей в обработчик нажатия кнопки "Fetch Data (with Task)" - `buttonTask_Click`:
```csharp
Task<List<string>> peopleTask = Repository.GetPeopleList();
List<string> people = peopleTask.Result;
```

Этот код не будет выполняться асинхронно. Он будет ожидать завершение задачи `peopleTask` в основном потоке, поэтому UI заморозится. Добавим конструкцию `ContinueWith(t => { })`:

```csharp
peopleTask.ContinueWith(t =>
{
  List<string> people = peopleTask.Result;
});
```

Теперь задача по получению пользователей выполнится асинхронно. После её завершения выполнится код в блоке `ContinueWith`.
Добавим в `ContinueWith` отображение полученных имен в `textBoxMain`:
```csharp
textBoxMain.AppendText($"{Environment.NewLine}Person list:{Environment.NewLine}");
foreach (var person in people)
{
    textBoxMain.AppendText($"- {person}{Environment.NewLine}");
}
```

Если запустить приложение и нажать на "Fetch Data (with Task)", то возникнет ошибка. Все потому, что код в блоке `ContinueWith` выполняется в потоке, отличном от того где находится [SynchronizationContext](https://habrahabr.ru/post/232169/) UI потока.
Для выполнения в нужном потоке добавим в вызов метода `ContinueWith` аргумент `TaskScheduler.FromCurrentSynchronizationContext()`:
```csharp
peopleTask.ContinueWith(t => { ... }, TaskScheduler.FromCurrentSynchronizationContext());
```
Теперь приложение работает корректно. Перейдем к реализации этого кода с помощью ключевых слов `async` и `await`.

#### Реализация с async/await
Основное отличие от предыдущей реализации — код будет похож на синхронный. Перейдем в обработчик нажатия кнопки "Fetch Data (with await)" - `buttonAwait_Click`. Добавим код для получения списка пользователей:
```csharp
List<string> people = await Repository.GetPeopleList();
```

В объявление метода добавим слово `async`, чтобы среда исполнения поняла что `await` это ключевое слово, а не просто переменная. Вставим без изменений код из `ContinueWith`:
```csharp
textBoxMain.AppendText($"{Environment.NewLine}Person list:{Environment.NewLine}");
foreach (var person in people)
{
    textBoxMain.AppendText($"- {person}{Environment.NewLine}");
}
```

Все. Приложение работает так же как и в предыдущем пункте. Код выглядит как синхронный. Выполнение продолжается в том же потоке, из которого и было вызвано.

### Обработка ошибок
Для демонстрации добавим в метод `GetPeopleList` код вызова ошибки (после `Task.Delay(2000)`):
```csharp
throw new NotImplementedException("Метод не реализован!");
```

#### Обработка ошибок для await метода
Сначала рассмотрим самый простой случай. Отлов и обработка ошибок для метода с `await` происходит как в синхронном коде:
```csharp
try
{
    // Получение и вывод значений из репозитория
}
catch (Exception ex)
{
    MessageBox.Show(ex.Message, "ОШИБКА");
}
finally
{
    // Критичный к выполнению код
}
```
Всё. Дополнительно писать ничего не надо, ошибка будет поймана.

#### Обработка ошибок для Task метода
Для метода с блоком `ContinueWith` обработать ошибки можно несколькими способами.

Первый, использовать еще один вызов `ContinueWith` на задаче. Вызовем `ContinueWith` с 2 дополнительными параметрами:
```csharp
peopleTask.ContinueWith(t =>
    {
        // Получение и вывод значений из репозитория
    },
    CancellationToken.None,
    TaskContinuationOptions.OnlyOnRanToCompletion,
    TaskScheduler.FromCurrentSynchronizationContext());
```

Главное — аргумент `TaskContinuationOptions.OnlyOnRanToCompletion`. Он указывает, что блок кода выполнится только если в задаче не было ошибок.

Теперь, код для обработки ошибки:

```csharp
peopleTask.ContinueWith(t =>
    {
        foreach (var exception in t.Exception.Flatten().InnerExceptions)
        {
            MessageBox.Show(exception.Message);
        }
    },
    CancellationToken.None,
    TaskContinuationOptions.OnlyOnFaulted,
    TaskScheduler.FromCurrentSynchronizationContext());
```

Опция `OnlyOnFaulted` указывает, что код в блоке выполниться только при ошибке в задаче. Оператор `foreach` разворачивает ошибки в «плоское» состояние, т. к. все ошибки представляются в виде иерархии и оборачиваются в `AggregateException`.

Для имитации блока `finally`, напишем:
```csharp
peopleTask.ContinueWith(t =>
    {
        // Критичный к выполнению код
    },
    CancellationToken.None);
```

Второй способ обработки ошибок занимает меньше строк. В блок `ContinueWith` добавляется условный оператор, который проверяет статус задачи:
```csharp
peopleTask.ContinueWith(t =>
    {
        if (t.Status == TaskStatus.RanToCompletion)
        {
            // Получение и вывод значений из репозитория
        }
        if (t.Status == TaskStatus.Faulted)
        {
            // Обработка ошибок
        }
        // (finally) Критичный к выполнению код
    },
    TaskScheduler.FromCurrentSynchronizationContext());
```

### Отмена действий
Обновим метод `GetPeopleList` класса `Repository`. Добавим параметр `CancellationToken` и точку отмены после вызова `Task.Delay(2000)`:
```csharp
public async Task<List<string>> GetPeopleList(CancellationToken cancellationToken = new CancellationToken())
{
    await Task.Delay(1500, cancellationToken);
    cancellationToken.ThrowIfCancellationRequested();
    return new List<string> { ... };
}
```

Обратит внимание, что отмена произойдет только после ожидания в 2 секунды. Само действие `Task.Delay` не прерывается.

Для операции отмены используем кнопку "Cancel request" с обработчиком `buttonCancel_Click`. Объекту `CancellationToken` можно задать значение только при инициализации. Поэтому создадим переменную `CancellationTokenSource`. Она позволяет генерировать токены и изменять их состояние во время выполнения.

В класс `MainForm` добавим поле:
```csharp
private CancellationTokenSource _tokenSource;
```

А в обработчик `buttonCancel_Click`  код для подачи токену сигнала отмены:
```csharp
_tokenSource.Cancel();
```

#### Обработка отмены для async метода
В обработчике `buttonAwait_Click` изменим вызов метода `GetPeopleList()`, добавив инициализацию `_tokenSource` и передав сгенерированный токен в качестве аргумента:
```csharp
_tokenSource = new CancellationTokenSource();
List<string> people = await Repository.GetPeopleList(_tokenSource.Token);
```

Добавим обработку операции отмены:
```csharp
catch (OperationCanceledException ex)
{
    MessageBox.Show(ex.Message, "Canceled");
}
```

#### Обработка отмены для Task метода
Для `buttonTask_Click` добавим похожий код для передачи токена:
```csharp
_tokenSource = new CancellationTokenSource();
Task<List<string>> peopleTask = Repository.GetPeopleList(_tokenSource.Token);
```

Для обработки операции отмены в блок `ContinueWith` добавим:
```csharp
if (t.Status == TaskStatus.Canceled)
{
  MessageBox.Show("Operation Canceled", "Canceled");
}
```

### Deadlocks
Добавим в класс `Repository` метод `DeadlockTestAsync()`:
```csharp
public async Task DeadlockTestAsync()
{
    await Task.Delay(1500);
    Console.WriteLine("Done!");
}
```

Вызовем этот метод в обработчике кнопки "Deadlock":
```csharp
async void buttonDeadlock_Click
{
    Repository.DeadlockTestAsync().Wait();
}
```

Все. При нажатии на кнопку возникнет Deadlock. Почему? Рассмотрим по пунктам:

1. `DeadlockTestAsync()` вызывается на потоке с UI.
2. `Task.Delay()` запускается в новом потоке.
3. `await` захватывает `SynchronizationContext` и подключает continuation для выполнения действий после завершения.
4. Вернемся к вызову `DeadlockTestAsync()`.
5. `Wait()` ждет завершение задачи в UI потоке.
6. `Task.Delay()` ожидает выполнить продолжение на UI потоке.
7. Но поток в ожидание - Дедлок!
8. Все потому, что задача не вернется из `DeadlockTestAsync()`, пока не выполнится "продолжение".

Для избежания подобной ситуации, в библиотеках, лучше писать `.ConfigureAwait(false)`:
```csharp
await Task.Delay(1500).ConfigureAwait(false);
```
Это позволит выполнить "продолжение" в том же потоке, в котором работала задача. В моем примере это будет поток, отличный от UI потока.

### Полезные ссылки
* Stephen blog - [Async and Await](http://blog.stephencleary.com/2012/02/async-and-await.html)
* Async/Await - [Best Practices in Asynchronous Programming](https://msdn.microsoft.com/en-us/magazine/jj991977.aspx)
* Async/Await [FAQ](http://blogs.msdn.com/b/pfxteam/archive/2012/04/12/10293335.aspx)
* [Await anything](http://blogs.msdn.com/b/pfxteam/archive/2011/01/13/10115642.aspx)
