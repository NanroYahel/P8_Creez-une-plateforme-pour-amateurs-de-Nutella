# Generated by Django 2.0.3 on 2018-04-18 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitute', '0005_auto_20180418_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='nutriments',
            field=models.CharField(max_length=3000),
        ),
    ]
