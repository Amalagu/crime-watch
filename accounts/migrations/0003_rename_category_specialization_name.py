# Generated by Django 4.0.8 on 2024-02-09 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_specialization_investigator_specializations'),
    ]

    operations = [
        migrations.RenameField(
            model_name='specialization',
            old_name='category',
            new_name='name',
        ),
    ]
