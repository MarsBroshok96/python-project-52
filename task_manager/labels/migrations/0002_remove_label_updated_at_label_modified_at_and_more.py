# Generated by Django 4.1.7 on 2023-04-23 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='label',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='label',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='modified at'),
        ),
        migrations.AlterField(
            model_name='label',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
    ]
