# Generated by Django 5.0.7 on 2024-11-25 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reserva', '0011_admin_fecharegistro_chofer_fecharegistro'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='rut',
            field=models.CharField(default='21682301-k', max_length=10, verbose_name='Rut del Admin'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chofer',
            name='rut',
            field=models.CharField(default='21682301-k', max_length=10, verbose_name='Rut del Chofer'),
            preserve_default=False,
        ),
    ]