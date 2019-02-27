from django.db import models

class Subscribers(models.Model):
    """
    Модель пользователей обратной связи.
    """
    # e-mail пользователя
    email = models.EmailField(max_length=254, blank=True, default="")
    # Подтвержден ли почтовый ящик или нет
    confirmation = models.BooleanField(default=False)
    # Ключ подтверждения, который формируется в ссылке, отправленной на почту пользователя для подтверждения
    randomkey = models.CharField(max_length=100, help_text="Рандомный ключ")
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.email

    class Meta:
        ordering = ["email"]
