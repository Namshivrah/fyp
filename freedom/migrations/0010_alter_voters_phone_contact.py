# Generated by Django 4.2.9 on 2024-02-10 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freedom', '0009_alter_address_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voters',
            name='phone_contact',
            field=models.CharField(max_length=10),
        ),
    ]