from django.db import models

class Certificate(models.Model):
    CATEGORY_CHOICES = [
        ('teachers', 'Мұғалімдер'),
        ('students', 'Оқушылар'),
    ]

    LEVEL_CHOICES = [
        ('district', 'Аудан деңгейі'),
        ('city', 'Қала деңгейі'),
    ]

    title = models.CharField('Атауы', max_length=200)
    year = models.CharField('Жыл', max_length=4)
    image = models.ImageField('Сурет', upload_to='certificates/')
    category = models.CharField('Категория', max_length=20, choices=CATEGORY_CHOICES)
    level = models.CharField('Деңгей', max_length=20, choices=LEVEL_CHOICES)
    order = models.IntegerField('Реттілік', default=0)
    created_at = models.DateTimeField('Құрылған күні', auto_now_add=True)
    updated_at = models.DateTimeField('Өзгертілген күні', auto_now=True)

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаттар'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.year})"