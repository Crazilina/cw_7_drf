# Generated by Django 5.0.7 on 2024-07-13 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='is_pleasant',
            field=models.BooleanField(choices=[(True, 'Приятная'), (False, 'Нет')], default=False, help_text='Приятная привычка?', verbose_name='Приятная привычка'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='is_public',
            field=models.BooleanField(choices=[(True, 'Публичная'), (False, 'Нет')], default=False, help_text='Публичная привычка?', verbose_name='Публичная привычка'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='period',
            field=models.PositiveIntegerField(choices=[(1, 'Ежедневная'), (7, 'Еженедельная')], default=1, help_text='Введите периодичность.', verbose_name='Периодичность'),
        ),
    ]
