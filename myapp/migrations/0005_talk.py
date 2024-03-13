# Generated by Django 5.0.2 on 2024-03-05 20:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_customuser_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('talk', models.CharField(max_length=500)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('talk_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='talk_from', to=settings.AUTH_USER_MODEL)),
                ('talk_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='talk_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
