from pytest import raises as _

from shared.classes.crypto.message.message import *


def testp_initialization():
    # можно вообще ничего не указывать (все значения будут установлены по умолчанию, а в качестве данных - пустая последовательность)
    m = Message()
    assert m._data == EMPTY_MESSAGE
    assert m.encoding.nme == 'utf-8'                                  # проверяем, что там установилось
    assert m.method.nme == 'sha-256'                                  # проверяем имя метода хеширования

    # можно указать метод хеширования сообщения в виде строки (реальное значение все равно будет установлено из перечисления Method)
    m = Message(method='sha-256')                                     # задаем значение строкой
    assert m.method == Method.sha256                                  # проверяем, что мы получаем элемент перечисления
    assert m.method.nme == 'sha-256'                                  # проверяем имя

    # можно указать метод и через перечисление Method (это и является целевым способом)
    m = Message(method=Method.sha256)                                 # задаем перечислимым типом
    assert m.method.nme == 'sha-256'                                  # проверяем, что нужное значение установилось

    # указать кодировку (способ интерпретации данных) можно в виде строки (реальное значение все равно будет установлено типа Encoding)
    m = Message(encoding='bin')                                       # задаем значение строкой (можно: bnr, bin, hex, utf-8 и т.д.)
    assert m.encoding == Encoding.bin                                 # проверяем, что мы получаем конкретный элемент перечисления
    assert m.encoding.nme == 'bin'                                    # проверяем, что имя элемента перечисления указано верно

    # можно указать кодировку через перечисление Encoding (это и является целевым способом)
    m = Message(encoding=Encoding.utf8, method=Method.sha256)         # задаем значения целевым способом
    assert m.encoding.nme == 'utf-8'                                  # проверяем, что там установилось
    assert m.method.nme == 'sha-256'                                  # проверяем, что там установилось

    # можно изменить ранее установленное значение через обращение к свойствам
    m.method = Method.sha256                                          # ну, допустим мы меняем
    m.encoding = Encoding.bin                                         # устанавливаем другое значение
    assert m.encoding.nme == 'bin'                                    # проверяем, что там установилось
    assert m.method.nme == 'sha-256'                                  # проверяем, что там установилось

    # в качестве данных можно установить массив байтов (именно в такой форме данные будут храниться внутри объекта)
    d = bytearray([])                                                 # создаем массив
    for i in range(10):                                               # 10 раз...
        d.append(0x00)                                                # ... добавляем в него байты

    assert m._data == EMPTY_MESSAGE                                   # убедимся в том, что пока что там пусто
    m._set_data(d)                                                    # установим данные
    assert m._data == d                                               # убедимся в том, что данные установились


def testn_initialization():
    # при попытке указать в качестве метода хеширование что-либо кроме строки или Method, будет поднято исключение (несоответствие типов)
    with _(TypeError):
        m = Message(method=False)                                     # noqa тестируем попытку установить в качестве метода будево значение

    # при попытке строку, которой нет в Method (тип правильный, но значение не правильное), будет поднято исключение (ошибочное значение)
    with _(ValueError):
        m = Message(method='unknown')                                 # тестируем попытку установить в качестве метода "левую" строку

    with _(TypeError):
        m = Message(encoding=1.2)                                     # noqa тестируем попытку установить кодировку через вещественное число

    with _(ValueError):
        m = Message(encoding='bmp')                                   # тестируем попытку установить в качестве кодировки "левый" формат

    dx = bytearray(0x00.to_bytes(1_048_576, 'big'))    # создаем массив-заполнитель
    d = EMPTY_MESSAGE                                                 # создаем массив данных
    while len(d) <= MAX_LENGTH:                                       # заполняем массив данных заполнителем, пока не превысит MAX_LENGTH
        d += dx                                                       # ... добавляем очередную порцию

    assert len(d) > MAX_LENGTH                                        # убедимся, что длина больше допустимой

    with _(ValueError):
        m = Message(d)                                                # тестируем попытку установить слишком длинные данные
