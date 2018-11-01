# Generated by Django 2.1.2 on 2018-11-01 01:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flashcards', '0004_user_word'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Expression',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expression_number', models.IntegerField(verbose_name='Expression Number')),
                ('time', models.DateTimeField(verbose_name='Time')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]