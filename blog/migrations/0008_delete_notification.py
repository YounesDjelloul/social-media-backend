# Generated by Django 3.2.7 on 2021-09-17 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_rename_channel_name_notificationlistener_notification_group_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
