# Generated by Django 2.0.6 on 2018-06-17 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='used',
            field=models.BooleanField(default=False),
        ),
    ]
