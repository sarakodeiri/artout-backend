# Generated by Django 2.2.2 on 2019-12-11 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_private',
            field=models.BooleanField(default=True),
        ),
    ]