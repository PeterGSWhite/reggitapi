# Generated by Django 3.2.6 on 2021-08-05 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reggit', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='body',
            new_name='pattern',
        ),
        migrations.AddField(
            model_name='post',
            name='test_text',
            field=models.CharField(default='', max_length=500000),
            preserve_default=False,
        ),
    ]