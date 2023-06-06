# Generated by Django 4.2.2 on 2023-06-06 11:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ministrant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('birthname', models.CharField(max_length=100)),
                ('surename', models.CharField(max_length=100)),
                ('birth_date', models.DateField()),
                ('address', models.CharField(max_length=100)),
                ('town', models.CharField(max_length=100)),
                ('town_zip', models.CharField(max_length=100)),
            ],
        ),
    ]
