# Generated by Django 4.2.7 on 2023-12-26 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ASSSs', '0010_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.FileField(max_length=1000, null=True, upload_to='avatar'),
        ),
    ]
