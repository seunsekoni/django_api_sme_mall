# Generated by Django 3.1.6 on 2021-03-16 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20210316_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
