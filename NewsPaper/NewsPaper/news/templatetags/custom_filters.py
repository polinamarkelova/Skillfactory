from django import template


register = template.Library()

CENSOR_WORDS = [
    'дегустации',
    'жвачка'

]


@register.filter()
def censor(value):
    """
    text: текст к которому нужно применить фильтр
    """
    for word in CENSOR_WORDS:
        value = value.replace(word[1:], '*' * len(word[1:]))
    return value
