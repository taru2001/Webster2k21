# Generated by Django 3.1 on 2021-10-18 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0002_alter_coin_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
