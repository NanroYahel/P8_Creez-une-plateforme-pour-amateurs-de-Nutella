# Generated by Django 2.0.3 on 2018-04-12 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitute', '0002_auto_20180412_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(max_length=30),
        ),
    ]