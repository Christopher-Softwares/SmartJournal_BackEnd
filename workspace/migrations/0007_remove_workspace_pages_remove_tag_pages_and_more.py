# Generated by Django 5.0.6 on 2024-12-12 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0006_alter_page_folder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workspace',
            name='pages',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='pages',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='workspace',
        ),
        migrations.DeleteModel(
            name='Page',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
