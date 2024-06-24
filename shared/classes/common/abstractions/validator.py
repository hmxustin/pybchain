"""
**Абстрактный валидатор (валидация входных значений)**

Валидатор, обеспечивающий проверку значений перед их установкой (может быть
использован через декоратор с параметрами)
"""

from inspect import signature
from re import search
from typing import (
    Any, Callable, Dict, List, Optional, Tuple, TypeAlias, TypeVar
)


VObject: TypeAlias = Any
"""
Псевдоним для валидируемого объекта (объекта проверок)
"""

Args: TypeAlias = Tuple
"""
Псевдоним для кортежа аргументов
"""

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

T = TypeVar('T', bound='Validator')
"""
Аннотация типа для self в классе ``Validator``
"""


class ValidationError(Exception):
    """
    **Базовый класс "Ошибка валидации"**

    Базовый класс для исключений валидации
    """

    # Реализация не требуется


class Validator:
    """
    **Базовый класс "Валидатор"**

    Валидатор, способный циклом выполнять по отношению к объекту проверки
    (``obj``) список методов проверки (``methods``), поднимая соответствующие
    исключения в случае неудач
    """
    # region Константы
    E_NOT_LIST = ('💥 Параметр methods должен быть списком (list) методов '
                  'проверки (фактический тип полученного methods — {})')
    """
    Сообщение об ошибке, если ``methods`` не является списком
    """

    E_EMPTY_LIST = ('💥 Список методов не должен быть пустым: требуется по '
                    'меньшей мере один метод проверки')
    """
    Сообщение об ошибке, если ``methods`` является пустым списком
    """

    E_NON_CALLABLE = ('💥 Каждый элемент списка methods должен быть методом ('
                      '"callable". Вместо этого обнаружен объект типа {}')
    """
    Сообщение об ошибке, если элемент ``methods`` не является методом
    """

    E_NON_CALLABLE_H = ('💥 Объект handler должен быть методом (callable) или '
                        'None (фактический тип полученного handler — {}')
    """
    Сообщение об ошибке, если элемент ``handler`` не является методом
    """

    E_INFO = 'Ошибка [💥={}] c cообщением [✉️="{}"]. Обработчик не установлен'
    """
    Общий формат вывода сообщения об ошибке, если внешний обработчик не поступил
    """
    # endregion

    def __init__(self: T, methods: VMethods, handler: EHandler = None) -> None:
        """
        **Инициализация экземпляра**

        Инициализация и установка методов проверок и обработки ошибок
        :param methods: список методов проверок
        :param handler: обработчик ошибок
        :return: ``None``
        """
        if not isinstance(methods, list):
            tpe = type(methods)
            raise TypeError(self.E_NOT_LIST.format(tpe))

        if not methods:
            raise TypeError(self.E_EMPTY_LIST)

        for method in methods:
            if not callable(method):
                tpe = type(method)
                raise TypeError(self.E_NON_CALLABLE.format(tpe))

            sign = signature(method)
            if 'return' in sign.parameters:
                r_type = sign.parameters['return'].annotation
                if not (r_type == bool or r_type == Optional[bool]):
                    msg = (f'Конкретный метод проверки должен возвращать '
                           f'значение булева типа. По факту тип возвращаемого '
                           f'значения — {r_type}')
                    raise TypeError(msg)
            else:
                raise TypeError('Конкретный метод проверки должен '
                                'возвращать значения булева типа. '
                                'По факту метод ничего не '
                                'возвращает вообще')

        if handler is not None and not callable(handler):
            tpe = type(handler)
            raise TypeError(self.E_NON_CALLABLE_H.format(tpe))

        self._methods = methods
        self._handler = handler

    def validate(self: T, obj: VObject, **params: VParams) -> None:
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
                    en = _en(type(er))
                    msg = er.args[0]
                    print(self.E_INFO.format(en, msg))
                else:
                    self._handler(er, obj)

    def validate_with(self: T, **params: VParams) -> Callable:
        """
        ** Декоратор **

        Декоратор (с параметрами в виде именованных аргументов)

        :param params: аргументы, необходимые для валидации
        :return: конкретная функция валидации
        """
        def decorator(func: Callable) -> Callable:
            def wrapper(obj: VObject, *args: Args,
                        **kwargs: VParams) -> Callable:
                self.validate(obj, **params)
                return func(obj, *args, **kwargs)
            return wrapper
        return decorator
