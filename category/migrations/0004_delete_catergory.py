# Generated by Django 3.1.7 on 2021-07-07 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20210707_1512'),
        ('category', '0003_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Catergory',
        ),
    ]
