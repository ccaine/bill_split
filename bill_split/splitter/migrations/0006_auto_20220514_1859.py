# Generated by Django 3.2 on 2022-05-14 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('splitter', '0005_billgroup_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bill',
            old_name='bill_sections',
            new_name='bill_lines',
        ),
        migrations.RemoveField(
            model_name='billgroup',
            name='parent',
        ),
    ]
