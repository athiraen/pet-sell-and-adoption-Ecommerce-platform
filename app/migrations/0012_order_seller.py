# Generated by Django 5.1.2 on 2025-01-15 02:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_seller_list_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.seller_list'),
        ),
    ]
