from django.db import models

class Subscribers(models.Model):
    """
    Model representing a Post.
    """
    email = models.EmailField(max_length=254, blank=True, default="")
    confirmation = models.BooleanField(default=False)
    randomkey = models.CharField(max_length=100, help_text="Рандомный ключ")
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.email

    class Meta:
        ordering = ["email"]