# Generated by Django 2.2.1 on 2019-12-13 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('char_roster', '0003_auto_20191212_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='curr_hp',
            field=models.PositiveIntegerField(default=models.PositiveIntegerField(default=36)),
        ),
        migrations.AlterField(
            model_name='agent',
            name='max_hp',
            field=models.PositiveIntegerField(default=36),
        ),
    ]
