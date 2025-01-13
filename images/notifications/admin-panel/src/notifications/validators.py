from jinja2 import Environment, exceptions

from django.core.exceptions import ValidationError


def validate_jinja_template(template: str) -> None:
    try:
        Environment().parse(template)
    except exceptions.TemplateSyntaxError:
        raise ValidationError('синтаксическая ошибка в шаблоне')
