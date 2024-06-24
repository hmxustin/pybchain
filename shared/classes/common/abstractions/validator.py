"""
Валидатор, обеспечивающий проверку значений перед их установкой (может быть использован через декоратор с параметрами)
"""

from typing import Any, Dict, List, Callable, TypeAlias, Optional
from re import search

KWArgs: TypeAlias = Dict[str, Any]                                    # псевдоним именованных аргументов
VParams: TypeAlias = Optional[KWArgs]                                 # псевдоним необязательного параметра в виде именованных аргументов
VMethod: TypeAlias = Callable[[Any, VParams], None]                   # псевдоним для метода валидации
VMethods: TypeAlias = List[VMethod]                                   # псевдоним для списка методов валидации
EHandler: TypeAlias = Optional[Callable[[Exception, Any], None]]      # псевдоним для метода обработки ошибок


class ValidationError(Exception):
    """
    Базовый класс для исключений валидации
    """
    ...                                                               # реализация не требуется


class Validator:
    """
    Валидатор, способный выполнять по отношению к объекту проверки (``obj``) список методов проверки (``methods``), поднимая
    соответствующие исключения в случае неудач
    """
    def __init__(self, methods: VMethods, handler: EHandler = None) -> None:
        """
        Инициализация и установка методов проверок и обработки ошибок
        :param methods: список методов проверок
        :param handler: обработчик ошибок
        :return: ``None``
        """

        if not isinstance(methods, list):                             # проверяем, чтобы methods был списком; иначе, ...
            raise TypeError(f'Параметр methods должен быть списком '
                            f'методов проверки (в действительности '
                            f'тип methods — {type(methods)}')         # ... поднимаем исключение

        for method in methods:                                        # для каждого method в списке methods ...
            if not callable(method):                                  # ... проверяем, чтобы был именно методом; иначе, ...
                raise TypeError(f'Каждый элемент списка methods '
                                f'должен быть методом (callable). '
                                f'Фактически обнаружен тип '
                                f'{type(method)}')                    # ... ... поднимаем исключение

        if handler is not None and not callable(handler):             # если handler не является методом или None, то ...
            raise TypeError(f'Метод обработки ошибок (handler) '
                            f'должен быть методом (callable) или '
                            f'None (в действительности тип handler '
                            f'— {type(handler)}')                     # ... поднимаем исключение

        self._methods = methods                                       # устанавливаем список методов валидации (они будут применены циклом)
        self._handler = handler                                       # устанавливаем метод обработки ошибок

    def validate(self, obj: Any, **params: VParams) -> None:
        """
        Собственно, валидация
        :param obj: объект валидации
        :param params: параметры валидации
        :return: ``None`` (в случае неудачи проверки будет поднято соответствующее исключение и вызван обработчик)
        """

        def _en(error_class: type[ValidationError]) -> str | None:
            """
            Позволяет получить "чистое" наименование типа ошибки из строки, которую возвращает type

            :param error_class: результат работы функции type(ERROR)
            :return: строка, содержащая "чистое" наименование ошибки (например, TypeError) или ничего
            """

            pattern = r'<class \'__main__\.(.*?)\'>'                  # паттерн для выделения наименования типа ошибки из ее класса
            match = search(pattern, str(error_class))                 # выполняем поиск по паттерну
            return match.group(1) if match else None                  # возвращаем результат, если что-то нашлось

        for method in self._methods:                                  # для каждого метода в списке методов, ...
            try:                                                      # ... попытаемся ...
                method(obj, params)                                   # ... ... применить метод к объекту с соответствующими параметрами
            except ValidationError as er:                             # ... в случае неудачи, ...
                if self._handler is None:                             # ... ... если нет метода обработки ошибки, ...
                    print(f'Ошибка [💥={_en(type(er))}] '
                          f'c cообщением [✉️="{er.args[0]}"]. '
                          f'Обработчик не установлен 🚫')             # ... ... ... сообщим об этом
                else:                                                 # ... ... иначе, ...
                    self._handler(e, obj)                             # ... ... ... выполним метод обработки ошибки

    def validate_with(self, **params: VParams) -> Callable:
        """
        Декоратор (с параметрами в виде именованных аргументов)

        :param params: аргументы, необходимые для валидации
        :return: конкретная функция валидации
        """

        def decorator(func):                                          # декоратор
            def wrapper(obj, *args, **kwargs):                        # метод-обертка
                self.validate(obj, **params)                          # собственно, метод валидации
                return func(obj, *args, **kwargs)                     # возвращаем реальный метод (с параметрами)
            return wrapper                                            # возвращаем обертку
        return decorator                                              # возвращаем декоратор


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
