# Generated by Django 3.2.4 on 2021-08-12 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_custom_user_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='custom_user',
            name='user_wallet_address',
            field=models.CharField(default='', max_length=200),
        ),
    ]
