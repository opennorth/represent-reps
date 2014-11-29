# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='extra',
            field=jsonfield.fields.JSONField(blank=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='offices',
            field=jsonfield.fields.JSONField(blank=True),
        ),
        migrations.AlterField(
            model_name='representative',
            name='extra',
            field=jsonfield.fields.JSONField(blank=True),
        ),
        migrations.AlterField(
            model_name='representative',
            name='offices',
            field=jsonfield.fields.JSONField(blank=True),
        ),
    ]
