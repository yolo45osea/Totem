# Generated by Django 5.0.7 on 2024-12-03 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reserva', '0016_chofer_ubicacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='emailAcompanante1',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Correo Electrónico del Acompañante 1'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='emailAcompanante2',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Correo Electrónico del Acompañante 2'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='emailAcompanante3',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Correo Electrónico del Acompañante 3'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='nombreAcompanante1',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre del Acompañante 1'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='nombreAcompanante2',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre del Acompañante 2'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='nombreAcompanante3',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre del Acompañante 3'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='rutAcompanante1',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Rut del Acompañante 1'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='rutAcompanante2',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Rut del Acompañante 2'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='rutAcompanante3',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Rut del Acompañante 3'),
        ),
    ]