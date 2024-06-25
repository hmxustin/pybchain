"""
**Абстрактный валидатор (валидация входных значений)**

Валидатор, обеспечивающий проверку значений перед их установкой (может быть
использован через декоратор с параметрами)
"""

from inspect import signature, Signature
from re import search
from typing import TypeVar

from ._errors import *
from ._typing import *
from ._validation_error import *


T = TypeVar('T', bound='Validator')
"""
**Типизация self**

Аннотация типа для self в классе ``Validator``
"""


class Validator:
    """
    **Базовый класс "Валидатор"**

    Валидатор, способный циклом выполнять по отношению к объекту проверки
    (``obj``) список методов проверки (``methods``), поднимая соответствующие
    исключения в случае неудач
    """

    def __init__(self: T, methods: VMethods, handler: EHandler = None) -> None:
        """
        **Инициализация экземпляра**

        Инициализация и установка методов проверок и обработки ошибок
        :param methods: список методов проверок
        :param handler: обработчик ошибок
        :return: ``None``
        """
        self._methods = []

        if not isinstance(methods, list):
            tpe = type(methods)
            raise TypeError(NOT_LIST.format(tpe))

        if not methods:
            raise TypeError(EMPTY_LIST)

        for method in methods:
            self._set_method(method)

        if handler is not None and not callable(handler):
            tpe = type(handler)
            raise TypeError(self.E_NON_CALLABLE_H.format(tpe))

        if handler:
            sign = signature(handler)
            params = list(sign.parameters.values())

            if len(params) < 2:
                raise TypeError(self.E_NOT_ENOUGH_PARAMS)

            # Проверяем первый аргумент (исключая self, если это метод класса)
            first_param = params[0] if params[0].name != 'self' else params[1]
            if first_param.annotation != Exception:
                return

            # Проверяем второй аргумент
            second_param = params[1] if params[0].name != 'self' else params[2]
            if second_param.annotation != Any:
                return False

        self._handler = handler

    def _set_method(self: T, method: VMethod):
        if not callable(method):
            tpe = type(method)
            raise TypeError(NON_CALLABLE_M.format(tpe))

        sign = signature(method)
        ra = sign.return_annotation
        if ra is not Signature.empty:
            raise TypeError(self.E_RET_NOT_NONE)

    def validate(self: T, obj: VObj, **params: VParams) -> None:
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
            def wrapper(obj: VObj, *args: Args,
                        **kwargs: VParams) -> Callable:
                self.validate(obj, **params)
                return func(obj, *args, **kwargs)
            return wrapper
        return decorator
