# Generated by Django 3.2.4 on 2021-08-18 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_p2p_seller_user_cid_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='p2p_seller',
            name='sell_pair_name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
