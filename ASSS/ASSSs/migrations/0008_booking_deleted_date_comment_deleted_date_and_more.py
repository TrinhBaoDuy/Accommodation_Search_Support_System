# Generated by Django 4.2.7 on 2023-12-26 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ASSSs', '0007_alter_booking_options_alter_comment_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='deleted_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='deleted_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='discount',
            name='deleted_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='follow',
            name='deleted_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='house',
            name='deleted_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='image',
            name='deleted_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='deleted_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='deleted_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
