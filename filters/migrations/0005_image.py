# Generated by Django 3.0.3 on 2020-04-06 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filters', '0004_delete_option'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_src', models.ImageField(upload_to='')),
                ('img_opt', models.ImageField(upload_to='')),
            ],
        ),
    ]
