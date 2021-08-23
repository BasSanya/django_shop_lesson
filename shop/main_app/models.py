import sys
from io import BytesIO

from PIL import Image
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass


def get_product_url(obj, viewname, urlpattern_name, model_name):
    ct_model = obj.__class__meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend((model_products))
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products,
                                  key=lambda x: x.__class__._meta.model_name.startwith(with_respect_to),
                                  reverse=True)
        return products


class LatestProducts:
    objects = LatestProductsManager()


class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Ноутбуки': 'notebook__count',
        'Смартфони': 'smartphone__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_header_drop_list(self):
        model = get_models_for_count('notebook', 'smartphone')
        qs = list(self.get_queryset().annotate(*model))
        data = [
            dict(name=c.name, url=c.get_absolut_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Назва категорії')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolut_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (4000, 4000)
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 мб

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категорія', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Назва товару')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Зображення')
    description = models.TextField(verbose_name='Опис', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Ціна')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        min_height, min_width = self.MIN_RESOLUTION
        max_height, max_width = self.MAX_RESOLUTION
        if img.height < min_height or img.width < min_width:
            raise MinResolutionErrorException('Розрішення зображення менше мінімального')
        if img.height > max_height or img.width > max_width:
            raise MinResolutionErrorException('Розрішення зображення більше максимально допустимого')
        # new_img = img.convert('RGB')
        # resized = new_img.resize((800, 800), Image.ANTIALIAS)
        # filestream = BytesIO()
        # resized.save(filestream, 'PNG')
        # filestream.seek(0)
        # print(self.image.name.split('.'))
        # name = '{}.{}'.format(*self.image.name.split('.'))
        # self.image = InMemoryUploadedFile(filestream, 'ImageField', name, 'png/image',
        #                                   sys.getsizeof(filestream), None)
        super().save(*args, **kwargs)


class NoteBook(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Діагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплею')
    processor_freq = models.CharField(max_length=255, verbose_name='Частота процесора')
    ram = models.CharField(max_length=255, verbose_name='Оперативна пам\'ять')
    video = models.CharField(max_length=255, verbose_name='Відеокарта')
    time_without_charge = models.CharField(max_length=255, verbose_name='Час роботи від акамулятора')

    def __str__(self):
        return f'{self.category.name} {self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Smartphone(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Діагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплею')
    resolution = models.CharField(max_length=255, verbose_name='Розрішення екрану')
    accum_volume = models.CharField(max_length=255, verbose_name='Об\'єм акамулятора')
    ram = models.CharField(max_length=255, verbose_name='Оперативна пам\'ять')
    sd = models.BooleanField(default=True, verbose_name='Наявність SD карти пам\'яті')
    sd_volume_max = models.CharField(max_length=255,
                                     null=True,
                                     blank=True,
                                     verbose_name='Максимальний об\'єм карти пам\'яті')
    main_cam_mp = models.CharField(max_length=255, verbose_name='Основна камера')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Фронтальна камера')

    def __str__(self):
        return f'{self.category.name} : {self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупець', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Загальна сума')

    def __str__(self):
        return f'Продукт: {self.content_object.title} в корзині'


class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='Власник', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Загальна сума')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return self.id


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Користувач', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, verbose_name='Адрес')

    def __str__(self):
        return f'Покупець: {self.user.first_name} {self.user.last_name}'
