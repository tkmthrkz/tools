# Generated by Django 3.0.3 on 2020-04-15 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filters', '0007_auto_20200409_2232'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20)),
                ('password1', models.CharField(max_length=20)),
                ('password2', models.CharField(max_length=20)),
            ],
        ),
    ]
