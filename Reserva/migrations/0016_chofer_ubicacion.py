# Generated by Django 5.0.7 on 2024-12-03 01:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reserva', '0015_alter_sector_nombresector'),
    ]

    operations = [
        migrations.AddField(
            model_name='chofer',
            name='ubicacion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Sector', to='Reserva.sector'),
            preserve_default=False,
        ),
    ]