# Generated by Django 4.2.18 on 2025-02-14 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='avatar_url',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='头像'),
        ),
    ]
