# Generated by Django 5.0.7 on 2024-11-21 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reserva', '0003_tipo_alter_metodopago_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='metodopago',
            name='nombre',
            field=models.CharField(default='Tarjeta de Débito 1', max_length=50, verbose_name='Nombre Pago'),
            preserve_default=False,
        ),
    ]
