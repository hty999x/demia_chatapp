# Generated by Django 5.0.2 on 2024-02-28 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_remove_customuser_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='icon',
            field=models.FileField(default='', upload_to=''),
        ),
    ]
