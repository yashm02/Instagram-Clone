# Generated by Django 4.1.7 on 2023-02-18 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='users/profilepic.jpg', upload_to='users/%Y%m%d'),
        ),
    ]
