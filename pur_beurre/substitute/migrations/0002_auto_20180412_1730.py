# Generated by Django 2.0.3 on 2018-04-12 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitute', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(max_length=15),
        ),
    ]
