from django.db import models


class AbstractName(models.Model):
    """Абстрактная модель с полем name."""

    name = models.CharField(
        'Название',
        max_length=128,
        unique=True
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name
