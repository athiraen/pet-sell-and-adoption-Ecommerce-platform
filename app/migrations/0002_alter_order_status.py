# Generated by Django 5.1.2 on 2025-01-12 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default='conform', max_length=50),
        ),
    ]
