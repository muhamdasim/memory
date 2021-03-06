# Generated by Django 3.2.3 on 2021-07-01 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patients',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='patients',
            name='country',
            field=models.CharField(choices=[('us', 'USA'), ('vn', 'Viet Nam')], max_length=5),
        ),
        migrations.AlterField(
            model_name='patients',
            name='email',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='patients',
            name='first_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='patients',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10),
        ),
        migrations.AlterField(
            model_name='patients',
            name='last_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='patients',
            name='phone',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='patients',
            name='state',
            field=models.CharField(max_length=30),
        ),
    ]
