# Generated by Django 2.2.3 on 2020-01-02 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tip', '0004_auto_20191005_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='team_rank',
        ),
        migrations.AddField(
            model_name='team',
            name='win_points',
            field=models.IntegerField(default=10),
        ),
    ]
