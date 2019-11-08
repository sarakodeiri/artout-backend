# Generated by Django 2.2.2 on 2019-11-08 18:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0002_auto_20191107_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkin',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='check_in_time',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='event.Event'),
        ),
    ]