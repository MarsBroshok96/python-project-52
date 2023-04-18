# Generated by Django 4.1.7 on 2023-04-18 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('name', models.CharField(max_length=55, unique=True, verbose_name='name')),
            ],
            options={
                'verbose_name': 'status',
                'verbose_name_plural': 'statuses',
            },
        ),
    ]
