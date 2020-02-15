# Generated by Django 2.2.3 on 2020-01-31 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tip', '0002_auto_20200131_1619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='champion',
            name='out',
        ),
        migrations.AddField(
            model_name='champion',
            name='not_eliminated',
            field=models.BooleanField(default=1),
        ),
        migrations.AlterField(
            model_name='champion',
            name='champion',
            field=models.ForeignKey(max_length=100, on_delete=django.db.models.deletion.CASCADE, to='Tip.Team'),
        ),
    ]