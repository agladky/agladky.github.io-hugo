+++
title = "C# Enum и Атрибут Flags"
date = "2015-11-03T13:10:07+03:00"
tags = [".net"]
categories = ["Development"]
draft = true
description = "Как в c# enum добавлять, находить и удалять несколько значений, с помощю аттрибута Flags."
keywords = "C#, Enum, Flags, FlagsAttribute, Атрибут, Тип переисления, битовые, битовые операции"
slug = "flags-enums-in-csharp"
aliases = [
    "/posts/flags-enums-in-csharp/",
    "/2015/11/c-enum-flags.html"
]
+++

Периодически встречаются ситуации, когда одна переменная должна хранить и передавать несколько значений из типа перечисления. Для этого необходимо инициализировать значения enum'a степенью двойки. Как это сделано здесь, например:
``` csharp
[Flags]
public enum MyColors
{
    Yellow = 1,
    Green = 2,
    Red = 4,
    Blue = 8
}
```

Такие значения необходимы для использования [операторов смещения](https://ru.wikipedia.org/wiki/%D0%91%D0%B8%D1%82%D0%BE%D0%B2%D1%8B%D0%B5_%D0%BE%D0%BF%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D0%B8), таких как побитовое И (AND), ИЛИ (OR) и исключающее ИЛИ (XOR).

Теперь, что бы поместить несколько значений флагов в одну переменную, можно использовать следующий синтаксис:
``` csharp
myProperties.AllowedColors = MyColor.Red | MyColor.Green | MyColor.Blue;
```

Атрибут `[Flags]` не является обязательным и, по сути, используется для красивого вывода при вызове `.ToString()`. Рассмотрим примеры с указанием атрибута и без:
``` csharp
enum Colors { Yellow = 1, Green = 2, Red = 4, Blue = 8 }
[Flags] enum ColorsFlags { Yellow = 1, Green = 2, Red = 4, Blue = 8 }
...
var str1 = (Colors.Yellow | Colors.Red).ToString(); // "5"
var str2 = (ColorsFlags.Yellow | ColorsFlags.Red).ToString(); // "Yellow, Red"
```

Так же, атрибут `[Flags]` не означает, что значения автоматически будут возведены в степень двойки. Если забыть их проставить, то ничего работать не будет. Т.к. по умолчанию значения начинаются с 0 и каждое последующие увеличивается на 1.

Неправильное объявление:
``` csharp
[Flags]
public enum MyColors
{
    Yellow,
    Green,
    Red,
    Blue
}
```

Значения при данном объявление будут следующими: Yellow = 0, Green = 1, Red = 2, Blue = 3. Т.е. они не подходят для использования операций смещения.

### Как проверять наличие значения и удалять его из переменной
Для определения значения в переменной можно использовать следующий код:
``` csharp
if((myProperties.AllowedColors & MyColor.Yellow) == MyColor.Yellow)
{
    // Yellow has been set...
}

if((myProperties.AllowedColors & MyColor.Green) == MyColor.Green)
{
    // Green has been set...
}
```

или, начиная с .Net 4:
``` csharp
if (myProperties.AllowedColors.HasFlag(MyColor.Yellow))
{
    // Yellow has been set...
}
```

С помощью логической операции XOR можно исключать значения:
``` csharp
myProperties.AllowedColors = MyColor.Red | MyColor.Green | MyColor.Blue;
// Удаляем значение используя оператор смещения XOR.
myProperties.AllowedColors = myProperties.AllowedColors ^ MyColor.Green;
Console.WriteLine("My colors are {0}", myProperties.AllowedColors);
// Output: My colors are Red, Blue
```

### Что происходит внутри
Предыдущие операции работают, потому что переменные перечисления были объявлены как степень двойки. В битовом представлении переменные выглядят так:
``` csharp
 Yellow: 00000001
 Green:  00000010
 Red:    00000100
 Blue:   00001000
```

После того как выставить свойство `AllowedColors` в Red, Green и Blue, оно будет выглядеть так:
``` csharp
myProperties.AllowedColors: 00001110
```

Когда получаем значение, на самом деле над значениями производится операция смещения "И" (символ "&").
``` csharp
myProperties.AllowedColors: 00001110
             MyColor.Green: 00000010
             -----------------------
                            00000010 // Это тоже самое, что и MyColor.Green!
```

### Полезные ссылки
- What does the [Flags] Enum Attribute mean in csharp? – [Stackoverflow.com](http://stackoverflow.com/questions/8447/what-does-the-flags-enum-attribute-mean-in-c)
- Типы перечислений – [msdn.microsoft.com](https://msdn.microsoft.com/ru-ru/library/cc138362.aspx)
- FlagsAttribute (класс) – [msdn.microsoft.com](https://msdn.microsoft.com/ru-ru/library/system.flagsattribute(v=vs.110).aspx)
