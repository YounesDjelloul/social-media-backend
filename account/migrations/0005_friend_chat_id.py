# Generated by Django 3.2.7 on 2021-09-15 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_friendrequest_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='chat_id',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
