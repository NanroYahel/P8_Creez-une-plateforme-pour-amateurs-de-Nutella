# Generated by Django 2.0.3 on 2018-04-18 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitute', '0006_auto_20180418_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='nutriments',
            field=models.CharField(max_length=1500),
        ),
    ]
