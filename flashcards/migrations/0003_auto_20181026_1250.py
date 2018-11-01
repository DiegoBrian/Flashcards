# Generated by Django 2.1.2 on 2018-10-26 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0002_word_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='part_of_speech',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Part of speech'),
        ),
        migrations.AlterField(
            model_name='word',
            name='number',
            field=models.CharField(max_length=10, verbose_name='Number'),
        ),
    ]
