# Generated by Django 3.0.3 on 2020-04-24 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filters', '0013_auto_20200424_2111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='user',
            new_name='username',
        ),
    ]
