# Generated by Django 5.0.6 on 2024-12-08 01:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0005_folder_page_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='folder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pages', to='workspace.folder'),
        ),
    ]
