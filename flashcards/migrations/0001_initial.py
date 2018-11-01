# Generated by Django 2.1.2 on 2018-10-26 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=256, verbose_name='Word')),
                ('pronunciation', models.CharField(max_length=256, verbose_name='Pronunciation')),
                ('equivalence', models.CharField(max_length=256, verbose_name='Equivalence')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images', verbose_name='Image')),
            ],
        ),
    ]
