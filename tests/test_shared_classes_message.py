from shared.classes.crypto.message import *


def testp_initialization():
    # при создании инстанса можно указать метод хеширования сообщения в виде строки (реальное значение будет установлено из
    # перечисления Method)

    m = Message(method='sha-256')                                     # задаем значение строкой
    assert m._method == Method.sha256                                 # получаем элемент перечисления

    # разумеется, можно указать и через перечисление

    m = Message(method=Method.sha256)                                 # задаем перечислимым типом
    assert m._method.info == 'sha-256'                                # проверяем, что нужное значение установилось


