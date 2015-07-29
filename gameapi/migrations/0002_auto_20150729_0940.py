# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('gameapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('is_approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('definition', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Predict',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('goals1', models.IntegerField(default=0)),
                ('goals2', models.IntegerField(default=0)),
                ('match', models.ForeignKey(related_name='matchpredicts', to='gameapi.Match')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('rank', models.IntegerField(default=0)),
                ('league', models.ForeignKey(related_name='teams', to='gameapi.League')),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 7, 29, 9, 40, 12, 228051, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='rank',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 7, 29, 9, 40, 25, 968750, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='predict',
            name='user',
            field=models.ForeignKey(related_name='userpredicts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='match',
            name='Team1',
            field=models.ForeignKey(related_name='matchs_team1', to='gameapi.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='Team2',
            field=models.ForeignKey(related_name='matchs_team2', to='gameapi.Team'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
