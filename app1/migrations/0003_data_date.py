# Generated by Django 4.0.2 on 2022-02-22 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_alter_data_age_alter_data_breathing_alter_data_cough_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
