# Generated by Django 3.2.8 on 2021-10-28 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_app', '0003_auto_20211028_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='order_id',
            field=models.CharField(blank=True, max_length=364, null=True),
        ),
    ]