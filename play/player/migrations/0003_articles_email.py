# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0002_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='email',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
