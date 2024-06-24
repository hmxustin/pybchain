from pytest import raises as _

from shared.classes.common.abstractions.validator import *
from inspect import signature
from typing import Optional


def method_is_positive(obj, params) -> bool:
    return obj > 0


def method_always_true(obj) -> bool:
    return True


def method_without_return(obj):
    ...


def testp_validator_initialization():

    """
    Корректная инициализация валидатора требует передачи ему списка методов валидации (причем, методы должны возвращать значение булева
    типа, а сам список не должен быть пустым). Метод обработки ошибок передавать можно, но не обязательно.
    """

    methods = [method_is_positive]
    validator = Validator(methods)

def testn_validator_initialization():
    """
    """

    # Валидация невозможна если не переданы конкретные методы валидации.
    # Вариант 1. Аргумент methods не является списком

    methods = 42
    with _(Exception):
        validator = Validator(methods)  # noqa - намеренная ошибка ради теста


"""
Корректная инициализация с валидными методами.
Вызов исключения при передаче неверного типа methods.
Вызов исключения при передаче пустого списка методов.
Вызов исключения при передаче не вызываемого объекта в качестве метода.
Вызов исключения при методе, возвращающем не булево значение.
Вызов исключения при методе, ничего не возвращающем.
Корректная инициализация с валидным обработчиком.
Вызов исключения при передаче невалидного обработчика.
Корректная инициализация с методом, возвращающим Optional[bool].


def test_validator_init_with_valid_methods():
    # Тест для успешной инициализации с валидными методами
    methods = [is_positive]
    validator = Validator(methods)
    assert validator._methods == methods
    assert validator._handler is None

def test_validator_init_with_invalid_methods_type():
    # Тест для проверки TypeError при передаче не списка в методы
    with pytest.raises(TypeError):
        Validator(methods=is_positive)

def test_validator_init_with_empty_methods_list():
    # Тест для проверки TypeError при передаче пустого списка методов
    with pytest.raises(TypeError):
        Validator(methods=[])

def test_validator_init_with_non_callable_method():
    # Тест для проверки TypeError при передаче не вызываемого объекта в списке методов
    with pytest.raises(TypeError):
        Validator(methods=[lambda x: x > 0, 5])

def test_validator_init_with_invalid_return_type():
    # Тест для проверки TypeError при передаче метода с неверным возвращаемым типом
    def invalid_return_type(obj):
        return "not a bool"

    with pytest.raises(TypeError):
        Validator(methods=[invalid_return_type])

def test_validator_init_with_no_return_type():
    # Тест для проверки TypeError при передаче метода без возвращаемого типа
    def no_return_type(obj):
        pass

    with pytest.raises(TypeError):
        Validator(methods=[no_return_type])

def test_validator_init_with_valid_handler():
    # Тест для успешной инициализации с валидным обработчиком ошибок
    def handler(ex):
        print(ex)

    methods = [is_positive]
    validator = Validator(methods, handler)
    assert validator._methods == methods
    assert validator._handler == handler

def test_validator_init_with_invalid_handler():
    # Тест для проверки TypeError при передаче не вызываемого обработчика ошибок
    with pytest.raises(TypeError):
        Validator(methods=[is_positive], handler="not callable")
        
        
def test_init_with_valid_methods(self):
    # Тест инициализации с корректным списком методов

    def method1(obj): return True

    def method2(obj): return True

    validator = Validator([method1, method2])
    self.assertEqual(validator._methods, [method1, method2])


def test_init_with_empty_methods(self):
    # Тест инициализации с пустым списком методов

    validator = Validator([])
    self.assertEqual(validator._methods, [])


def test_init_with_invalid_methods_type(self):
    # Тест инициализации с некорректным типом аргумента methods

    with self.assertRaises(TypeError):
        Validator("not a list")


def test_init_with_non_callable_method(self):
    # Тест инициализации с некорректным элементом в списке methods

    with self.assertRaises(TypeError):
        Validator([lambda x: x, "not a function"])


def test_init_with_valid_handler(self):
    # Тест инициализации с корректным обработчиком ошибок


    def handler(e): return "Error handled"

    validator = Validator([], handler)
    self.assertEqual(validator._handler, handler)


def test_init_with_none_handler(self):
    # Тест инициализации с обработчиком ошибок равным None

    validator = Validator([])
    self.assertIsNone(validator._handler)


def test_init_with_invalid_handler_type(self):
    # Тест инициализации с некорректным типом обработчика ошибок

    with self.assertRaises(TypeError):
        Validator([], "not a function")


def type_is_valid(obj: Any):
    actual_t = type(obj)
    if actual_t is not str:
        raise ValidationError(f'Полученный объект не является '
                              f'{str} (реальный тип объекта: '
                              f'{actual_t})', 0)


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
