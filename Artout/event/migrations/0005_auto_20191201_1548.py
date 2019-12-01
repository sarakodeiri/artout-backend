# Generated by Django 2.2.2 on 2019-12-01 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_auto_20191108_2200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='location',
        ),
        migrations.RemoveField(
            model_name='location',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='location',
            name='longitude',
        ),
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='check_in_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='go_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
