from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class LatestProductManager:
    object = None

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        products = []
        ct_models = ContentType.objects.filter(model_in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        return products


class LatestProduct:
    object = LatestProductManager()


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=9, decimal_places=2)

    class Meta:
        abstract = True
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.title


class Notebook(Product):
    diagonal = models.CharField(max_length=50, verbose_name='Диагональ')
    display_type = models.CharField(max_length=50, verbose_name='Тип дисплея')
    freq = models.CharField(max_length=50, verbose_name='Частота процессора')
    ram = models.CharField(max_length=50, verbose_name='Оперативная память')
    video = models.CharField(max_length=50, verbose_name='Видеокарта')
    time_without_charge = models.CharField(max_length=50, verbose_name='Время работы аккумулятора')

    class Meta:
        verbose_name = "Ноутбук"
        verbose_name_plural = "Ноутбуки"

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


class Smartphone(Product):
    diagonal = models.CharField(max_length=50, verbose_name='Диагональ')
    display_type = models.CharField(max_length=50, verbose_name='Тип дисплея')
    resolution = models.CharField(max_length=50, verbose_name='Разрешение экрана')
    accum_volume = models.CharField(max_length=50, verbose_name='Объем батареи')
    ram = models.CharField(max_length=50, verbose_name='Оперативная память')
    sd = models.BooleanField(default=True)
    sd_volume_max = models.CharField(max_length=50, verbose_name='Максимальный объем встраеваемой памяти')
    main_cam_mp = models.CharField(max_length=50, verbose_name='Главная камера')
    frontal_cam_mp = models.CharField(max_length=50, verbose_name='Фронтальная камера')

    class Meta:
        verbose_name = "Смартфон"
        verbose_name_plural = "Смартфоны"

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    # product: Product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.IntegerField(default=1)
    final_price = models.DecimalField(verbose_name='Общая цена', max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Корзина продукта"
        verbose_name_plural = "Корзины продуктов"

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.product.title)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(verbose_name='Общая цена', max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user: User = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    # first_name = models.CharField(max_length=50, verbose_name='Имя пользователя')
    phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    address = models.CharField(max_length=50, verbose_name='Адрес')

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)

# class Specifications(models.Model):
#     name = models.CharField(max_length=50, verbose_name='Имя товара для характеристик')
#     content_type = models.ForeignKey(ContentType, verbose_name='', on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#
#     class Meta:
#         verbose_name = "Specifications"
#         verbose_name_plural = "Specificationss"
#
#     def __str__(self):
#         return "Характеристики для товара {}".format(self.name)
