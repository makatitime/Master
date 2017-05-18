# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='articles',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('author', models.CharField(max_length=32)),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=256)),
            ],
        ),
    ]
