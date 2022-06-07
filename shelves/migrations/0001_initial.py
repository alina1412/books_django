# Generated by Django 4.0.4 on 2022-06-07 03:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('tags', models.TextField(blank=True, max_length=200, null=True)),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shelves.reader')),
            ],
            options={
                'verbose_name_plural': 'Books',
            },
        ),
    ]
