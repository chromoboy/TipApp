# Generated by Django 2.2.3 on 2020-01-04 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tip', '0007_auto_20200104_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='tip',
            name='tip_guest',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='tip',
            name='tip_home',
            field=models.IntegerField(default=-1),
        ),
    ]
