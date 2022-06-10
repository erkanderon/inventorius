# Generated by Django 4.0.3 on 2022-06-09 20:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='NMAPTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=100)),
                ('took_time_in_minute', models.IntegerField(default=0)),
                ('flag', models.CharField(choices=[('0', 'Finished'), ('1', 'Running'), ('2', 'Failed'), ('3', 'Not Started')], default='3', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Subnet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subnet_ip', models.GenericIPAddressField()),
                ('mask', models.IntegerField(default=30, validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(8)])),
                ('cidr', models.CharField(default='None', editable=False, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Ip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=100)),
                ('dns', models.CharField(max_length=100, null=True)),
                ('port', models.CharField(max_length=500, null=True)),
                ('description', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='desc', to='common.description')),
                ('subnet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subnet.subnet')),
            ],
        ),
    ]
