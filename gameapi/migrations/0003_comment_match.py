# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameapi', '0002_auto_20150729_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='match',
            field=models.ForeignKey(to='gameapi.Match', default=1, related_name='matchcomments'),
            preserve_default=False,
        ),
    ]
