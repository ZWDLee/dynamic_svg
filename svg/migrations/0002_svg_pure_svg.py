# Generated by Django 3.2.13 on 2022-05-23 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svg', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='svg',
            name='pure_svg',
            field=models.BooleanField(default=True),
        ),
    ]
