# Generated by Django 4.0.4 on 2022-06-06 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelves', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reader',
            name='id',
        ),
        migrations.AddField(
            model_name='reader',
            name='reader_id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]