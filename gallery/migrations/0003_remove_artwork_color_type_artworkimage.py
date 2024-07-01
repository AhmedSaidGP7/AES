# Generated by Django 5.0.4 on 2024-07-01 04:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_artwork_color_type_artwork_material_artwork_style_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artwork',
            name='color_type',
        ),
        migrations.CreateModel(
            name='ArtworkImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='artwork_images/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('artwork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='gallery.artwork')),
            ],
        ),
    ]
