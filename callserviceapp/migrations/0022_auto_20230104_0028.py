# Generated by Django 3.2.16 on 2023-01-04 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callserviceapp', '0021_auto_20230103_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_data',
            name='posicion_lat',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='user_data',
            name='posicion_long',
            field=models.FloatField(default=None, null=True),
        ),
    ]