"""
Определен класс Message (согласно требованиям, описанным в wiki: https://github.com/hmxustin/pybchain/wiki/Message)
"""

from enum import Enum
from dataclasses import dataclass
from typing import Union

# region Константы общего назначения

BITS_IN_BYTE = 8
""" Количество битов в байте """

MIN_LENGTH = 0
""" Минимальная длина сообщения в битах """

MAX_LENGTH = 2**64
""" Максимальная длина сообщения в битах """

LENGTH_SIZE = 64
""" Размер в битах слова (QWord), представляющего собой значение длины сообщения в битах """

DEF_ENCODING = 'utf-8'
""" Кодировка строки по умолчанию """

DEF_METHOD = 'sha256'
""" Метод хеширования по умолчанию """

EMPTY_MESSAGE = bytearray()
""" Пустое сообщение """

# endregion

# region Сообщения об ошибках

E_INVALID_METHOD_TYPE = '🚨 Ошибочный типа данных {} при указании метода хеширования. Ожидается строка или перечисление "Method"'


# endregion


@dataclass
class EncodingInfo:
    """ Сведения о кодировке сообщения (как следует интерпретировать совокупность данных) """

    idx: int                                                          # индекс
    info: str                                                         # наименование
    readable: bool                                                    # признак читаемости (с точки зрения человека)


class Encoding(EncodingInfo, Enum):
    """ Перечисление всех доступных кодировок сообщения (способов интерпретации совокупности данных) """

    bnr = 100, 'bnr', False                                           # просто бинарные данные, не для чтения (binary non-readable)
    binstr = 200, 'binstr', True                                      # данные должны интерпретироваться как бинарная строка
    hexstr = 201, 'hexstr', True                                      # данные должны интерпретироваться как шестнадцатеричная строка
    utf8 = 300, 'utf-8', True                                         # стандартная кодировка (человеко-читаемый текст)
    cp1251 = 301, 'cp1251', True                                      # может быть реализовано при необходимости в процессе...
    cp866 = 302, 'cp866', True                                        # ... функционального развития проекта
    koi8r = 303, 'koi8-r', True                                       # ...

    # todo Добавьте ниже дополнительную кодировку при необходимости в формате: идентификатор = индекс, 'наименование', признак читаемости

@dataclass
class MethodInfo:
    """ Сведения о методе хеширования (какой метод следует применить к совокупности данных при вызове hash()) """

    idx: int                                                          # индекс
    info: str                                                         # наименование
    acceleration: bool                                                # доступно ли аппаратное ускорение


class Method(MethodInfo, Enum):
    """ Перечисление всех доступных методов хеширования """

    sha256 = 10, 'sha-256', True                                      # метод sha-256 с ускорением на уровне CPU (Intel® SHA Extensions)

    # todo Добавьте ниже дополнительный метод хеширования в формате: идентификатор = индекс, 'наименование', имеет ли аппаратное ускорение


TData = Union[str, bytes, bytearray]
""" Допустимые типы входящих (исходных) данных для сообщения """

TEncoding = Union[Encoding, str]
""" Допустимые типы для установки кодировки """

TMethod = Union[Method, str]
""" Допустимые типы для установки метода хеширования """


class Message:
    """ Сообщение, подлежащее хешированию (совокупность данных, описанная в спецификации) """

    def __init__(self, data: TData = EMPTY_MESSAGE, encoding: TEncoding = Encoding.utf8, method: TMethod = Method.sha256) -> None:
        """
        Метод создания экземпляра класса и установки начальных значений

        :param data: исходная совокупность данных
        :param encoding: кодировка (способ интерпретации исходной совокупности данных)
        :param method: метод хеширования, который требуется применить к исходной совокупности данных при вызове hash()
        :return: ``None``
        """
        ...

        self._method: Method                                          # инициация метода хеширования
        self._set_method(method)

    def _set_method(self, method: Method) -> None:
        """
        Установка метода хеширования исходной совокупности данных

        :param method: метод хеширования, который требуется применить к исходной совокупности данных при вызове hash()
        :return: ``None``
        """

        t = type(method)

        if t is str:
            print('1')
            return

        if t is Method:
            self._method = method
            return

        raise TypeError(E_INVALID_METHOD_TYPE.format(t))


