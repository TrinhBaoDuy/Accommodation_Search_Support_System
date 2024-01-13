# Generated by Django 5.0 on 2024-01-09 09:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ASSSs', '0018_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_query_name='likes', to='ASSSs.post'),
        ),
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_query_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
