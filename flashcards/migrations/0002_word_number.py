# Generated by Django 2.1.2 on 2018-10-26 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='number',
            field=models.IntegerField(default=1, verbose_name='Number'),
        ),
    ]