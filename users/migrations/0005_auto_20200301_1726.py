# Generated by Django 2.0.4 on 2020-03-01 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200301_0816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_champion',
            field=models.CharField(choices=[('----', '----')], default='----', max_length=12),
        ),
    ]
