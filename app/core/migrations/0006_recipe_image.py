# Generated by Django 2.2.7 on 2019-11-25 17:24

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_auto_20191125_1004"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="image",
            field=models.ImageField(
                null=True, upload_to=core.models.recipe_image_file_path
            ),
        ),
    ]
