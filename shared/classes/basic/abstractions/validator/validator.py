"""
**Абстрактный валидатор (валидация входных значений)**

Валидатор, обеспечивающий проверку значений перед их установкой (может быть
использован через декоратор с параметрами). Модуль разработан согласно
требованиям https://clck.ru/3BUKJk
"""

from ast import Raise, parse, walk
from inspect import Signature, getsource, signature
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
        self._handler = None

        if not isinstance(methods, list):
            tpe = type(methods)
            raise TypeError(NOT_LIST.format(tpe))

        if not methods:
            raise TypeError(EMPTY_LIST)

        for method in methods:
            self._set_method(method)

        if handler is not None and not callable(handler):
            tpe = type(handler)
            raise TypeError(NON_CALLABLE_H.format(tpe))

        if handler:
            self._set_handler(handler)

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
                    # print(INFO.format(en, msg))
                    raise ValidationError(INFO.format(en, msg))
                else:
                    self._handler(er, obj)

            except Exception as er:
                raise Exception(UNKNOWN_ERR)

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

    def _set_method(self: T, method: VMethod) -> None:
        """
        **Установка значений конкретных методов валидации**

        Проверяем каждый полученный конкретный метод валидации и добавляем в
        список. Проверки осуществляются на предмет:
         - является ли вызываемым (должен);
         - не имеет ли возвращаемого значения (не должен);
         - содержит ли внутри вызов исключения (должен).

        :param method: отдельный конкретный метод валидации для проверки
        :return: ``None``
        """
        if not callable(method):
            tpe = type(method)
            raise TypeError(NON_CALLABLE_M.format(tpe))

        sign = signature(method)
        ra = sign.return_annotation

        if ra is not Signature.empty and ra is not None:
            raise TypeError(RET_NOT_NONE)

        params = list(sign.parameters.values())

        if len(params) < 1:
            raise TypeError(NOT_ENOUGH_PARAMS)

        first_param = params[0] if params[0].name != 'self' else params[1]

        if first_param.annotation != Any:
            raise TypeError(PARAM_IS_NOT_ANY)

        method_source = getsource(method)
        sem_tree = parse(method_source)
        contains_exception = False

        for node in walk(sem_tree):
            if isinstance(node, Raise):
                contains_exception = True
                break

        if not contains_exception:
            raise TypeError(NOT_RAISES)

        self._methods.append(method)

    def _set_handler(self: T, handler: EHandler) -> None:
        """
        **Установка метода обработки исключений**

        Проверяем полученный метод (здесь мы уже точно знаем, что он получен),
        и устанавливаем его. Проверки осуществляются на предмет:
         - имеется ли два параметра (или более);
         - является ли первый параметр исключением;
         - является ли второй параметр Any.

        :param handler: метод обработки исключительных ситуаций
        :return:
        """
        sign = signature(handler)
        params = list(sign.parameters.values())

        ra = sign.return_annotation

        if ra is not Signature.empty and ra is not None:
            raise TypeError(RET_NOT_NONE)

        if len(params) < 2:
            raise TypeError(NOT_ENOUGH_PARAMS)

        first_param = params[0] if params[0].name != 'self' else params[1]

        if first_param.annotation != Exception:
            raise TypeError(PARAM_IS_NOT_EXCEPTION)

        second_param = params[1] if params[0].name != 'self' else params[2]

        if second_param.annotation != Any:
            raise TypeError(PARAM_IS_NOT_ANY)

        self._handler = handler
