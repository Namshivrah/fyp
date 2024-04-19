# Generated by Django 4.2.9 on 2024-02-05 08:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freedom', '0006_fingerprintbinarydata_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fingerprintbinarydata',
            name='voter',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='freedom.voter'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='candidate',
            name='image',
            field=models.ImageField(upload_to='candidate_images'),
        ),
        migrations.DeleteModel(
            name='Fingerprints',
        ),
    ]
