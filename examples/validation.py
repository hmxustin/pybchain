import shared.classes.basic.abstractions.validator as v


def _is_string(obj: v.VObj, params: v.VParams) -> None:
    t = type(obj)
    if t != str:
        raise v.ValidationError(
            f'Полученный объект {repr(obj)} имеет некорректный тип {t}. '
            f'Требуется строка'
        )


def _correct_length(obj: v.VObj, params: v.VParams) -> None:
    mn = params.get('min_length', 1)
    mx = params.get('max_length', 32)
    ln = len(obj)
    if not mn <= ln <= mx:
        raise v.ValidationError(
            f'Некорректная длина строки. Требуется строка длинной в пределах '
            f'от {mn} до {mx} (включительно). '
            f'Фактическая длина полученной строки составляет {ln}'
        )


vld = v.Validator([
    _is_string,
    _correct_length
])


# class UserName:
# 
#     def __init__(self, value: str) -> None:
# 
#         self._value = value
# 
# 
# 
# try:
#     user_name1 = UserName(vld.validate(1))
# except v.ValidationError as er:
#     print(er)
# 
# user_name2 = UserName(vld.validate('Вася', min_length=1, max_length=10))
# 
# user_name3 = UserName('Мегавасисуализавр')


class UserName:
    @vld.validate_with(max_length=10, min_length=1)                   # noqa
    def __init__(self, value):
        self._value = value


u_name = UserName('Вася')
