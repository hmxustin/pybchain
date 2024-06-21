"""
Определен класс Message (согласно требованиям, описанным в wiki: https://github.com/hmxustin/pybchain/wiki/Message
"""

from enum import Enum
from dataclasses import dataclass

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


# endregion

@dataclass
class EncodingInfo:                                                   # сведения о кодировке сообщения
    idx: int                                                          # индекс
    info: str                                                         # наименование
    readable: bool                                                    # признак читаемости (с точки зрения человека)


class Encoding(EncodingInfo, Enum):
    bnr = 100, 'bnr', False                                           # просто бинарные данные, не для чтения (binary non-readable)
    binstr = 200, 'binstr', True                                      # данные должны интерпретироваться как бинарная строка
    hexstr = 201, 'hexstr', True                                      # данные должны интерпретироваться как шестнадцатеричная строка
    utf8 = 300, 'utf-8', True                                         # стандартная кодировка (человеко-читаемый текст)
    # cp1251 = 301, 'cp1251', True                                      остальное может быть реализовано при необходимости в процессе
    # cp866 = 302, 'cp866', True                                        функционального развития
    # koi8r = 303, 'koi8-r', True
