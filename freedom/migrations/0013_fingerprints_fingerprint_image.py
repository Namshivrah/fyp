# Generated by Django 4.2.9 on 2024-02-12 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freedom', '0012_alter_candidates_post_aspired_for'),
    ]

    operations = [
        migrations.AddField(
            model_name='fingerprints',
            name='fingerprint_image',
            field=models.BinaryField(default=b''),
        ),
    ]