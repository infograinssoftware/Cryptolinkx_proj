# Generated by Django 3.2.4 on 2021-07-08 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210430_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='custom_user',
            name='is_otp_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='custom_user',
            name='is_qrcode_verified',
            field=models.BooleanField(default=False),
        ),
    ]
