# Generated by Django 4.0.3 on 2022-06-06 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0005_alter_boost_type_achive'),
    ]

    operations = [
        migrations.AddField(
            model_name='boost',
            name='achiveGet',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='boost',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'casual'), (1, 'auto')], default=0),
        ),
    ]
