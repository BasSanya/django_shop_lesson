# Generated by Django 3.2.6 on 2021-08-22 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20210822_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smartphone',
            name='sd',
            field=models.BooleanField(default=True, verbose_name="Наявність SD карти пам'яті"),
        ),
        migrations.AlterField(
            model_name='smartphone',
            name='sd_volume_max',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name="Максимальний об'єм встроїної пам'яті"),
        ),
    ]
