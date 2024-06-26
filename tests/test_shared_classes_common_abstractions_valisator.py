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


def real_length_validation(obj: Any, params: VParams) -> None:        # noqa
    max_length = params.get('max_length')

    if max_length is None:
        raise ValidationError('Необходимо указать max_length в kwargs')

    ln = len(obj)
    if ln > max_length:
        msg = (f'Фактическая длина объекта {repr(obj)} составляет {ln}, '
               f'что выходит за пределы максимально допустимого значения '
               f'({max_length})')
        raise ValidationError(msg)


def real_handler(e: Exception, obj: Any) -> None:                     # noqa
    if isinstance(e, ValidationError):
        raise ZeroDivisionError


def unexpected_crush(obj: Any, params: VParams) -> None:              # noqa
    1 / 0                                                             # noqa
    raise ValidationError


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
       или их типы).
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
       этим параметрами.
    3. Валидатор ничего не делает, если его корректно вызвали с параметрами, и
       объект соответствует параметрам.

    4. При установленном обработчике поднимается та ошибка, которую определил
       обработчик, а не встроенная ошибка валидатора

    :return: ``None``
    """
    s = 'Очень длинная строка, которая, явно длиннее 20 символов, в натуре!'

    methods = [real_length_validation]
    validator = Validator(methods)                                    # noqa
    with _(ValidationError):
        validator.validate(s)

    s = 'Очень длинная строка, которая, явно длиннее 20 символов, в натуре!'
    methods = [real_length_validation]
    validator = Validator(methods)                                    # noqa
    with _(ValidationError):
        validator.validate(s, max_length=20)                          # noqa

    s = 'Коротенькая строка, явно меньше 100 символов'
    methods = [real_length_validation]
    validator = Validator(methods)                                    # noqa
    validator.validate(s, max_length=100)                             # noqa

    validator = Validator([real_length_validation], real_handler)
    with _(ZeroDivisionError):
        validator.validate(s, max_length=1)                           # noqa

    validator = Validator([unexpected_crush])
    with _(Exception, match=r'.*непредвиденная'):
        validator.validate(s, max_length=1)                           # noqa

def testn_validation() -> None:                                       # noqa
    ...


def testp_validation_via_decorator() -> None:
    """
    **Валидация через декоратор**

    Осуществляется корректный вызов валидатора в виде декоратора

    :return: ``None``
    """
    validator = Validator([real_length_validation])
    s = ''

    @validator.validate_with(max_length=20)                           # noqa
    def set_value(obj: Any) -> None:                                  # noqa
        nonlocal s
        s = obj

    set_value('test')                                                 # noqa
    assert s == 'test'                                                # noqa

    @validator.validate_with(max_length=1)                            # noqa
    def set_new_value(obj: Any) -> None:
        nonlocal s
        s = obj

    with _(ValidationError):
        set_new_value('И тогда я схватил этого подлеца...')           # noqa

    assert s == 'test'                                                # noqa
    

def testn_validation_via_decorator() -> None:
    ...
