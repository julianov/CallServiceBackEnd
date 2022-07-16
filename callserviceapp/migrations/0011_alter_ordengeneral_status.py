# Generated by Django 3.2.13 on 2022-06-19 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callserviceapp', '0010_auto_20220605_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordengeneral',
            name='status',
            field=models.CharField(choices=[('ENV', 'ENVIADA'), ('REC', 'RECIBIDA'), ('PEI', 'PEDIDO INFORMACION'), ('RES', 'RESPUESTA DEL CLIENTE'), ('PRE', 'PRESUPUESTADA'), ('ACE', 'ACEPTADA'), ('EVI', 'EN VIAJE'), ('ENS', 'EN SITIO'), ('RED', 'REALIZADA'), ('CAN', 'CANCELADA'), ('REX', 'RECHAZADA')], default='SO', max_length=3),
        ),
    ]
