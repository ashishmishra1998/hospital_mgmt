# Generated by Django 4.1.2 on 2022-11-25 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_user_data_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_data',
            name='card_serial',
            field=models.CharField(max_length=10, null=True),
        ),
    ]