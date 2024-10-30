# Generated by Django 5.1 on 2024-10-30 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_equipment_image_alter_room_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='price',
            field=models.PositiveIntegerField(default=20000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='price',
            field=models.PositiveIntegerField(default=50000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='price',
            field=models.PositiveIntegerField(default=100000),
            preserve_default=False,
        ),
    ]
