+++
title = "C# Enum и Атрибут Flags"
date = "2015-11-03T13:10:07+03:00"
tags = ["dotnet"]
categories = ["Development"]
draft = false
description = "Как в c# enum добавлять, находить и удалять несколько значений, с помощью атрибута Flags."
keywords = "C#, Enum, Flags, FlagsAttribute, Атрибут, Тип перечисления, битовые, битовые операции"
slug = "flags-enums-in-csharp"
aliases = [
    "/posts/flags-enums-in-csharp/",
    "/2015/11/c-enum-flags.html"
]
+++

Возникают ситуации, когда переменная должна хранить несколько значений типа перечисления. Например, используемые области логирования: _Warning + Info_, или сочетания цветов: _Red + Blue + Green_.

Для хранения в переменной нескольких флагов, значениям енама присваиваются степени двойки:
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

Значения _2, 4, 8_ используются для [операторов смещения](https://ru.wikipedia.org/wiki/%D0%91%D0%B8%D1%82%D0%BE%D0%B2%D1%8B%D0%B5_%D0%BE%D0%BF%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D0%B8), таких как побитовое И (AND), ИЛИ (OR) и исключающее ИЛИ (XOR).

### Операции над переменной
Логическое ИЛИ (`|`) применяется для помещения нескольких значений флагов в одну переменную:
``` csharp
myProperties.AllowedColors = MyColor.Red | MyColor.Green | MyColor.Blue;
```

Логическое И (`&`) помогает при нахождении значения флага:
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

Начиная с .Net 4 можно использовать сокращенную версию, без явного указания `&`:
``` csharp
if (myProperties.AllowedColors.HasFlag(MyColor.Yellow))
{
    // Yellow has been set...
}
```

Операция XOR (’^’) исключает значения из переменной:
``` csharp
myProperties.AllowedColors = MyColor.Red | MyColor.Green | MyColor.Blue;
// Удаляем значение используя оператор смещения XOR.
myProperties.AllowedColors = myProperties.AllowedColors ^ MyColor.Green;
Console.WriteLine("My colors are {0}", myProperties.AllowedColors);
// Output: My colors are Red, Blue
```

### Атрибут Flags
Атрибут `[Flags]` необязательный и используется для красивого вывода при вызове `.ToString()`:
``` csharp
enum Colors { Yellow = 1, Green = 2, Red = 4, Blue = 8 }
[Flags] enum ColorsFlags { Yellow = 1, Green = 2, Red = 4, Blue = 8 }
...
var str1 = (Colors.Yellow | Colors.Red).ToString(); // "5"
var str2 = (ColorsFlags.Yellow | ColorsFlags.Red).ToString(); // "Yellow, Red"
```

Так же, атрибут `[Flags]` не присваивает значениям степень двойки. Если не проставить вручную, то значения инициализируются как в обычном енаме.

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

Присвоенные значения: _Yellow = 0, Green = 1, Red = 2, Blue = 3_. Они не подходят для использования операций смещения.

### Битовое представление
Описанное выше работает благодаря битовому представлению значений флагов при проставлении степени двойки:
``` csharp
Yellow: 00000001
Green:  00000010
Red:    00000100
Blue:   00001000
```

Значение переменной `AllowedColors` после присваивания _Red, Green_ и _Blue_ c использованием операции ИЛИ (`|`):
``` csharp
myProperties.AllowedColors: 00001110
```


Теперь, для проверки вхождения значения _Green_ в переменную используем операцию смещения И (`&`):
``` csharp
myProperties.AllowedColors: 00001110
             MyColor.Green: 00000010
             -----------------------
                            00000010 // Это то же самое, что и MyColor.Green!
```

### Полезные ссылки
- What does the [Flags] Enum Attribute mean in csharp? – [Stackoverflow.com](http://stackoverflow.com/questions/8447/what-does-the-flags-enum-attribute-mean-in-c)
- Типы перечислений – [msdn.microsoft.com](https://msdn.microsoft.com/ru-ru/library/cc138362.aspx)
- FlagsAttribute (класс) – [msdn.microsoft.com](https://msdn.microsoft.com/ru-ru/library/system.flagsattribute(v=vs.110).aspx)
