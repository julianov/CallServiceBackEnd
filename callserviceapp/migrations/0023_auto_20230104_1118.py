# Generated by Django 3.2.16 on 2023-01-04 11:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('callserviceapp', '0022_auto_20230104_0028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='user_id',
        ),
        migrations.AlterField(
            model_name='ordengeneral',
            name='rubro',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='callserviceapp.item'),
        ),
        migrations.AlterField(
            model_name='user_data',
            name='user_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
