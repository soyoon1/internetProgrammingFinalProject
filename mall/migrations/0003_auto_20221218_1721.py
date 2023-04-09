# Generated by Django 3.2 on 2022-12-18 17:21

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0002_manufacturer_description_manufacturer_logo_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='hook_text',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=markdownx.models.MarkdownxField(),
        ),
    ]