# Generated by Django 3.1.7 on 2021-03-21 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='holdMyData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lowSongId', models.TextField()),
                ('midSongId', models.TextField()),
                ('highSongId', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='preferredMusic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('danceabilityPreferred', models.FloatField(blank=True)),
                ('acousticnessPreferred', models.FloatField(blank=True)),
                ('tempoPreferred', models.FloatField(blank=True)),
            ],
        ),
    ]
