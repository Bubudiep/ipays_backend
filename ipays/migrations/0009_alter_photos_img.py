# Generated by Django 5.0.3 on 2024-03-24 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipays', '0008_photos_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photos',
            name='img',
            field=models.BinaryField(default=1),
            preserve_default=False,
        ),
    ]
