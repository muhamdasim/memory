# Generated by Django 3.2.3 on 2021-07-02 04:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0002_auto_20210701_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='patients',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='patients',
            name='country',
            field=models.CharField(choices=[('us', 'USA'), ('vn', 'Viet Nam')], default=None, max_length=5),
        ),
    ]
