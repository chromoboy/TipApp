# Generated by Django 2.2.3 on 2020-01-07 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tip', '0009_remove_tip_tip'),
    ]

    operations = [
        migrations.AddField(
            model_name='tip',
            name='matchday',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='match',
            name='guest_score',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='match',
            name='guest_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guest_team', to='Tip.Team'),
        ),
        migrations.AlterField(
            model_name='match',
            name='home_score',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='match',
            name='home_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_team', to='Tip.Team'),
        ),
    ]
