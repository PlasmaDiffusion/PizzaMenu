# Generated by Django 2.2.6 on 2019-10-27 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_placedorder_delivered'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Extra',
        ),
        migrations.RemoveField(
            model_name='order',
            name='extras',
        ),
        migrations.AddField(
            model_name='mainitem',
            name='canHaveToppings',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='menuoption',
            name='canHaveToppings',
            field=models.BooleanField(default=True),
        ),
    ]
