"""
**Тесты для Валидатора**

Тестирование Валидатора в различных условиях
"""

from pytest import raises as _

from shared.classes.basic.abstractions.validator.validator import *


def method_has_raise(a: Any) -> None:                                 # noqa
    if False:
        raise Exception  # noqa


def method_has_raise_1(a: Any) -> None:                               # noqa
    if False:
        raise Exception  # noqa


def correct_handler(e: Exception, obj: Any) -> None:                  # noqa
    ...


def method_returns_something() -> str:                                # noqa
    return '42'


def method_without_params() -> None:                                  # noqa
    ...


def method_with_invalid_param(obj: int) -> None:                      # noqa
    ...


def method_without_raise(obj: Any) -> None:                           # noqa
    ...


def handler_with_only_one_param(a: Any) -> None:                      # noqa
    ...


def handler_with_invalid_param1(a: Any, b: Any) -> None:              # noqa
    ...


def handler_with_invalid_param2(e: Exception, b: int) -> None:        # noqa
    ...


def real_Length_validation(obj: Any, params: VParams) -> None:        # noqa
    max_length = params.get('max_length')

    if max_length is None:
        raise TypeError('Необходимо указать max_length в kwargs')

    ln = len(obj)
    if ln > max_length:
        msg = (f'Фактическая длина объекта {repr(obj)} составляет {ln}, '
               f'что выходит за пределы максимально допустимого значения '
               f'({max_length})')
        raise ValueError(msg)


def testp_validator_initialization() -> None:
    """
    **Инициализация (корректная)**

    Корректная инициализация валидатора требует передачи ему списка методов
    валидации (причем, методы должны возвращать значение булева типа, а сам
    список не должен быть пустым). Метод обработки ошибок передавать можно,
    но не обязательно. Если он передается, то он должен получать исключение и
    сам объект.

    Корректная инициализация возможна при следующих обстоятельствах:

    1. Корректная инициализация с валидными методами (с одним, с несколькими)
       без обработчика.
    2. Корректная инициализация с валидным обработчиком.

    Задача: Проверить, что класс инициализируется корректно
    при передаче списка методов валидации и обработчика ошибок.
    """
    methods = [method_has_raise]
    validator = Validator(methods)                                    # noqa

    methods = [method_has_raise, method_has_raise_1]
    validator = Validator(methods)                                    # noqa

    methods = [method_has_raise, method_has_raise_1]
    handler = correct_handler
    validator = Validator(methods, handler)                           # noqa


def testn_validator_initialization() -> None:
    """
    ** Инициализация (некорректная)**

    Некорректная реализация возможна при следующих обстоятельствах:

    1. Исключение при передаче неверного типа methods (не список).
    2. Исключение при передаче пустого списка методов (список, но пустой).
    3. Исключение при передаче не вызываемого объекта в качестве метода.
    4. Исключение при передаче невалидного обработчика (не вызываемый).
    5. Исключение при методе, возвращающем какое-либо значение.
    6. Исключение при методе с неправильными параметрами (некорректное число
       или их типы.
    7. Исключение при хэндлере не являющемся вызываемым.
    8. Исключение при хэндлере с неправильными параметрами (некорректное
       число или их типы).

    """
    methods = {'first': 1, 'second': 2}
    with _(TypeError):
        validator = Validator(methods)                                # noqa

    methods = []
    with _(TypeError):
        validator = Validator(methods)                                # noqa

    methods = ['first', 'second']
    with _(TypeError):
        validator = Validator(methods)                                # noqa

    methods = [method_returns_something]
    with _(TypeError):
        validator = Validator(methods)                                # noqa

    methods = [method_without_params]
    with _(TypeError):
        validator = Validator(methods)                                # noqa

    methods = [method_with_invalid_param]
    with _(TypeError):
        validator = Validator(methods)                                # noqa

    methods = [method_without_raise]
    with _(TypeError):
        validator = Validator(methods)                                # noqa

    methods = [method_has_raise, method_has_raise_1]
    handler = 'Vasya'
    with _(TypeError):
        validator = Validator(methods, handler)                       # noqa

    methods = [method_has_raise, method_has_raise_1]
    handler = method_returns_something
    with _(TypeError):
        validator = Validator(methods, handler)                       # noqa

    methods = [method_has_raise, method_has_raise_1]
    handler = handler_with_only_one_param
    with _(TypeError):
        validator = Validator(methods, handler)                       # noqa

    methods = [method_has_raise, method_has_raise_1]
    handler = handler_with_invalid_param1
    with _(TypeError):
        validator = Validator(methods, handler)                       # noqa

    methods = [method_has_raise, method_has_raise_1]
    handler = handler_with_invalid_param2
    with _(TypeError):
        validator = Validator(methods, handler)                       # noqa


