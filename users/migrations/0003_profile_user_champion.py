# Generated by Django 2.2.3 on 2020-02-13 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_profile_user_champion'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_champion',
            field=models.CharField(choices=[('ger', 'deutschland'), ('spa', 'spanien'), ('eng', 'England'), ('fra', 'Frankreich'), ('ITA', 'Italien'), ['---', '---']], default='----', max_length=12),
        ),
    ]