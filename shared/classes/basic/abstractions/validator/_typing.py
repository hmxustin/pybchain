"""
**Типы и аннотации для "Валидатора"**

Модуль содержит аннотации и описание ключевых типов данных для класса
``Validator`` согласно требованиям https://clck.ru/3BUKJk
"""

from typing import Any, Callable, Dict, List, Optional, Tuple, TypeAlias


VObj: TypeAlias = Any
"""
**Проверяемый объект**
 
Псевдоним для валидируемого объекта (объекта проверок). Объект должен 
быть всегда только один 
"""

Args: TypeAlias = Tuple
"""
**Аргументы**

Псевдоним для кортежа аргументов
"""

KWArgs: TypeAlias = Dict[str, Any]
"""
**Именованные аргументы**

Псевдоним словаря именованных аргументов
"""

VParams: TypeAlias = Optional[KWArgs]
"""
**Параметры валидации (необязательные)**

Псевдоним необязательного параметра в виде именованных аргументов
"""

VMethod: TypeAlias = Callable[[VObj, VParams], None]
"""
**Метод проверки (callable)**

Псевдоним для конкретного метода валидации, который передается валидатору. 
Этот метод не должен ничего возвращать, но должен содержать внутри себя 
исключение
"""

VMethods: TypeAlias = List[VMethod]
"""
**Список методов проверки**

Псевдоним для списка всех методов, которые передаются валидатору
"""

EHandler: TypeAlias = Optional[Callable[[Exception, VObj], None]]
"""
**Метод обработки исключений (handler)**

Псевдоним для метода обработки ошибок, возникших в процессе применения 
методов проверки к объекту проверки
"""
