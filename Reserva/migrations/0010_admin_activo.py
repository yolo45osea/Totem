# Generated by Django 5.0.7 on 2024-11-25 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reserva', '0009_admin_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='activo',
            field=models.BooleanField(default=True, verbose_name='¿Está Activo?'),
        ),
    ]
