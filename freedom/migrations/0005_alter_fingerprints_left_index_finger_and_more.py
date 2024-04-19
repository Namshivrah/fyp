# Generated by Django 4.2.9 on 2024-02-01 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freedom', '0004_alter_candidate_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fingerprints',
            name='left_index_finger',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='fingerprints',
            name='left_middle_finger',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='fingerprints',
            name='left_pinky_finger',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='fingerprints',
            name='left_ring_finger',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='fingerprints',
            name='left_thumb',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='fingerprints',
            name='right_index_finger',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='fingerprints',
            name='right_middle_finger',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='fingerprints',
            name='right_pinky_finger',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='fingerprints',
            name='right_ring_finger',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='fingerprints',
            name='right_thumb',
            field=models.BinaryField(),
        ),
    ]
