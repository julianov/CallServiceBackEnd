# Generated by Django 3.2.9 on 2022-01-30 15:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('callserviceapp', '0003_auto_20220128_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='daystamp',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chat',
            name='timestamp',
            field=models.TimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chat',
            name='day',
            field=models.DateField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='chat',
            name='time',
            field=models.TimeField(blank=True, default=None),
        ),
    ]