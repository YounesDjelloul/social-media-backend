# Generated by Django 3.2.7 on 2021-09-15 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_friend'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='to_user',
            new_name='receiver',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='from_user',
            new_name='sender',
        ),
    ]
