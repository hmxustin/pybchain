"""
**Сообщения об ошибках**

Сообщения об ошибках, используемые в классе ``Validator`` согласно
требованиям https://clck.ru/3BUKJk
"""

NOT_LIST = (
    '💥 Параметр methods должен быть списком (list) методов проверки ('
    'фактический тип полученного methods — {})'
)

EMPTY_LIST = (
    '💥 Список методов не должен быть пустым: требуется по меньшей мере один '
    'метод проверки'
)

NON_CALLABLE_M = (
    '💥 Каждый элемент списка methods должен быть методом ("callable". Вместо '
    'этого обнаружен объект типа {}'
)

NON_CALLABLE_H = (
    '💥 Объект handler должен быть методом (callable) или None (фактический '
    'тип полученного handler — {}'
)

INFO = (
    'Ошибка [💥={}] c cообщением [✉️="{}"]. Обработчик не установлен ('
    'данное сообщение сгенерировано самим валидатором'
)

NOT_ENOUGH_PARAMS = (
    '💥 Полученный метод должен принимать не менее двух параметров'
)

NOT_RAISES = (
    '💥 Полученный в качестве конкретного валидатора метод должен содержать '
    'вызов исключения, но не содержит ни одного вызова raise'
)

PARAM_IS_NOT_EXCEPTION = (
    '💥 Первый параметр метода обработки исключений должен быть типа '
    'Exception, но не относится к данному типу'
)

PARAM_IS_NOT_ANY = (
    '💥 Параметр должен быть типа Any, но не относится к данному типу'
)

RET_NOT_NONE = (
    '💥 Полученный метод содержит возвращаемое значение, В то время как он не '
    'должен ничего возвращать'
)

PARAM_IS_NOT_DICT = (
    '💥 Параметр должен быть типа Dict, но не относится к данному типу'
)

ONE_PARAM_REQUIRED = (
    '💥 Полученный метод должен принимать хотя бы один параметр]'
)

UNKNOWN_ERR = (
    '💥 Произошла непредвиденная ошибка'
)
