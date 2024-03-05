# Generated by Django 4.2.1 on 2024-01-22 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='targetmuscle',
            options={'ordering': ['position'], 'verbose_name': 'Categories by target muscle group', 'verbose_name_plural': 'Categories by target muscle group'},
        ),
        migrations.RemoveField(
            model_name='targetmuscle',
            name='level',
        ),
        migrations.RemoveField(
            model_name='targetmuscle',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='targetmuscle',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='targetmuscle',
            name='tree_id',
        ),
        migrations.AlterField(
            model_name='targetmuscle',
            name='name',
            field=models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='targetmuscle',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='workout.targetmuscle', verbose_name='Родитель'),
        ),
        migrations.AlterField(
            model_name='targetmuscle',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, verbose_name='URL'),
        ),
    ]