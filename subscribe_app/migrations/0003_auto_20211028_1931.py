# Generated by Django 3.2.8 on 2021-10-28 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_app', '0002_razorpay_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='cancel_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user_profile',
            name='subscribe_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]