# Generated by Django 4.0.3 on 2022-07-08 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_config'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='smtp_port',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='networkconndescription',
            name='code',
            field=models.IntegerField(max_length=100),
        ),
    ]