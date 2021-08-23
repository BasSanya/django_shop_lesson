# Generated by Django 3.2.6 on 2021-08-21 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20210821_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='Smartphone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Назва товару')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='', verbose_name='Зображення')),
                ('description', models.TextField(null=True, verbose_name='Опис')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Ціна')),
                ('diagonal', models.CharField(max_length=255, verbose_name='Діагональ')),
                ('display_type', models.CharField(max_length=255, verbose_name='Тип дисплею')),
                ('resolution', models.CharField(max_length=255, verbose_name='Розрішення екрану')),
                ('accum_volume', models.CharField(max_length=255, verbose_name="Об'єм акамулятора")),
                ('ram', models.CharField(max_length=255, verbose_name="Оперативна пам'ять")),
                ('sd', models.BooleanField(default=True)),
                ('sd_volume_max', models.CharField(max_length=255, verbose_name="Максимальний об'єм встроїної пам'яті")),
                ('main_cam_mp', models.CharField(max_length=255, verbose_name='Основна камера')),
                ('frontal_cam_mp', models.CharField(max_length=255, verbose_name='Фронтальна камера')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.category', verbose_name='Категорія')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NoteBookProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Назва товару')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='', verbose_name='Зображення')),
                ('description', models.TextField(null=True, verbose_name='Опис')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Ціна')),
                ('diagonal', models.CharField(max_length=255, verbose_name='Діагональ')),
                ('display_type', models.CharField(max_length=255, verbose_name='Тип дисплею')),
                ('processor_freq', models.CharField(max_length=255, verbose_name='Частота процесора')),
                ('ram', models.CharField(max_length=255, verbose_name="Оперативна пам'ять")),
                ('video', models.CharField(max_length=255, verbose_name='Відеокарта')),
                ('time_without_charge', models.CharField(max_length=255, verbose_name='Час роботи від акамулятора')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.category', verbose_name='Категорія')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]