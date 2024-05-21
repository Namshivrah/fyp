# Generated by Django 4.2.9 on 2024-02-10 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freedom', '0010_alter_voters_phone_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiotypes',
            name='audio_type',
            field=models.CharField(choices=[('English', 'English'), ('Luganda', 'Luganda'), ('Kiswahili', 'Kiswahili')], max_length=10),
        ),
        migrations.AlterField(
            model_name='fingerprints',
            name='finger',
            field=models.CharField(choices=[('Thumb', 'Thumb'), ('Index Finger', 'Index Finger'), ('Middle Finger', 'Middle Finger'), ('Ring Finger', 'Ring Finger'), ('Pinky Finger', 'Pinky Finger')], max_length=13),
        ),
        migrations.AlterField(
            model_name='fingerprints',
            name='hand',
            field=models.CharField(choices=[('Right_Hand', 'Right_Hand'), ('Left_Hand', 'Left_Hand')], max_length=10),
        ),
        migrations.AlterField(
            model_name='voters',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6),
        ),
        migrations.AlterField(
            model_name='voters',
            name='phone_contact',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='voters',
            name='voter_type',
            field=models.CharField(choices=[('Blind', 'Blind'), ('Blind_and_Mute', 'Blind_and_Mute'), ('Blind_and_Lame', 'Blind_and_Lame')], max_length=15),
        ),
    ]