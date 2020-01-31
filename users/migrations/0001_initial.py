# Generated by Django 2.2.3 on 2020-01-31 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('score', models.IntegerField(default=0)),
                ('rank', models.IntegerField(default=0)),
                ('user_champion', models.CharField(choices=[('ger', 'deutschland'), ('spa', 'spanien'), ('eng', 'England'), ('fra', 'Frankreich'), ['---', '---']], default='----', max_length=12)),
                ('joker', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
