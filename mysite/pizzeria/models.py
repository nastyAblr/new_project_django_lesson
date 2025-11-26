from django.db import models
from django.utils.text import slugify
from transliterate import translit


class Pizza(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    image = models.ImageField(upload_to='pizzas/', blank=True, null=True, verbose_name='Фото')
    ingredients = models.TextField(verbose_name='Состав')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')

    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            latin_name = translit(self.name, 'ru', reversed=True)
            base_slug = slugify(latin_name)
            slug = base_slug
            counter = 1

            while Pizza.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return  self.name

    class Meta:
        verbose_name = 'Пицца'
        verbose_name_plural = 'Пиццы'


class Order(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.CharField(max_length=255, verbose_name='Адрес доставки')
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, verbose_name='Пицца')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    def __str__(self):
        return f"Заказ #{self.id} — {self.pizza.name}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
