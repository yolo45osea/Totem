# Generated by Django 5.0.7 on 2024-11-25 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reserva', '0007_remove_pasajero_fotoperfil_remove_pasajero_activo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('idAdmin', models.CharField(max_length=5, primary_key=True, serialize=False, verbose_name='Id Admin')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre del Admin')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
                ('password', models.CharField(max_length=128, verbose_name='Contraseña')),
            ],
        ),
        migrations.CreateModel(
            name='TipoAdmin',
            fields=[
                ('idTipo', models.CharField(max_length=5, primary_key=True, serialize=False, verbose_name='Id Tipo Admin')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre Tipo Admin')),
            ],
        ),
    ]