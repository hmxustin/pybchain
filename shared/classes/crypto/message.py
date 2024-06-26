"""
Определен класс Message (согласно требованиям, описанным в wiki: https://github.com/hmxustin/pybchain/wiki/Message)
"""

from enum import Enum
from typing import Union
from dataclasses import dataclass

# region Константы общего назначения

BITS_IN_BYTE = 8
""" Количество битов в байте """

MIN_LENGTH = 0
""" Минимальная длина сообщения в битах """

MAX_LENGTH_IN_BITS = 8_589_934_592
""" Максимальная длина сообщения в битах """

MAX_LENGTH = MAX_LENGTH_IN_BITS // BITS_IN_BYTE
""" Максимальная длина сообщения в байтах (всё-таки данные хранятся в байтах) """

LENGTH_SIZE = 64
""" Размер в битах слова (QWord), представляющего собой значение длины сообщения в битах """

DEF_ENCODING = 'utf-8'
""" Кодировка строки по умолчанию """

DEF_METHOD = 'sha256'
""" Метод хеширования по умолчанию """

EMPTY_MESSAGE = bytearray([])
""" Пустое сообщение """

# endregion

# region Сообщения об ошибках

E_METHOD_TYPE = '🚨 Ошибочный тип данных {} при указании метода хеширования. Ожидается строка или перечисление "Method"'
""" Сообщение об ошибке при получении некорректного типа данных при установке метода хеширования """

E_METHOD_NAME = '🚨 Ошибочное наименование {} при указании метода хеширования. Ожидается строка, перечисленная в "Method.*.nme"'
""" Сообщение об ошибке при попытке указать некорректное наименование для метода хеширования (указание через строку) """

E_ENCODING_TYPE = ('🚨 Ошибочный тип данных {} при указании кодовой таблицы (способа интерпретации данных). Ожидается строка или '
                   'перечисление "Encoding"')
""" Сообщение об ошибке при получении некорректного типа данных при установке кодировки """

E_ENCODING_NAME = ('🚨 Ошибочное наименование {} при указании кодовой таблицы (способа интерпретации данных). Ожидается строка, '
                   'перечисленная в "Encoding.*.nme"')
""" Сообщение об ошибке при попытке указать некорректное наименование для кодировки (при указании через строку) """

E_DATA_TYPE = '🚨 Ошибочный тип данных {} при указании исходной совокупности данных. Ожидается строка, последовательность или массив байтов'
""" Сообщение об ошибке при получении некорректного типа данных при установке исходных данных """

E_DATA_LENGTH = ('🚨 Слишком большой массив (фактическая длина в байтах: {}) для хеширования. Максимальная длина в байтах не должна '
                 'превышать {}')
""" Сообщение об ошибке при получении некорректного типа данных при установке исходных данных """

# endregion


@dataclass
class EncodingInfo:
    """ Сведения о кодировке сообщения (как следует интерпретировать совокупность данных) """

    idx: int                                                          # индекс
    nme: str                                                          # наименование
    readable: bool                                                    # признак читаемости (с точки зрения человека)


class Encoding(EncodingInfo, Enum):
    """ Перечисление всех доступных кодировок сообщения (способов интерпретации совокупности данных) """

    bnr = 100, 'bnr', False                                           # просто бинарные данные, не для чтения (binary non-readable)
    bin = 200, 'bin', True                                            # данные должны интерпретироваться как бинарная строка
    hex = 201, 'hex', True                                            # данные должны интерпретироваться как шестнадцатеричная строка
    utf8 = 300, 'utf-8', True                                         # стандартная кодировка (человеко-читаемый текст)
    cp1251 = 301, 'cp1251', True                                      # может быть реализовано при необходимости в процессе...
    cp866 = 302, 'cp866', True                                        # ... функционального развития проекта
    koi8r = 303, 'koi8-r', True                                       # ...

    # todo Добавьте ниже дополнительную кодировку при необходимости в формате: идентификатор = индекс, 'наименование', признак читаемости


