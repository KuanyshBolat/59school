from django.db import models

class NavLink(models.Model):
    name = models.CharField("Название", max_length=200)
    href = models.CharField("Ссылка", max_length=200)
    order = models.IntegerField("Порядок", default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Ссылка навигации'
        verbose_name_plural = 'Ссылки навигации'

    def __str__(self):
        return self.name

class Header(models.Model):
    logo = models.ImageField("Логотип", upload_to='header/', blank=True, null=True)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    email = models.CharField("Email", max_length=200, blank=True)
    nav_links = models.ManyToManyField(NavLink, blank=True)

    class Meta:
        verbose_name = 'Хэдер'
        verbose_name_plural = 'Хэдер'

    def __str__(self):
        return "Header"

class HeroSlide(models.Model):
    title = models.CharField("Заголовок", max_length=255, blank=True)
    subtitle = models.CharField("Подзаголовок", max_length=255, blank=True)
    image = models.ImageField("Изображение", upload_to='hero/')
    order = models.IntegerField("Порядок", default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Слайд Hero'
        verbose_name_plural = 'Слайды Hero'

    def __str__(self):
        return self.title or f"Slide {self.pk}"

class About(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    body = models.TextField("Текст")
    image = models.ImageField("Изображение", upload_to='about/', blank=True, null=True)

    class Meta:
        verbose_name = 'О школе'
        verbose_name_plural = 'О школе'

    def __str__(self):
        return self.title

class Stat(models.Model):
    number = models.CharField("Число", max_length=50)
    label = models.CharField("Подпись", max_length=200)
    order = models.IntegerField("Порядок", default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистики'

    def __str__(self):
        return f"{self.number} - {self.label}"

class Director(models.Model):
    name = models.CharField("Имя", max_length=200)
    title = models.CharField("Должность", max_length=200, blank=True)
    bio = models.TextField("Биография", blank=True)
    image = models.ImageField("Фото", upload_to='director/', blank=True, null=True)

    class Meta:
        verbose_name = 'Директор'
        verbose_name_plural = 'Директор'

    def __str__(self):
        return self.name

class ContactInfo(models.Model):
    address = models.CharField("Адрес", max_length=255, blank=True)
    phone = models.CharField("Телефон", max_length=100, blank=True)
    email = models.CharField("Email", max_length=200, blank=True)
    map_embed = models.TextField("Код карты (embed)", blank=True)

    class Meta:
        verbose_name = 'Контактная информация'
        verbose_name_plural = 'Контактная информация'

    def __str__(self):
        return "Contact Info"

class Footer(models.Model):
    title = models.CharField("Заголовок", max_length=200, blank=True)
    body = models.TextField("Текст", blank=True)
    links = models.TextField("Ссылки (JSON)", blank=True)

    class Meta:
        verbose_name = 'Футер'
        verbose_name_plural = 'Футер'

    def __str__(self):
        return self.title or "Footer"

class Page(models.Model):
    slug = models.SlugField("Slug", unique=True)
    title = models.CharField("Заголовок", max_length=200)
    body = models.TextField("Контент", blank=True)
    order = models.IntegerField("Порядок", default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    def __str__(self):
        return self.title

class ImageBlock(models.Model):
    page = models.ForeignKey(Page, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField("Изображение", upload_to='images/')
    caption = models.CharField("Подпись", max_length=255, blank=True)
    alt = models.CharField("Alt текст", max_length=255, blank=True)
    order = models.IntegerField("Порядок", default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.caption or f"Image {self.pk}"
