# Generated by Django 3.1.2 on 2021-12-19 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_transactionhistory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transactionhistory',
            options={'ordering': ['-time']},
        ),
    ]
