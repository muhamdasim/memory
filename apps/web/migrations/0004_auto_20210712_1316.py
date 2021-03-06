# Generated by Django 3.2.3 on 2021-07-12 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20210702_0439'),
    ]

    operations = [
        migrations.CreateModel(
            name='Therapist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('password', models.TextField()),
                ('language', models.CharField(choices=[('en', 'English'), ('vn', 'Vietnamese')], default='en', max_length=5)),
                ('ts', models.DateTimeField(auto_now_add=True)),
                ('is_subscribed_newsletters', models.BooleanField(default=False)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='patients',
            name='age',
        ),
        migrations.RemoveField(
            model_name='patients',
            name='country',
        ),
        migrations.RemoveField(
            model_name='patients',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='patients',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='patients',
            name='state',
        ),
        migrations.RemoveField(
            model_name='patients',
            name='user',
        ),
    ]
