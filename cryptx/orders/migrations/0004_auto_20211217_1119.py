# Generated by Django 3.1 on 2021-12-17 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20211216_1733'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-time']},
        ),
    ]