# Generated by Django 4.2.7 on 2023-11-06 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crossword', '0003_crosswords_posting_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crosswords',
            old_name='crator_id',
            new_name='craetor_id',
        ),
        migrations.RenameField(
            model_name='crosswords',
            old_name='lang',
            new_name='language',
        ),
    ]