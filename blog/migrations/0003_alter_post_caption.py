# Generated by Django 3.2.7 on 2021-09-10 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='caption',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
