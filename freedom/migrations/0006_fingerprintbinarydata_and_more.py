# Generated by Django 4.2.9 on 2024-02-01 13:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freedom', '0005_alter_fingerprints_left_index_finger_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FingerprintBinaryData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('binary_data', models.BinaryField()),
            ],
        ),
        migrations.RemoveField(
            model_name='fingerprints',
            name='left_index_finger',
        ),
        migrations.RemoveField(
            model_name='fingerprints',
            name='left_middle_finger',
        ),
        migrations.RemoveField(
            model_name='fingerprints',
            name='left_pinky_finger',
        ),
        migrations.RemoveField(
            model_name='fingerprints',
            name='left_ring_finger',
        ),
        migrations.RemoveField(
            model_name='fingerprints',
            name='left_thumb',
        ),
        migrations.RemoveField(
            model_name='fingerprints',
            name='right_index_finger',
        ),
        migrations.RemoveField(
            model_name='fingerprints',
            name='right_middle_finger',
        ),
        migrations.RemoveField(
            model_name='fingerprints',
            name='right_pinky_finger',
        ),
        migrations.RemoveField(
            model_name='fingerprints',
            name='right_ring_finger',
        ),
        migrations.RemoveField(
            model_name='fingerprints',
            name='right_thumb',
        ),
        migrations.AddField(
            model_name='fingerprints',
            name='finger_positions',
            field=models.JSONField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fingerprints',
            name='fingerprint_binary_data',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='freedom.fingerprintbinarydata'),
            preserve_default=False,
        ),
    ]