def testp_validation() -> None:
    """
    **Фактическая валидация (через вызов метода)**

    Проводим реальные тесты валидации:
    1. Валидатор корректно дает исключение, при его вызове без параметров,
       когда валидатору нужны параметры.
    2. Валидатор корректно возвращает ошибку, при его правильном вызове с
       нужными параметрами, при условии, что объект проверки не соответствует
       этим параметрами
    3. Валидатор ничего не делает, если его корректно вызвали с параметрами, и
       объект соответствует параметрам

    :return: ``None``
    """
    s = 'Очень длинная строка, которая, явно длиннее 20 символов, в натуре!'

    methods = [real_Length_validation]
    validator = Validator(methods)                                    # noqa
    with _(TypeError):
        validator.validate(s)

    s = 'Очень длинная строка, которая, явно длиннее 20 символов, в натуре!'
    methods = [real_Length_validation]
    validator = Validator(methods)                                    # noqa
    with _(ValueError):
        validator.validate(s, max_length=20)                          # noqa

    s = 'Коротенькая строка, явно меньше 100 символов'
    methods = [real_Length_validation]
    validator = Validator(methods)                                    # noqa
    validator.validate(s, max_length=100)                             # noqa


def testn_validation() -> None:                                       # noqa
    ...


"""

2. Тесты метода валидации (validate)

Успешная валидация: Проверить, что метод validate не выбрасывает исключений при успешной проверке объекта.
Неуспешная валидация: Проверить, что метод validate выбрасывает соответствующее исключение ValidationError при неудачной проверке объекта.
Обработка ошибок: Проверить, что метод validate вызывает обработчик ошибок handler при неудачной проверке объекта, если он задан.
Вывод информации об ошибке: Проверить, что при отсутствии обработчика ошибок, метод validate выводит информацию об ошибке в консоль.

3. Тесты декоратора (validate_with)

Корректное применение декоратора: Проверить, что декоратор validate_with корректно выполняет валидацию объекта перед вызовом декорируемой функции.
Передача параметров в декоратор: Проверить, что декоратор validate_with корректно принимает и использует параметры, переданные при его вызове.

5. Тесты на граничные случаи

Проверить поведение класса при передаче пустых или None значений в качестве аргументов.
Проверить поведение класса при возникновении различных типов исключений во время валидации.
Проверить поведение класса при использовании сложных типов данных в качестве аргументов.
Важно:

Все тесты должны быть хорошо документированы и покрывать все возможные сценарии использования класса.
Тесты должны быть написаны с использованием фреймворка для тестирования Python, такого как pytest или unittest.
Тесты должны быть запущены на разных платформах и версиях Python, чтобы убедиться в корректной работе класса во всех средах.


def length_is_valid(obj: Any, params: VParams):
    ln = len(obj)
    mx = params.get('max_length')
    if ln > mx:
        raise ValidationError(f'Фактическая длина строки ({ln}) '
                              f'превышает максимально допустимую '
                              f'({mx})', 0)


def type_is_valid_handler(ex: Exception, obj: Any) -> None:
    if ex.args[1] == 0:
        intro = f'💥 При попытке валидации объекта [{obj}]'
        raise ValueError(f'{intro} '
                         f'возникла ошибка -=[ {ex.args[0]} ]=-')
    else:
        raise Exception('Неизвестная ошибка')


validator = Validator([type_is_valid, length_is_valid])


# Используем декоратор для валидации входных данных функции
@validator.validate_with(max_length=4)                                # noqa
def process_string(text):
    return text.upper()


# Пример корректного использования
try:
    result = process_string("hello")
    print(result)  # Выведет: HELLO
except TypeError as e:
    print(f"Ошибка: {e}")

# Пример некорректного использования (передаем число вместо строки)
s = 11222
try:
    result = process_string(s)                                        # noqa
    print(result)
except TypeError as e:
    print(f"Ошибка: {e}")  # Выведет: Ошибка: Полученный объект не является <class 'str'> (реальный тип объекта: <class 'int'>)
"""
