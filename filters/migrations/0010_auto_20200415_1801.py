# Generated by Django 3.0.3 on 2020-04-15 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filters', '0009_auto_20200415_1758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='username',
            new_name='user_name',
        ),
    ]