@dataclass
class MethodInfo:
    """ Сведения о методе хеширования (какой метод следует применить к совокупности данных при вызове hash()) """

    idx: int                                                          # индекс
    nme: str                                                          # наименование
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
        self._set_method(method)                                      # фактически устанавливаем значение с соответствующими проверками

        self._encoding: Encoding                                      # инициализация кодировки (способа интерпретации входных данных)
        self._set_encoding(encoding)                                  # фактическая установка значения с соответствующими проверками

        self._data: bytearray                                         # инициализация совокупности данных
        self._set_data(data)                                          # фактическая установка данных с проверками и преобразованиями

    def _set_method(self, method: Method) -> None:
        """
        Установка метода хеширования исходной совокупности данных. Перед установкой производится проверка: на корректность типа данных, а
        в случае, если поступила строка, проверяется еще и значение (на предмет соответствия одному из значений ENum-а)

        :param method: метод хеширования, который требуется применить к исходной совокупности данных при вызове hash()
        :return: ``None``
        """

        t = type(method)                                              # получаем тип

        if t is str:                                                  # если пришла строка, то...
            found = None                                              # ... инициализируем поиск
            for i in Method:                                          # ... начинаем искать среди значений EMun-а
                if method == i.nme:                                   # ... ... если нашли, то...
                    found = i                                         # ... ... ... сохраняем найденного
                    break                                             # ... ... ... прекращаем поиск

            if not found:                                             # ... если не найдено совпадений, то...
                raise ValueError(E_METHOD_NAME.format(method))        # ... ... поднимаем исключение (ошибочное значение)

            self._method = found                                      # ... если пришли сюда, значит, можно устанавливать значение (ENum)
            return                                                    # ... больше нам тут делать нечего

        if t is Method:                                               # если пришел ENum, то...
            self._method = method                                     # ... проверять нечего, можно устанавливать значение (ENum)
            return                                                    # ... больше нам тут делать нечего

        raise TypeError(E_METHOD_TYPE.format(t))                      # ... если пришли сюда, значит поднимаем исключение (ошибка типа)

    def _set_encoding(self, encoding: Encoding) -> None:
        """
        Установка кодировки (способа интерпретации данных). Перед установкой производится проверка на корректность типа данных, а если
        поступила строка, дополнительно проверяется ее значение (на предмет соответствия одному из допустимых значений ENum-a)

        :param encoding: кодировка (способ интерпретации данных)
        :return: ``None``
        """

        t = type(encoding)                                            # получаем тип

        if t is str:                                                  # если пришла строка, то...
            found = None                                              # ... инициализируем поиск
            for i in Encoding:                                        # ... начинаем искать среди значений EMun-а
                if encoding == i.nme:                                 # ... ... если нашли, то...
                    found = i                                         # ... ... ... сохраняем найденного
                    break                                             # ... ... ... прекращаем поиск

            if not found:                                             # ... если не найдено совпадений, то...
                raise ValueError(E_ENCODING_NAME.format(encoding))    # ... ... поднимаем исключение (ошибочное значение)

            self._encoding = found                                    # ... если уж нашли, то устанавливаем значение
            return                                                    # ... больше нам тут делать нечего

        if t is Encoding:                                             # если получили ENum, то...
            self._encoding = encoding                                 # ... проверять нечего, просто устанавливаем значение
            return                                                    # ... больше нам тут делать нечего

        raise TypeError(E_ENCODING_TYPE.format(t))                    # ююю если пришли сюда, значит получен некорректный тип данных

    def _set_data(self, data: TData) -> None:
        """
        Фактическая установка данных с соответствующими предварительными проверками и преобразованиями

        :param data: исходные данные (в том виде, как они поступили)
        :return: ``None``
        """

        t = type(data)                                                # получаем тип

        if t not in [str, bytes, bytearray]:                          # если тип данных не входит в допустимый перечень, то ...
            raise TypeError(E_DATA_TYPE.format(t))                    # ... поднимаем исключение

        actual_setters = {                                            # перечень методов, которые реально будут обрабатывать входные данные
            str: self._set_data_from_str,                             # ... для случая, если входные данные представлены строкой
            bytes: self._set_data_from_bytes,                         # ... -*-*- последовательностью байтов
            bytearray: self._set_data_from_bytearray                  # ... -*-*- массивом байтов
        }

        setter = actual_setters[t]                                    # выбираем сеттер в зависимости от реального типа входных данных
        setter(data)                                                  # noqa вызываем конкретный актуальный сеттер

    def _set_data_from_str(self, data: str) -> None:
        """
        Фактическая установка данных из исходной строки с соответствующими предварительными проверками и преобразованиями

        :param data: исходные данные (в виде строки)
        :return: ``None``
        """

        actual_setters = {
            Encoding.bnr: self._set_data_from_str_as_utf8,
            Encoding.bin: self._set_data_from_str_as_bin,
            Encoding.hex: self._set_data_from_str_as_hex
        }

        setter = actual_setters[self._encoding]
        setter(data)                                                  # noqa вызываем конкретный актуальный сеттер

    def _set_data_from_str_as_utf8(self, data: str) -> None:
        """
        Установка значений из строки, которую следует интерпретировать как обычную человеко-читаемую строку в кодировке utf-8

        :param data: исходная строка
        :return: ``None``
        """

        ...

    def _set_data_from_str_as_bin(self, data: str) -> None:
        """
        Установка значений из строки, которую следует интерпретировать как бинарную строку (то есть, строку из нулей, единиц и пробелов
        (все пробелы будут удалены))

        :param data: исходная бинарная строка
        :return: ``None``
        """

        ...

    def _set_data_from_str_as_hex(self, data: str) -> None:
        """
        Установка значений из строки, которую следует интерпретировать как шестнадцатеричную строку (то есть, строку из символов
        шестнадцатеричного алфавита и пробелов (все пробелы будут удалены))

        :param data: исходная шестнадцатеричная строка
        :return: ``None``
        """

        ...

    def _set_data_from_bytes(self, data: bytes) -> None:
        """
        Фактическая установка данных из последовательности байтов с соответствующими предварительными проверками и преобразованиями

        :param data: исходные данные (в виде последовательности байтов)
        :return: ``None``
        """

        data = bytearray(data)                                        # преобразуем в массив байтов
        self._set_data_from_bytearray(data)                           # вызываем метод установки значения

    def _set_data_from_bytearray(self, data: bytearray) -> None:
        """
        Фактическая установка данных из исходной строки с соответствующими предварительными проверками и преобразованиями

        :param data: исходные данные (в виде строки)
        :return: ``None``
        """

        ln = len(data)                                                # получаем фактическую длину массива в байтах

        if ln > MAX_LENGTH:                                           # если длина больше, чем нужно, ...
            args = (str(ln), str(MAX_LENGTH))                         # ... формируем сообщение
            raise ValueError(E_DATA_LENGTH.format(*args))             # ... поднимаем исключение

        self._data = data                                             # все ок -> устанавливаем данные

    @property
    def method(self) -> Method:
        """
        Свойство: "Метод"

        :return: метод (хеширования)
        """

        return self._method                                           # возвращаем хранимое значение

    @method.setter
    def method(self, method: Method) -> None:
        """
        Сеттер свойства "Метод"

        :param method: устанавливаемый метод хеширования (алгоритм)
        :return: ``None``
        """

        self._set_method(method)                                      # вызываем внутренний метод установки значения

    @property
    def encoding(self) -> Encoding:
        """
        Свойство "Кодировка" (кодовая таблица или способ интерпретации данных)

        :return: кодировка
        """

        return self._encoding                                         # возвращаем хранимое значение

    @encoding.setter
    def encoding(self, encoding) -> None:
        """
        Сеттер свойства "Кодировка"

        :param encoding: устанавливаемая кодировка (способ интерпретации данных)
        :return: ``None``
        """
        self._set_encoding(encoding)                                  # вызываем внутренний метод установки значения
