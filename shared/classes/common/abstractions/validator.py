""" Базовый класс для исключения, возникающего при ошибке валидации, а также, собственно, сам валидатор """

from typing import Any, Dict, List, Callable, TypeAlias, Optional

ValidationParams: TypeAlias = Optional[Dict[str, Any]]
ValidationMethod: TypeAlias = Callable[[Any, ValidationParams], None]
ValidationMethods: TypeAlias = List[ValidationMethod]
ValidationHandler: TypeAlias = Callable[[Exception, Any, ValidationParams], None]


class ValidationError(Exception):
    """ Базовый класс для исключений валидации """


class Validator:
    """ Валидатор, способный выполнять по отношению к объекту проверки (``obj``) список методов проверки (``methods``), поднимая
    соответствующие исключения в случае неудач """
    def __init__(self, methods: ValidationMethods, handler: ValidationHandler) -> None:
        """
        Инициализация и установка методов проверок и обработчика ошибок
        :param methods: список методов проверок
        :param handler: обработчик ошибок
        :return: ``None``
        """
        self._methods = methods
        self._handler = handler

    def validate(self, obj: Any, **params: ValidationParams) -> None:
        """
        Собственно, валидация
        :param obj: объект валидации
        :param params: параметры валидации
        :return: ``None`` (в случае неудачи проверки будет поднято соответствующее исключение и вызван обработчик)
        """
        for method in self._methods:
            try:
                method(obj, params)
            except ValidationError as e:
                self._handler(e, obj, **params)

    def validate_with(self, **params: ValidationParams):
        def decorator(func):
            def wrapper(obj, *args, **kwargs):
                self.validate(obj, **params)
                return func(obj, *args, **kwargs)
            return wrapper
        return decorator


def type_is_valid(obj: Any, params: ValidationParams):
    actual_t = type(obj)
    if actual_t is not str:
        raise ValidationError(f'Полученный объект не является '
                              f'{str} (реальный тип объекта: '
                              f'{actual_t})', 0)


def type_is_valid_handler(e: Exception, obj, params=None):
    if params is None:
        params = {}
    if e.args[1] == 0:
        intro = f'При попытке валидации объекта [{obj}]'
        raise TypeError(f'{intro} '
                        f'возникла ошибка {e.args[0]}')
    else:
        raise Exception('Неизвестная ошибка')


validator = Validator([type_is_valid], type_is_valid_handler)


# Используем декоратор для валидации входных данных функции
@validator.validate_with()
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
    result = process_string(s)
    print(result)
except TypeError as e:
    print(f"Ошибка: {e}")  # Выведет: Ошибка: Полученный объект не является <class 'str'> (реальный тип объекта: <class 'int'>)