# Generated by Django 5.1 on 2024-10-30 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='image',
            field=models.ImageField(default='images.jpg', upload_to='equipement_images'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='image',
            field=models.ImageField(default='image.jpg', upload_to='rooms_images'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='service_images'),
        ),
    ]