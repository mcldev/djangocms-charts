# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_charts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chartjsbarmodel',
            name='chart_position',
            field=models.CharField(max_length=100, verbose_name='Chart Position', blank=True),
        ),
        migrations.AddField(
            model_name='chartjsdoughnutmodel',
            name='chart_position',
            field=models.CharField(max_length=100, verbose_name='Chart Position', blank=True),
        ),
        migrations.AddField(
            model_name='chartjslinemodel',
            name='chart_position',
            field=models.CharField(max_length=100, verbose_name='Chart Position', blank=True),
        ),
        migrations.AddField(
            model_name='chartjspiemodel',
            name='chart_position',
            field=models.CharField(max_length=100, verbose_name='Chart Position', blank=True),
        ),
        migrations.AddField(
            model_name='chartjspolarmodel',
            name='chart_position',
            field=models.CharField(max_length=100, verbose_name='Chart Position', blank=True),
        ),
        migrations.AddField(
            model_name='chartjsradarmodel',
            name='chart_position',
            field=models.CharField(max_length=100, verbose_name='Chart Position', blank=True),
        ),
        migrations.AlterField(
            model_name='chartjsbarmodel',
            name='legend_position',
            field=models.CharField(max_length=100, verbose_name='Legend Position', blank=True),
        ),
        migrations.AlterField(
            model_name='chartjsdoughnutmodel',
            name='legend_position',
            field=models.CharField(max_length=100, verbose_name='Legend Position', blank=True),
        ),
        migrations.AlterField(
            model_name='chartjslinemodel',
            name='legend_position',
            field=models.CharField(max_length=100, verbose_name='Legend Position', blank=True),
        ),
        migrations.AlterField(
            model_name='chartjspiemodel',
            name='legend_position',
            field=models.CharField(max_length=100, verbose_name='Legend Position', blank=True),
        ),
        migrations.AlterField(
            model_name='chartjspolarmodel',
            name='legend_position',
            field=models.CharField(max_length=100, verbose_name='Legend Position', blank=True),
        ),
        migrations.AlterField(
            model_name='chartjsradarmodel',
            name='legend_position',
            field=models.CharField(max_length=100, verbose_name='Legend Position', blank=True),
        ),
    ]
