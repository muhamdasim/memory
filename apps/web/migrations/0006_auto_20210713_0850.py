# Generated by Django 3.2.3 on 2021-07-13 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20210712_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patients',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patients',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
