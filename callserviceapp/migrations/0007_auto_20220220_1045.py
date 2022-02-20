# Generated by Django 3.2.9 on 2022-02-20 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('callserviceapp', '0006_auto_20220212_1231'),
    ]

    operations = [
        migrations.CreateModel(
            name='listraProveedoresOrdenEmergencia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ticket', models.IntegerField(blank=True, default=1000)),
                ('proveedor_email', models.EmailField(blank=True, max_length=254)),
            ],
        ),
        migrations.RemoveField(
            model_name='ordenemergencia',
            name='lista_proveedores_empresa',
        ),
        migrations.RemoveField(
            model_name='ordenemergencia',
            name='lista_proveedores_independientes',
        ),
        migrations.AddField(
            model_name='item',
            name='hace_orden_emergencia',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='item_company',
            name='hace_orden_emergencia',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ordenemergencia',
            name='lista_proveedores',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='callserviceapp.listraproveedoresordenemergencia'),
        ),
    ]