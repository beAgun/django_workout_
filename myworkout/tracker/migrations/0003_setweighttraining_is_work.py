# Generated by Django 4.2.1 on 2024-01-29 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='setweighttraining',
            name='is_work',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
