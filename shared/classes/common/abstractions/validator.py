"""
**Абстрактный валидатор (валидация входных значений)**

Валидатор, обеспечивающий проверку значений перед их установкой (может быть
использован через декоратор с параметрами)
"""

from inspect import signature
from re import search
from typing import Any, Callable, Dict, List, Optional, TypeAlias


KWArgs: TypeAlias = Dict[str, Any]
"""
Псевдоним именованных аргументов
"""

VParams: TypeAlias = Optional[KWArgs]
"""
Псевдоним необязательного параметра в виде именованных аргументов
"""

VMethod: TypeAlias = Callable[[Any, VParams], bool]
"""
Псевдоним для метода валидации
"""

VMethods: TypeAlias = List[VMethod]
"""
Псевдоним для метода валидации
"""

EHandler: TypeAlias = Optional[Callable[[Exception, Any], None]]
"""
Псевдоним для метода обработки ошибок
"""


class ValidationError(Exception):
    """
    **Базовый класс "Ошибка валидации"**

    Базовый класс для исключений валидации
    """

    # Реализация не требуется
    ...


class Validator:
    """
    **Базовый класс "Валидатор"**

    Валидатор, способный циклом выполнять по отношению к объекту проверки
    (``obj``) список методов проверки (``methods``), поднимая соответствующие
    исключения в случае неудач
    """

    def __init__(self, methods: VMethods, handler: EHandler = None) -> None:
        """
        **Инициализация экземпляра**

        Инициализация и установка методов проверок и обработки ошибок
        :param methods: список методов проверок
        :param handler: обработчик ошибок
        :return: ``None``
        """
        if not isinstance(methods, list):
            raise TypeError(f'Параметр methods должен быть списком '
                            f'методов проверки (в действительности '
                            f'тип methods — {type(methods)}')

        if not methods:
            raise TypeError('Список методов не должен быть пустым: '
                            'пропадает смысл проверок')

        for method in methods:
            if not callable(method):
                raise TypeError(f'Каждый элемент списка methods '
                                f'должен быть методом (callable). '
                                f'Фактически обнаружен тип '
                                f'{type(method)}')

            sign = signature(method)
            if 'return' in sign.parameters:
                r_type = sign.parameters['return'].annotation
                if not (r_type == bool or r_type == Optional[bool]):
                    raise TypeError(f'Конкретный метод проверки '
                                    f'должен возвращать значение '
                                    f'булева типа. По факту тип'
                                    f'возвращаемого значения - '
                                    f'{r_type}')
            else:
                raise TypeError('Конкретный метод проверки должен '
                                'возвращать значения булева типа. '
                                'По факту метод ничего не '
                                'возвращает вообще')

        if handler is not None and not callable(handler):
            raise TypeError(f'Метод обработки ошибок (handler) '
                            f'должен быть методом (callable) или '
                            f'None (в действительности тип handler '
                            f'— {type(handler)}')

        self._methods = methods
        self._handler = handler

    def validate(self, obj: Any, **params: VParams) -> None:
        """
        **Метод валидации**

        Выполняется валидация (в случае неудачи проверки будет поднято
        соответствующее исключение и вызван обработчик)

        Собственно, валидация
        :param obj: объект валидации
        :param params: параметры валидации
        :return: ``None``
        """
        def _en(error_class: type[ValidationError]) -> str | None:
            """
            **Метод получения имени ошибки**

            Позволяет получить "чистое" наименование типа ошибки из
            строки, которую возвращает type

            :param error_class: результат работы функции type(ERROR)
            :return: строка, содержащая "чистое" наименование ошибки
            (например, TypeError) или ничего
            """
            pattern = r'<class \'__main__\.(.*?)\'>'
            match = search(pattern, str(error_class))
            return match.group(1) if match else None

        for method in self._methods:
            try:
                method(obj, params)
            except ValidationError as er:
                if self._handler is None:
                    print(f'Ошибка [💥={_en(type(er))}] '
                          f'c cообщением [✉️="{er.args[0]}"]. '
                          f'Обработчик не установлен 🚫')
                else:
                    self._handler(er, obj)

    def validate_with(self, **params: VParams) -> Callable:
        """
        ** Декоратор **

        Декоратор (с параметрами в виде именованных аргументов)

        :param params: аргументы, необходимые для валидации
        :return: конкретная функция валидации
        """
        def decorator(func):
            def wrapper(obj, *args, **kwargs):
                self.validate(obj, **params)
                return func(obj, *args, **kwargs)
            return wrapper
        return decorator
