# Generated by Django 3.2.3 on 2021-07-02 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_is_subscribed_newsletters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=255),
        ),
    ]
