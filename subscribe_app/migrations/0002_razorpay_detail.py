# Generated by Django 3.2.8 on 2021-10-28 19:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Razorpay_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=264, unique=True)),
                ('success_status', models.BooleanField(default=False)),
                ('amount', models.CharField(blank=True, max_length=265, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]