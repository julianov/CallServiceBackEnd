# Generated by Django 3.2.9 on 2022-02-12 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callserviceapp', '0005_auto_20220130_1324'),
    ]

    operations = [
        migrations.CreateModel(
            name='nuevo_chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notify_to', models.EmailField(blank=True, max_length=254)),
                ('message_from', models.EmailField(blank=True, max_length=254)),
                ('ticket', models.IntegerField(blank=True, default=1000)),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='items',
            field=models.CharField(choices=[('CARPINTERÍA', 'CARPINTERÍA'), ('CERRAJERÍA', 'CERRAJERÍA'), ('CONSTRUCCIÓN', 'CONSTRUCCIÓN'), ('CONTADURÍA', 'CONTADURÍA'), ('ELECTRICIDAD', 'ELECTRICIDAD'), ('ELECTRÓNICA', 'ELECTRÓNICA'), ('ESTÉTICA', 'ESTÉTICA'), ('FLETE', 'FLETE'), ('FUMIGACIÓN', 'FUMIGACIÓN'), ('GASISTA', 'GASISTA'), ('HERRERÍA', 'HERRERÍA'), ('INFORMÁTICA', 'INFORMÁTICA'), ('JARDINERÍA', 'JARDINERÍA'), ('MECÁNICA', 'MECÁNICA'), ('MODA', 'MODA'), ('PASEADOR DE MASCOTAS', 'PASEADOR DE MASCOTAS'), ('PINTOR', 'PINTOR'), ('REFRIGERACIÓN', 'REFRIGERACIÓN'), ('REMOLQUES - GRÚAS', 'REMOLQUES'), ('PLOMERÍA', 'PLOMERÍA'), ('TELEFONÍA CELULAR', 'TELEFONÍA CELULAR'), ('TEXTIL', 'TEXTIL')], max_length=25),
        ),
        migrations.AlterField(
            model_name='item_company',
            name='items',
            field=models.CharField(choices=[('CARPINTERÍA', 'CARPINTERÍA'), ('CERRAJERÍA', 'CERRAJERÍA'), ('CONSTRUCCIÓN', 'CONSTRUCCIÓN'), ('CONTADURÍA', 'CONTADURÍA'), ('ELECTRICIDAD', 'ELECTRICIDAD'), ('ELECTRÓNICA', 'ELECTRÓNICA'), ('ESTÉTICA', 'ESTÉTICA'), ('FLETE', 'FLETE'), ('FUMIGACIÓN', 'FUMIGACIÓN'), ('GASISTA', 'GASISTA'), ('HERRERÍA', 'HERRERÍA'), ('INFORMÁTICA', 'INFORMÁTICA'), ('JARDINERÍA', 'JARDINERÍA'), ('MECÁNICA', 'MECÁNICA'), ('MODA', 'MODA'), ('PASEADOR DE MASCOTAS', 'PASEADOR DE MASCOTAS'), ('PINTOR', 'PINTOR'), ('REFRIGERACIÓN', 'REFRIGERACIÓN'), ('REMOLQUES - GRÚAS', 'REMOLQUES'), ('PLOMERÍA', 'PLOMERÍA'), ('TELEFONÍA CELULAR', 'TELEFONÍA CELULAR'), ('TEXTIL', 'TEXTIL')], max_length=25),
        ),
    ]