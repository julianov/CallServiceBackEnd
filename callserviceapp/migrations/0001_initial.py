# Generated by Django 3.2.9 on 2021-12-26 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='chat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('mensaje', models.TextField(blank=True)),
                ('cliente', models.EmailField(blank=True, max_length=254)),
                ('proveedor', models.EmailField(blank=True, max_length=254)),
                ('day', models.DateField()),
                ('time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='client',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('random_number', models.IntegerField(default=0)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200)),
                ('picture', models.ImageField(blank=True, upload_to='media/')),
                ('qualification', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='company',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=200)),
                ('email', models.EmailField(default=None, max_length=254)),
                ('random_number', models.IntegerField(default=0)),
                ('company_name', models.CharField(blank=True, max_length=200)),
                ('company_description', models.CharField(blank=True, max_length=200)),
                ('picture', models.ImageField(default=None, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('items', models.CharField(choices=[('CARPINTERÍA', 'CARPINTERÍA'), ('CERRAJERÍA', 'CERRAJERÍA'), ('CONSTRUCCIÓN', 'CONSTRUCCIÓN'), ('ELECTRICIDAD', 'ELECTRICIDAD'), ('ELECTRÓNICA', 'ELECTRÓNICA'), ('FLETE', 'FLETE'), ('GASISTA', 'GASISTA'), ('HERRERÍA', 'HERRERÍA'), ('INFORMÁTICA', 'INFORMÁTICA'), ('JARDINERÍA', 'JARDINERÍA'), ('MECÁNICA', 'MECÁNICA'), ('PLOMERÍA', 'PLOMERÍA'), ('REFRIGERACIÓN', 'REFRIGERACIÓN'), ('REMOLQUES - GRÚAS', 'REMOLQUES'), ('TELEFONÍA CELULAR', 'TELEFONÍA CELULAR'), ('TEXTIL', 'TEXTIL')], max_length=25)),
                ('certificate', models.ImageField(default=None, upload_to='')),
                ('radius', models.FloatField(default=None)),
                ('qualification', models.IntegerField(default=0)),
                ('publicidad', models.IntegerField(default=0)),
                ('pais', models.TextField(blank=True)),
                ('provincia', models.TextField(blank=True)),
                ('ciudad', models.TextField(blank=True)),
                ('domicilio_calle', models.TextField(blank=True)),
                ('domicilio_numeracion', models.TextField(blank=True)),
                ('posicion_lat', models.FloatField(default=None)),
                ('posicion_long', models.FloatField(default=None)),
                ('description', models.TextField(blank=True)),
                ('days_of_works', models.CharField(choices=[('LUNES A VIERNES', 'LUNES A VIERNES'), ('LUNES A LUNES', 'LUNES A LUNES')], default='LV', max_length=25)),
                ('hour_init', models.TimeField()),
                ('hour_end', models.TimeField()),
                ('picture1', models.ImageField(blank=True, default=None, upload_to='')),
                ('picture2', models.ImageField(blank=True, default=None, upload_to='')),
                ('picture3', models.ImageField(blank=True, default=None, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='item_company',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('items', models.CharField(choices=[('CARPINTERÍA', 'CARPINTERÍA'), ('CERRAJERÍA', 'CERRAJERÍA'), ('CONSTRUCCIÓN', 'CONSTRUCCIÓN'), ('ELECTRICIDAD', 'ELECTRICIDAD'), ('ELECTRÓNICA', 'ELECTRÓNICA'), ('FLETE', 'FLETE'), ('GASISTA', 'GASISTA'), ('HERRERÍA', 'HERRERÍA'), ('INFORMÁTICA', 'INFORMÁTICA'), ('JARDINERÍA', 'JARDINERÍA'), ('MECÁNICA', 'MECÁNICA'), ('REFRIGERACIÓN', 'REFRIGERACIÓN'), ('REMOLQUES - GRÚAS', 'REMOLQUES'), ('PLOMERÍA', 'PLOMERÍA'), ('TELEFONÍA CELULAR', 'TELEFONÍA CELULAR'), ('TEXTIL', 'TEXTIL')], max_length=25)),
                ('certificate', models.ImageField(upload_to='media/')),
                ('description', models.TextField(blank=True)),
                ('radius', models.FloatField(default=None)),
                ('qualification', models.IntegerField(default=0)),
                ('publicidad', models.IntegerField(default=0)),
                ('pais', models.TextField(blank=True)),
                ('provincia', models.TextField(blank=True)),
                ('ciudad', models.TextField(blank=True)),
                ('domicilio_calle', models.TextField(blank=True)),
                ('domicilio_numeracion', models.TextField(blank=True)),
                ('posicion_lat', models.FloatField(default=None)),
                ('posicion_long', models.FloatField(default=None)),
                ('days_of_works', models.CharField(choices=[('LV', 'LUNES A VIERNES'), ('LL', 'LUNES A LUNES')], default='LV', max_length=25)),
                ('hour_init', models.TimeField()),
                ('hour_end', models.TimeField()),
                ('picture1', models.ImageField(blank=True, default=None, upload_to='')),
                ('picture2', models.ImageField(blank=True, default=None, upload_to='')),
                ('picture3', models.ImageField(blank=True, default=None, upload_to='')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='callserviceapp.company')),
            ],
        ),
        migrations.CreateModel(
            name='serviceProvider',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=200)),
                ('email', models.EmailField(default=None, max_length=254)),
                ('random_number', models.IntegerField(default=0)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200)),
                ('picture', models.ImageField(blank=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='ordenGeneral',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('client_email', models.EmailField(blank=True, max_length=254)),
                ('proveedor_email', models.EmailField(blank=True, max_length=254)),
                ('tiempo_respuesta_promedio', models.FloatField(default=1000)),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('ticket', models.IntegerField(blank=True, default=1000)),
                ('status', models.CharField(choices=[('ENV', 'ENVIADA'), ('REC', 'RECIBIDA'), ('ABI', 'ABIERTA'), ('PRE', 'PRESUPUESTADA'), ('ACE', 'ACEPTADA'), ('EVI', 'EN VIAJE'), ('ENS', 'EN SITIO'), ('RED', 'REALIZADA'), ('CAN', 'CANCELADA'), ('REX', 'RECHAZADA')], default='SO', max_length=3)),
                ('location_lat', models.FloatField(blank=True, default=None)),
                ('location_long', models.FloatField(blank=True, default=None)),
                ('day', models.TextField(default='Lunes Martes Miercoles Jueves Viernes')),
                ('time', models.TimeField(blank=True, default=None)),
                ('tituloPedido', models.TextField(default='Solicitud de pedido')),
                ('problem_description', models.TextField(blank=True, default=None)),
                ('picture1', models.ImageField(blank=True, default=None, upload_to='')),
                ('picture2', models.ImageField(blank=True, default=None, upload_to='')),
                ('presupuesto_inicial', models.FloatField(default=0)),
                ('pedido_mas_información', models.TextField(default=0)),
                ('respuesta_cliente_pedido_mas_información', models.TextField(default=0)),
                ('picture1_mas_información', models.ImageField(blank=True, default=None, upload_to='')),
                ('picture2_mas_información', models.ImageField(blank=True, default=None, upload_to='')),
                ('motivo_rechazo', models.TextField(blank=True, default=None)),
                ('resena', models.TextField(blank=True, default=None)),
                ('rubro', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='callserviceapp.item')),
            ],
        ),
        migrations.CreateModel(
            name='ordenEmergencia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('ENV', 'ENVIADA'), ('REC', 'RECIBIDA'), ('ACE', 'ACEPTADA'), ('EVI', 'EN VIAJE'), ('ENS', 'EN SITIO'), ('RED', 'REALIZADA'), ('CAN', 'CANCELADA'), ('REX', 'RECHAZADA')], default='SO', max_length=3)),
                ('client_email', models.EmailField(blank=True, max_length=254)),
                ('proveedor_email', models.EmailField(blank=True, max_length=254)),
                ('tiempo_respuesta_promedio', models.FloatField(default=1000)),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('ticket', models.IntegerField(blank=True, default=1000)),
                ('location_lat', models.FloatField(blank=True, default=None)),
                ('location_long', models.FloatField(blank=True, default=None)),
                ('tituloPedido', models.TextField(default='Solicitud de pedido')),
                ('problem_description', models.TextField(blank=True)),
                ('picture1', models.ImageField(blank=True, default=None, upload_to='')),
                ('picture2', models.ImageField(blank=True, default=None, upload_to='')),
                ('lista_proveedores_empresa', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='callserviceapp.item_company')),
                ('lista_proveedores_independientes', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='callserviceapp.item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='provider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='callserviceapp.serviceprovider'),
        ),
        migrations.CreateModel(
            name='campañaPublicidad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('EM', 'EMAIL'), ('HO', 'HOME')], default='HO', max_length=2)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='callserviceapp.company')),
                ('serviceProvider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='callserviceapp.serviceprovider')),
            ],
        ),
    ]
