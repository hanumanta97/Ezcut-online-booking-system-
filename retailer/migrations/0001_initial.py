# Generated by Django 4.2.12 on 2024-05-15 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='buisness',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('eamil_id', models.TextField()),
                ('buisness_name', models.TextField()),
                ('user_name', models.EmailField(max_length=254)),
                ('phone', models.TextField()),
                ('city', models.TextField()),
                ('services', models.ImageField(upload_to='')),
                ('services_price', models.TextField()),
                ('shop_address', models.TextField()),
                ('password_user', models.TextField()),
                ('user_id', models.TextField()),
            ],
            options={
                'db_table': 'buisness',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('shop_id', models.TextField()),
                ('username', models.EmailField(max_length=254)),
                ('usermessage', models.TextField()),
                ('rating', models.FloatField()),
            ],
            options={
                'db_table': 'review',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='schedule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('shop_id', models.TextField()),
                ('user_id', models.TextField()),
                ('services', models.EmailField(max_length=254)),
                ('total_price', models.TextField()),
                ('time', models.TimeField()),
                ('date', models.DateField()),
                ('status', models.TextField()),
                ('appointment_record', models.DateTimeField(auto_now=True)),
                ('remarks', models.TextField()),
            ],
            options={
                'db_table': 'schedule_appointment',
                'managed': False,
            },
        ),
    ]
