# Generated by Django 5.0 on 2024-06-12 18:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0005_delete_phoneotp_user_is_staff_user_is_superuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pret',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('taux_interet', models.FloatField(default=0.0)),
                ('encours', models.FloatField(default=0.0)),
                ('solde_payer', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='phone')),
            ],
        ),
    ]
