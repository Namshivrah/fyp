# Generated by Django 4.2.9 on 2024-05-22 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freedom', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidates',
            name='profile_pic',
            field=models.ImageField(upload_to=''),
        ),
    ]