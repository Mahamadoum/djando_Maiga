from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class RussianNameValidator:


    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя- '"

    def __init__(self, message=None):
        self.message = message or "Имя должно содержать только русские буквы, дефис и пробел"

    def __call__(self, value):
        if value and not all(c in self.ALLOWED_CHARS for c in value):
            raise ValidationError(self.message)