# Generated by Django 2.0.3 on 2019-10-20 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20191020_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuoption',
            name='largeOnly',
            field=models.BooleanField(default=False),
        ),
    ]
