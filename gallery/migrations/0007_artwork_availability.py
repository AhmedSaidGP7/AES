# Generated by Django 5.0.4 on 2024-07-02 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0006_alter_artwork_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='artwork',
            name='availability',
            field=models.TextField(default='In Stock'),
        ),
    ]
