# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-18 05:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Medic_App', '0004_auto_20160405_0629'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('1', 'medic chat'), ('2', 'patients chat')], max_length=20)),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Medic_App.ChatRoom')),
                ('sent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='disease',
            name='commonness',
            field=models.CharField(choices=[('1', 'very uncommon'), ('2', 'uncommon'), ('3', 'common'), ('4', 'very common')], max_length=1),
        ),
    ]