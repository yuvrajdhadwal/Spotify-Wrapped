# Generated by Django 4.1 on 2024-12-01 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify_data', '0004_alter_duowrapped_datetime_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duowrapped',
            name='datetime_created',
            field=models.CharField(default='2024-11-30-18-05-14-482343', max_length=50),
        ),
        migrations.AlterField(
            model_name='spotifywrapped',
            name='datetime_created',
            field=models.CharField(default='2024-11-30-18-05-14-482343', max_length=50),
        ),
    ]
