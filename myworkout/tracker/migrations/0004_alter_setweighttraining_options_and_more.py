# Generated by Django 4.2.1 on 2024-01-29 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_setweighttraining_is_work'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='setweighttraining',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='setweighttraining',
            name='is_work',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
